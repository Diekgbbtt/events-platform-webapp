import logging
import sys
from lsprotocol import types
from pygls.cli import start_server
from pygls.lsp.server import LanguageServer
from enum import Enum
from pathlib import Path
from urllib.parse import urlparse, unquote
from urllib.request import url2pathname
from pygls.workspace import TextDocument

from dtm.compiler import compile as data_compile, DataModelError
from stm.compiler import compile as security_compile, SecurityModelError
from ptm.compiler import compile as privacy_compile, PrivacyModelError, PrivacyModelWarning


InternalDiagnostic = DataModelError | SecurityModelError | PrivacyModelError | PrivacyModelWarning


# Client-side extensions must use the same language IDs
class NagLanguageId(Enum):
    DATA_MODEL = "nag-data-model"
    SECURITY_MODEL = "nag-security-model"
    PRIVACY_MODEL = "nag-privacy-model"


def get_sibling_file_with_extension(server: LanguageServer, uri: str, new_extension: str) -> tuple[str, str] | None:
    parsed = urlparse(uri)
    current_path = Path(url2pathname(unquote(parsed.path)))
    sibling_path = current_path.with_suffix(new_extension)
    sibling_uri = sibling_path.as_uri()
    
    try:
        doc = server.workspace.get_text_document(sibling_uri)
        return (sibling_uri, doc.source)
    except KeyError:
        if sibling_path.exists():
            return (sibling_uri, sibling_path.read_text())
        else:
            return None

def get_required_sibling(
    server: LanguageServer, 
    uri: str, 
    extension: str,
    error_class: type[InternalDiagnostic]
) -> str:
    sibling = get_sibling_file_with_extension(server, uri, extension)
    if not sibling:
        raise error_class(None, f"Cannot find {extension} file")
    return sibling[1]

def collect_internal_diagnostics(
    server: LanguageServer,
    document: TextDocument
) -> list[InternalDiagnostic]:
    warnings = []
    try:
        match document.language_id:
            case NagLanguageId.DATA_MODEL.value:
                _, warnings = data_compile(document.source)
                
            case NagLanguageId.SECURITY_MODEL.value:
                data_model_source = get_required_sibling(server, document.uri, ".dtm", SecurityModelError)

                data_model, warnings = data_compile(data_model_source)
                _ = security_compile(data_model, document.source)
                
            case NagLanguageId.PRIVACY_MODEL.value:
                data_model_source = get_required_sibling(server, document.uri, ".dtm", PrivacyModelError)
                security_model_source = get_required_sibling(server, document.uri, ".stm", PrivacyModelError)

                data_model = data_compile(data_model_source)
                security_model = security_compile(data_model, security_model_source)
                _, warnings = privacy_compile(data_model, security_model, document.source)
                
            case other:
                raise ValueError(f"Unrecognized language ID: {other}")    
    except (DataModelError, SecurityModelError, PrivacyModelError) as error:
        return [error] + warnings   # type: ignore
    except Exception:
        logging.exception("Internal compiler error")
        raise
    
    return warnings

def collect_diagnostics(server: LanguageServer, document: TextDocument) -> list[types.Diagnostic]:
    def make_range(range) -> types.Range:
        if range:
            return types.Range(
                start=types.Position(line=range.start_line - 1, character=range.start_column),
                end=types.Position(line=range.end_line - 1, character=range.end_column)
            )
        else:
            return types.Range(
                start=types.Position(line=0, character=0),
                end=types.Position(line=0, character=0)
            )

    internal_diagnostics = collect_internal_diagnostics(server, document)

    diagnostics = []
    for diagnostic in internal_diagnostics:
        diagnostics.append(
            types.Diagnostic(
                message=diagnostic.msg,
                severity=types.DiagnosticSeverity.Warning 
                         if diagnostic.severity == "warning" 
                         else types.DiagnosticSeverity.Error,
                range=make_range(diagnostic.range)
            )
        )

    return diagnostics

def collect_and_publish_diagnostics(server: LanguageServer, uri: str):
    document = server.workspace.get_text_document(uri)
    
    if document.language_id is None:
        return

    diagnostics = collect_diagnostics(server, document)
    server.text_document_publish_diagnostics(
        types.PublishDiagnosticsParams(
            uri=uri,
            version=document.version,
            diagnostics=diagnostics
        )
    )


server = LanguageServer("nag-py-server", "v0.1")

@server.feature(types.TEXT_DOCUMENT_DID_OPEN)
def did_open(server: LanguageServer, params: types.DidOpenTextDocumentParams):
    collect_and_publish_diagnostics(server, params.text_document.uri)

@server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
def did_change(server: LanguageServer, params: types.DidChangeTextDocumentParams):
    collect_and_publish_diagnostics(server, params.text_document.uri)

@server.feature(types.TEXT_DOCUMENT_DID_SAVE)
def did_save(server: LanguageServer, params: types.DidSaveTextDocumentParams):
    collect_and_publish_diagnostics(server, params.text_document.uri)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stderr,  # required for IO mode, as stdout is read by the client
        level=logging.DEBUG
    )
    start_server(server)
from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener
from dtm.parser import DataModelVisitor, DataModelParser, DataModelLexer
from range import Range


class DataModelError(Exception):
    def __init__(self, range: Range | None, msg='Data model error'):
        self.range = range
        self.msg = msg
        self.severity = "error"


class DTMErrorListener(ErrorListener):

    def __init__(self):
        super(DTMErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise DataModelError(Range(line, column, line, column), f"Syntax error: {msg}")

class JSONVisitor(DataModelVisitor):

    def __init__(self):
        self.datamodel = []
        self.component = ""
        self.propertyType = ""
        self.attributes = []
        self.methods = []
        self.association = {}
        self.allTypes = set()

    def get_assoc_name(name1, name2):
        return "Association_" + name1 + "_" + name2

    def visitDataModel(self, ctx):
        self.visitChildren(ctx)
        for a in self.association:
            if len(self.association[a]) != 2:
                raise DataModelError(
                    None, 
                    f"Association '{a}' is not binary (actual arity: {len(self.association[a])}; expected: 2)")
            self.datamodel.append({
                "class": a,
                "isAssociation": True,
                "ends": self.association[a]
            })
        cs = list(map(lambda c: c["class"],filter((lambda c: "isAssociation" not in c),self.datamodel))) + ['String','Integer','Real','Boolean']
        for c in self.allTypes:
            if c not in cs:
               raise DataModelError(None, f"Type '{c}' is not defined")


    def visitEntityComponent(self, ctx):
        self.visitChildren(ctx)
        cls = list(filter((lambda c: c["class"] == self.component),self.datamodel))
        if len(cls)>0:
            raise DataModelError(
                Range.from_context(ctx.entity().TypeName()), 
                f"Entity '{self.component}' already defined")

        self.datamodel.append({
            "class": self.component,
            "attributes" : self.attributes,
            "methods" : self.methods
        })
        self.attributes = []
        self.methods = []

    def visitEnumComponent(self, ctx):
        self.visitChildren(ctx)
        cls = list(filter((lambda c: c["class"] == self.component),self.datamodel))
        if len(cls)>0:
            raise DataModelError(
                Range.from_context(ctx.enumm().TypeName()), 
                f"Enum '{self.component}' already defined")
        self.datamodel.append({
            "class": self.component,
            "isEnum": True,
            "attributes": self.attributes
        })
        self.attributes = []
        self.methods = []

    def visitEntity(self, ctx):
        self.component=ctx.TypeName().getText()
        return self.visitChildren(ctx)

    def visitAttribute(self, ctx):
        self.visitChildren(ctx)
        name = ctx.propertyName().getText()
        ats = list(filter((lambda a: a["name"] == name),self.attributes))
        if len(ats)>0:
            raise DataModelError(
                Range.from_context(ctx.propertyName()), 
                f"Attribute '{name}' already defined")
        self.attributes.append({
				"name": name,
				"type": self.propertyType
			})

    def visitEnd(self, ctx):
        self.visitChildren(ctx)
        end = {
            "name": ctx.propertyName()[0].getText(),
            "target": self.propertyType if "type" not in self.propertyType else self.propertyType["type"],
            "mult": "1" if "collection" not in self.propertyType else "*"
        }
        if len(ctx.propertyName()) <= 1:
            # in
            association = ctx.TypeName().getText()
        else:
            # oppositeTo
            name1 = ctx.propertyName()[0].getText()
            name2 = ctx.propertyName()[1].getText()
            (name1, name2) = (name2, name1) if name2 < name1 else (name1, name2)
            association = JSONVisitor.get_assoc_name(name1, name2)


        if association in self.association:
                self.association[association].append(end)
        else:
            self.association[association] = [end]

    def visitMethod(self, ctx):
        self.visitChildren(ctx)
        entry = False
        if ctx.getChild(0) is not None and ctx.getChild(0).getText() == "@entry":
            entry = True
        name = ctx.propertyName()[0].getText()
        if name == 'main':
            raise DataModelError(
                Range.from_context(ctx.propertyName()[0]), 
                f"Defined method is not allowed to have the name 'main'")
        params = []
        i = 0
        for p in ctx.argName:
            params.append({
                "name": p.getText(),
                "type": ctx.argTypes[i].getText()
            })
            i += 1
        mts = list(filter((lambda m: m["name"] == name),self.methods))
        pt = list(map(lambda e: e["type"],params))
        if len(mts)>0:
            oload = False
            for m in mts:
                mt = list(map(lambda e: e["type"],m["params"]))
                if mt == pt:
                    oload = True
            if oload:
                raise DataModelError(
                    Range.from_context(ctx.propertyName()[0]), 
                    f"Method '{name}' with parameters '{pt}' already defined")
        self.methods.append({
            "entry": entry,
            "name": name,
            "return": ctx.retType.getText() if ctx.retType != None else "Void",
            "params": params
        })

    def visitCollectionType(self, ctx):
        self.visitChildren(ctx)
        self.propertyType = {
            "collection": ctx.collectionTypeName().getText(),
            "type": self.propertyType
        }

    def visitBasicType(self, ctx):
        self.propertyType = ctx.getText()
        self.allTypes.add(self.propertyType)

    def visitEnumm(self, ctx):
        self.component=ctx.TypeName().getText()
        return self.visitChildren(ctx)

    def visitEnumBody(self, ctx):
        lit = ctx.EnumLiteral().getText() if ctx.EnumLiteral()!=None else ctx.TypeName().getText()
        self.attributes.append(lit)
        return self.visitChildren(ctx)


def compile(s):
    listener = DTMErrorListener()

    input_stream = InputStream(s)
    lexer = DataModelLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(listener)

    stream = CommonTokenStream(lexer)
    parser = DataModelParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(listener)
    
    tree = parser.dataModel()
    visitor = JSONVisitor()
    tree.accept(visitor)
    return visitor.datamodel, []
from antlr4 import ParserRuleContext, TerminalNode
from dataclasses import dataclass
from typing import Self

@dataclass
class Range:
    start_line: int
    start_column: int
    end_line: int
    end_column: int

    def __post_init__(self):
        assert (self.end_line > self.start_line) or \
            (self.start_line == self.end_line and self.start_column <= self.end_column)
    
    @classmethod
    def from_context(cls, ctx: ParserRuleContext | TerminalNode) -> Self:
        if isinstance(ctx, TerminalNode):
            token = ctx.symbol  # type: ignore
            return cls(token.line, token.column, token.line, token.column + len(token.text))
        else:
            return cls(ctx.start.line, ctx.start.column, ctx.stop.line, ctx.stop.column)
    
    def __str__(self) -> str:
        if self.start_line == self.end_line and self.start_column == self.end_column:
            return f"{self.start_line}:{self.start_column}"
        else:
            return f"{self.start_line}:{self.start_column}~{self.end_line}:{self.end_column}"
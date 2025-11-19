from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener
from ocl.parser import OclExpressionVisitor, OclExpressionParser, OclExpressionLexer



class OCLParseError(Exception):
    def __init__(self, msg = 'OCL parse error'):
        self.msg = msg


class OCLErrorListener(ErrorListener):

    def __init__(self):
        super(OCLErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise OCLParseError("OCLParseError: Syntax error at line {} col {}: {}".format(line, column, msg))

    # def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
    #     raise OCLParseError()

    # def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
    #     raise OCLParseError()

    # def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
    #     raise OCLParseError()

class LambdaVisitor(OclExpressionVisitor):
    def __init__(self, dm=[], module=None):
        self.ind = ""
        self.result = ""
        self.free_vars = []
        self.bound_vars = set()
        self.call = False
        self.dm = dm
        self.module = module

    def reset(self):
        self.ind = ""
        self.result = ""
        self.free_vars = []
        self.bound_vars = set()
        self.call = False
        # self.dm = []
        # self.module = None

    def add_free(self,x):
        if x not in self.free_vars:
            self.free_vars.append(x)

    def lambda_exp(self):
        args = ', '.join(x + "= None" for x in self.free_vars)
        return f"(lambda {args}: {self.result})"

    def line(self, s):
        self.result += self.ind + s + "\n"

    def inline(self, s):
        self.result += s

    def indent(self):
        self.ind += "  "

    def unindent(self):
        self.ind = self.ind[2:]

    def visitUnaryOperation(self, ctx):
        self.inline(ctx.operator.text + " ")
        self.visit(ctx.expression)

    def visitAttributeNavigation(self, ctx):
        self.visit(ctx.expression)
        self.inline(f".dot('{ctx.attname.getText()}')")

    def visitPrimaryExpression(self, ctx):
        return self.visitChildren(ctx)

    def visitArithmeticBinaryOperation(self, ctx):
        self.visit(ctx.left)
        if ctx.operator.text == 'div':
            self.inline(' // ')
        elif ctx.operator.text == 'mod':
            self.inline(' % ')
        else:
            self.inline(f" {ctx.operator.text} ")
        self.visit(ctx.right)

    def visitSimpleName(self, ctx):
        name = ctx.getText()
        cls = list(map((lambda c: c["class"]), filter((lambda c: "isAssociation" not in c),self.dm))) + ['Role']
        if name not in self.bound_vars and not self.call and name not in cls:
            self.add_free(name)
        if name in cls:
            if self.module:
                name = f"{self.module}.{name}"
        self.inline(name)

    def visitFullQualifiedName(self, ctx):
        if self.module:
            self.inline(f"{self.module}.{ctx.getText().replace('::', '.')}")
        else:
            self.inline(ctx.getText().replace('::', '.'))

    def visitComparisonBinaryOperation(self, ctx):
        self.visit(ctx.left)
        operator = ctx.operator.text
        operator = operator if operator != '=' else '=='
        operator = operator if operator != '<>' else '!='
        self.inline(f" {operator} ")
        self.visit(ctx.right)

    def visitCollectionCall(self, ctx):
        operation = ctx.attname.getText()

        self.visit(ctx.expression)
        self.inline(f".{operation}(")
        self.visit(ctx.argExp())
        self.inline(")")


    def visitBooleanBinaryOperation(self, ctx):
        op = ctx.operator.text
        op = op if op != 'implies' else '<='
        op = op if op != 'xor' else '!='
        self.visit(ctx.left)
        self.inline(f" {op} ")
        self.visit(ctx.right)

    def visitCallExpression(self, ctx):
        self.call = True
        self.visit(ctx.expression)
        self.call = False
        self.inline("(")
        self.visit(ctx.argExp())
        self.inline(")")

    def visitMethodCall(self, ctx):
        if ctx.attname.getText() == 'oclAsType':
            self.visit(ctx.expression)
            return
        if ctx.attname.getText() == 'concat':
            self.inline('(')
            self.visit(ctx.expression)
            self.inline(' + ')
            self.visit(ctx.argExp())
            self.inline(')')
            return
        if ctx.attname.getText() == 'size':
            self.inline('len(')
            self.visit(ctx.expression)
            self.inline(')')
            return

        self.visit(ctx.expression)
        self.inline(f".{ctx.attname.getText()}(")
        self.visit(ctx.argExp())
        self.inline(")")

    def visitArgumentsExp(self, ctx):
        for exp in ctx.oclExp():
            self.visit(exp)
            if exp is not ctx.oclExp()[-1]:
                self.inline(', ')

    def visitLambdaExp(self, ctx):
        for x in ctx.varnames:
            self.bound_vars.add(x.getText())
        args = ', '.join(x.getText() for x in ctx.varnames)
        self.inline(f"(lambda {args}: ")
        self.visit(ctx.oclExp())
        self.inline(f")")
        for x in ctx.varnames:
            self.bound_vars.remove(x.getText())

    def visitFoldExp(self, ctx):
        x = ctx.varname.getText()
        acc = ctx.accname.getText()
        self.bound_vars.add(x)
        self.bound_vars.add(acc)
        self.visit(ctx.accvalue)
        self.inline(f", ")
        self.inline(f"(lambda {acc}, {x}: ")
        self.visit(ctx.oclExp()[-1])
        self.inline(f")")
        self.bound_vars.remove(x)
        self.bound_vars.remove(acc)

    def visitNestedExp(self, ctx):
        self.inline('(')
        self.visit(ctx.nested)
        self.inline(')')

    def visitSelfExp(self, ctx):
        if 'self' not in self.bound_vars:
            self.add_free('self')
        self.inline('self')

    def visitNumberLiteral(self, ctx):
        self.inline(ctx.getText())

    def visitStringLiteral(self, ctx):
        self.inline(ctx.getText())

    def visitBooleanLiteral(self, ctx):
        self.inline(ctx.getText().capitalize())

    def visitUnlimitedNaturalLiteral(self, ctx):
        return self.visitChildren(ctx)

    def visitInvalidLiteral(self, ctx):
        self.inline("None")

    def visitNullLiteral(self, ctx):
        self.inline("None")

    def visitTupleLiteralExp(self, ctx):
        self.inline('OCLTuple(')
        for part in ctx.tupleLiteralPartCS():
            self.visit(part)
            if part is not ctx.tupleLiteralPartCS()[-1]:
                self.inline(", ")
        self.inline(')')

    def visitTupleLiteralPartCS(self, ctx):
        self.inline(f"{ctx.unrestrictedName().getText()}=")
        self.visit(ctx.oclExp())

    def visitCollectionLiteralExp(self, ctx):
        ctype = ctx.collectionTypeCS().getText()
        if ctype == 'Sequence' or ctype == 'Bag':
            opening = '['
            ending = ']'
        elif ctype == 'Set' and len(ctx.expressions) > 0:
            opening = '{'
            ending = '}'
        elif ctype == 'Set':
            opening = 'set('
            ending = ')'
        elif ctype == 'OrderedSet':
            opening = 'dict.fromkeys(['
            ending = '])'
        self.inline(opening)
        for exp in ctx.expressions:
            self.visit(exp)
            if exp is not ctx.expressions[-1]:
                self.inline(', ')
        self.inline(ending)

    def visitCollectionTypeCS(self, ctx):
        self.visitChildren(ctx)

    def visitStringType(self, ctx):
        return self.visitChildren(ctx)

    def visitIntegerType(self, ctx):
        return self.visitChildren(ctx)

    def visitUnlimitedNaturalType(self, ctx):
        return self.visitChildren(ctx)

    def visitBooleanType(self, ctx):
        return self.visitChildren(ctx)

    def visitCollectionType(self, ctx):
        return self.visitChildren(ctx)

    def visitBagType(self, ctx):
        return self.visitChildren(ctx)

    def visitOrderedSetType(self, ctx):
        self.inline(ctx.getText())

    def visitSequenceType(self, ctx):
        self.inline("list")

    def visitSetType(self, ctx):
        self.inline("set")

    def visitCollectionLiteralPartCS(self, ctx):
        if ctx.isInterval:
            self.inline("*range(")
            self.visit(ctx.inf)
            self.inline(", ")
            self.visit(ctx.sup)
            self.inline("+1")
            self.inline(")")
        else:
            self.visitChildren(ctx)

    def visitTypeLiteralExp(self, ctx):
        return self.visitChildren(ctx)

    def visitLetExp(self, ctx):
        args = ', '.join(x.unrestrictedName().getText() for x in ctx.variables)
        self.inline(f"(lambda {args}: ")
        for x in ctx.variables:
            self.bound_vars.add(x.unrestrictedName().getText())
        self.visit(ctx.oclExp())
        for x in ctx.variables:
            self.bound_vars.remove(x.unrestrictedName().getText())
        self.inline(")(")
        for param in ctx.variables:
            self.visit(param.oclExp())
            if param is not ctx.variables[-1]:
                self.inline(", ")
        self.inline(")")

    def visitLetVariableCS(self, ctx):
        self.inline(f"{ctx.unrestrictedName().getText()} = ")
        self.visit(ctx.oclExp())
        self.line("")

    def visitTypeExpCS(self, ctx):
        return self.visitChildren(ctx)

    def visitTypeNameExpCS(self, ctx):
        return self.visitChildren(ctx)

    def visitTypeLiteralCS(self, ctx):
        return self.visitChildren(ctx)

    def visitTupleTypeCS(self, ctx):
        return self.visitChildren(ctx)

    def visitTuplePartCS(self, ctx):
        return self.visitChildren(ctx)

    def visitIfExp(self, ctx):
        self.visit(ctx.body)
        self.inline(" if ")
        self.visit(ctx.condition)
        self.inline(" else ")
        self.visit(ctx.else_)

    def visitNumberLiteralExpCS(self, ctx):
        return self.visitChildren(ctx)

    def visitStringLiteralExpCS(self, ctx):
        return self.visitChildren(ctx)

    def visitBooleanLiteralExpCS(self, ctx):
        return self.visitChildren(ctx)

    def visitUnlimitedNaturalLiteralCS(self, ctx):
        return self.visitChildren(ctx)

    def visitInvalidLiteralExpCS(self, ctx):
        return self.visitChildren(ctx)

    def visitNullLiteralExpCS(self, ctx):
        return self.visitChildren(ctx)

    def visitUnrestrictedName(self, ctx):
        return self.visitChildren(ctx)

    def visitUnreservedName(self, ctx):
        return self.visitChildren(ctx)


def compile(s):
    input_stream = InputStream(s)
    lexer = OclExpressionLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = OclExpressionParser(stream)
    parser.removeErrorListeners()
    listener = OCLErrorListener()
    parser.addErrorListener(listener)
    
    tree = parser.ocl()
    visitor = LambdaVisitor()
    tree.accept(visitor)
    return (visitor.lambda_exp(), set(visitor.free_vars))

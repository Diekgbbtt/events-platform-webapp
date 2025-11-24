# Generated from PrivacyModel.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PrivacyModelParser import PrivacyModelParser
else:
    from PrivacyModelParser import PrivacyModelParser

# This class defines a complete generic visitor for a parse tree produced by PrivacyModelParser.

class PrivacyModelVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PrivacyModelParser#privacyModel.
    def visitPrivacyModel(self, ctx:PrivacyModelParser.PrivacyModelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#personaldata.
    def visitPersonaldata(self, ctx:PrivacyModelParser.PersonaldataContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#resources.
    def visitResources(self, ctx:PrivacyModelParser.ResourcesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#purposes.
    def visitPurposes(self, ctx:PrivacyModelParser.PurposesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#SimplePurpose.
    def visitSimplePurpose(self, ctx:PrivacyModelParser.SimplePurposeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#ComplexPurpose.
    def visitComplexPurpose(self, ctx:PrivacyModelParser.ComplexPurposeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#apurposes.
    def visitApurposes(self, ctx:PrivacyModelParser.ApurposesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#apurpose.
    def visitApurpose(self, ctx:PrivacyModelParser.ApurposeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#dpurposes.
    def visitDpurposes(self, ctx:PrivacyModelParser.DpurposesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#dpurpose.
    def visitDpurpose(self, ctx:PrivacyModelParser.DpurposeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#methodName.
    def visitMethodName(self, ctx:PrivacyModelParser.MethodNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#constraint.
    def visitConstraint(self, ctx:PrivacyModelParser.ConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#desc.
    def visitDesc(self, ctx:PrivacyModelParser.DescContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#ocl.
    def visitOcl(self, ctx:PrivacyModelParser.OclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#UnaryOperation.
    def visitUnaryOperation(self, ctx:PrivacyModelParser.UnaryOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#AttributeNavigation.
    def visitAttributeNavigation(self, ctx:PrivacyModelParser.AttributeNavigationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#PrimaryExpression.
    def visitPrimaryExpression(self, ctx:PrivacyModelParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#ArithmeticBinaryOperation.
    def visitArithmeticBinaryOperation(self, ctx:PrivacyModelParser.ArithmeticBinaryOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#SimpleName.
    def visitSimpleName(self, ctx:PrivacyModelParser.SimpleNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#FullQualifiedName.
    def visitFullQualifiedName(self, ctx:PrivacyModelParser.FullQualifiedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#ComparisonBinaryOperation.
    def visitComparisonBinaryOperation(self, ctx:PrivacyModelParser.ComparisonBinaryOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#CollectionCall.
    def visitCollectionCall(self, ctx:PrivacyModelParser.CollectionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#BooleanBinaryOperation.
    def visitBooleanBinaryOperation(self, ctx:PrivacyModelParser.BooleanBinaryOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#MethodCall.
    def visitMethodCall(self, ctx:PrivacyModelParser.MethodCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#CallExpression.
    def visitCallExpression(self, ctx:PrivacyModelParser.CallExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#FoldExp.
    def visitFoldExp(self, ctx:PrivacyModelParser.FoldExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#LambdaExp.
    def visitLambdaExp(self, ctx:PrivacyModelParser.LambdaExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#ArgumentsExp.
    def visitArgumentsExp(self, ctx:PrivacyModelParser.ArgumentsExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#primaryExp.
    def visitPrimaryExp(self, ctx:PrivacyModelParser.PrimaryExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#selfExp.
    def visitSelfExp(self, ctx:PrivacyModelParser.SelfExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#nestedExp.
    def visitNestedExp(self, ctx:PrivacyModelParser.NestedExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#NumberLiteral.
    def visitNumberLiteral(self, ctx:PrivacyModelParser.NumberLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#StringLiteral.
    def visitStringLiteral(self, ctx:PrivacyModelParser.StringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#BooleanLiteral.
    def visitBooleanLiteral(self, ctx:PrivacyModelParser.BooleanLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#UnlimitedNaturalLiteral.
    def visitUnlimitedNaturalLiteral(self, ctx:PrivacyModelParser.UnlimitedNaturalLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#InvalidLiteral.
    def visitInvalidLiteral(self, ctx:PrivacyModelParser.InvalidLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#NullLiteral.
    def visitNullLiteral(self, ctx:PrivacyModelParser.NullLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#tupleLiteralExp.
    def visitTupleLiteralExp(self, ctx:PrivacyModelParser.TupleLiteralExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#tupleLiteralPartCS.
    def visitTupleLiteralPartCS(self, ctx:PrivacyModelParser.TupleLiteralPartCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#collectionLiteralExp.
    def visitCollectionLiteralExp(self, ctx:PrivacyModelParser.CollectionLiteralExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#collectionTypeCS.
    def visitCollectionTypeCS(self, ctx:PrivacyModelParser.CollectionTypeCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#StringType.
    def visitStringType(self, ctx:PrivacyModelParser.StringTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#IntegerType.
    def visitIntegerType(self, ctx:PrivacyModelParser.IntegerTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#RealType.
    def visitRealType(self, ctx:PrivacyModelParser.RealTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#BooleanType.
    def visitBooleanType(self, ctx:PrivacyModelParser.BooleanTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#CollectionType.
    def visitCollectionType(self, ctx:PrivacyModelParser.CollectionTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#BagType.
    def visitBagType(self, ctx:PrivacyModelParser.BagTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#OrderedSetType.
    def visitOrderedSetType(self, ctx:PrivacyModelParser.OrderedSetTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#SequenceType.
    def visitSequenceType(self, ctx:PrivacyModelParser.SequenceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#SetType.
    def visitSetType(self, ctx:PrivacyModelParser.SetTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#collectionLiteralPartCS.
    def visitCollectionLiteralPartCS(self, ctx:PrivacyModelParser.CollectionLiteralPartCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#typeLiteralExp.
    def visitTypeLiteralExp(self, ctx:PrivacyModelParser.TypeLiteralExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#letExp.
    def visitLetExp(self, ctx:PrivacyModelParser.LetExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#letVariableCS.
    def visitLetVariableCS(self, ctx:PrivacyModelParser.LetVariableCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#typeExpCS.
    def visitTypeExpCS(self, ctx:PrivacyModelParser.TypeExpCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#typeNameExpCS.
    def visitTypeNameExpCS(self, ctx:PrivacyModelParser.TypeNameExpCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#typeLiteralCS.
    def visitTypeLiteralCS(self, ctx:PrivacyModelParser.TypeLiteralCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#tupleTypeCS.
    def visitTupleTypeCS(self, ctx:PrivacyModelParser.TupleTypeCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#tuplePartCS.
    def visitTuplePartCS(self, ctx:PrivacyModelParser.TuplePartCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#ifExp.
    def visitIfExp(self, ctx:PrivacyModelParser.IfExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#numberLiteralExpCS.
    def visitNumberLiteralExpCS(self, ctx:PrivacyModelParser.NumberLiteralExpCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#stringLiteralExpCS.
    def visitStringLiteralExpCS(self, ctx:PrivacyModelParser.StringLiteralExpCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#booleanLiteralExpCS.
    def visitBooleanLiteralExpCS(self, ctx:PrivacyModelParser.BooleanLiteralExpCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#unlimitedNaturalLiteralCS.
    def visitUnlimitedNaturalLiteralCS(self, ctx:PrivacyModelParser.UnlimitedNaturalLiteralCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#invalidLiteralExpCS.
    def visitInvalidLiteralExpCS(self, ctx:PrivacyModelParser.InvalidLiteralExpCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#nullLiteralExpCS.
    def visitNullLiteralExpCS(self, ctx:PrivacyModelParser.NullLiteralExpCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#unrestrictedName.
    def visitUnrestrictedName(self, ctx:PrivacyModelParser.UnrestrictedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PrivacyModelParser#unreservedName.
    def visitUnreservedName(self, ctx:PrivacyModelParser.UnreservedNameContext):
        return self.visitChildren(ctx)



del PrivacyModelParser
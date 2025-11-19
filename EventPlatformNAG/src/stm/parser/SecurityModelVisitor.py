# Generated from SecurityModel.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SecurityModelParser import SecurityModelParser
else:
    from SecurityModelParser import SecurityModelParser

# This class defines a complete generic visitor for a parse tree produced by SecurityModelParser.

class SecurityModelVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SecurityModelParser#securityModel.
    def visitSecurityModel(self, ctx:SecurityModelParser.SecurityModelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#userClass.
    def visitUserClass(self, ctx:SecurityModelParser.UserClassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#roles.
    def visitRoles(self, ctx:SecurityModelParser.RolesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#srole.
    def visitSrole(self, ctx:SecurityModelParser.SroleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#role.
    def visitRole(self, ctx:SecurityModelParser.RoleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#resources.
    def visitResources(self, ctx:SecurityModelParser.ResourcesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#resource.
    def visitResource(self, ctx:SecurityModelParser.ResourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#ActionUnconstrained.
    def visitActionUnconstrained(self, ctx:SecurityModelParser.ActionUnconstrainedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#ActionConstrained.
    def visitActionConstrained(self, ctx:SecurityModelParser.ActionConstrainedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#actions.
    def visitActions(self, ctx:SecurityModelParser.ActionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#ActionResource.
    def visitActionResource(self, ctx:SecurityModelParser.ActionResourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#ActionAttribute.
    def visitActionAttribute(self, ctx:SecurityModelParser.ActionAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#constraint.
    def visitConstraint(self, ctx:SecurityModelParser.ConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#attributeName.
    def visitAttributeName(self, ctx:SecurityModelParser.AttributeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#ocl.
    def visitOcl(self, ctx:SecurityModelParser.OclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#UnaryOperation.
    def visitUnaryOperation(self, ctx:SecurityModelParser.UnaryOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#AttributeNavigation.
    def visitAttributeNavigation(self, ctx:SecurityModelParser.AttributeNavigationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#PrimaryExpression.
    def visitPrimaryExpression(self, ctx:SecurityModelParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#ArithmeticBinaryOperation.
    def visitArithmeticBinaryOperation(self, ctx:SecurityModelParser.ArithmeticBinaryOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#SimpleName.
    def visitSimpleName(self, ctx:SecurityModelParser.SimpleNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#FullQualifiedName.
    def visitFullQualifiedName(self, ctx:SecurityModelParser.FullQualifiedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#ComparisonBinaryOperation.
    def visitComparisonBinaryOperation(self, ctx:SecurityModelParser.ComparisonBinaryOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#CollectionCall.
    def visitCollectionCall(self, ctx:SecurityModelParser.CollectionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#BooleanBinaryOperation.
    def visitBooleanBinaryOperation(self, ctx:SecurityModelParser.BooleanBinaryOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#MethodCall.
    def visitMethodCall(self, ctx:SecurityModelParser.MethodCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#CallExpression.
    def visitCallExpression(self, ctx:SecurityModelParser.CallExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#FoldExp.
    def visitFoldExp(self, ctx:SecurityModelParser.FoldExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#LambdaExp.
    def visitLambdaExp(self, ctx:SecurityModelParser.LambdaExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#ArgumentsExp.
    def visitArgumentsExp(self, ctx:SecurityModelParser.ArgumentsExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#primaryExp.
    def visitPrimaryExp(self, ctx:SecurityModelParser.PrimaryExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#selfExp.
    def visitSelfExp(self, ctx:SecurityModelParser.SelfExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#nestedExp.
    def visitNestedExp(self, ctx:SecurityModelParser.NestedExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#NumberLiteral.
    def visitNumberLiteral(self, ctx:SecurityModelParser.NumberLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#StringLiteral.
    def visitStringLiteral(self, ctx:SecurityModelParser.StringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#BooleanLiteral.
    def visitBooleanLiteral(self, ctx:SecurityModelParser.BooleanLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#UnlimitedNaturalLiteral.
    def visitUnlimitedNaturalLiteral(self, ctx:SecurityModelParser.UnlimitedNaturalLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#InvalidLiteral.
    def visitInvalidLiteral(self, ctx:SecurityModelParser.InvalidLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#NullLiteral.
    def visitNullLiteral(self, ctx:SecurityModelParser.NullLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#tupleLiteralExp.
    def visitTupleLiteralExp(self, ctx:SecurityModelParser.TupleLiteralExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#tupleLiteralPartCS.
    def visitTupleLiteralPartCS(self, ctx:SecurityModelParser.TupleLiteralPartCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#collectionLiteralExp.
    def visitCollectionLiteralExp(self, ctx:SecurityModelParser.CollectionLiteralExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#collectionTypeCS.
    def visitCollectionTypeCS(self, ctx:SecurityModelParser.CollectionTypeCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#StringType.
    def visitStringType(self, ctx:SecurityModelParser.StringTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#IntegerType.
    def visitIntegerType(self, ctx:SecurityModelParser.IntegerTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#RealType.
    def visitRealType(self, ctx:SecurityModelParser.RealTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#BooleanType.
    def visitBooleanType(self, ctx:SecurityModelParser.BooleanTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#CollectionType.
    def visitCollectionType(self, ctx:SecurityModelParser.CollectionTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#BagType.
    def visitBagType(self, ctx:SecurityModelParser.BagTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#OrderedSetType.
    def visitOrderedSetType(self, ctx:SecurityModelParser.OrderedSetTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#SequenceType.
    def visitSequenceType(self, ctx:SecurityModelParser.SequenceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#SetType.
    def visitSetType(self, ctx:SecurityModelParser.SetTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#collectionLiteralPartCS.
    def visitCollectionLiteralPartCS(self, ctx:SecurityModelParser.CollectionLiteralPartCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#typeLiteralExp.
    def visitTypeLiteralExp(self, ctx:SecurityModelParser.TypeLiteralExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#letExp.
    def visitLetExp(self, ctx:SecurityModelParser.LetExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#letVariableCS.
    def visitLetVariableCS(self, ctx:SecurityModelParser.LetVariableCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#typeExpCS.
    def visitTypeExpCS(self, ctx:SecurityModelParser.TypeExpCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#typeNameExpCS.
    def visitTypeNameExpCS(self, ctx:SecurityModelParser.TypeNameExpCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#typeLiteralCS.
    def visitTypeLiteralCS(self, ctx:SecurityModelParser.TypeLiteralCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#tupleTypeCS.
    def visitTupleTypeCS(self, ctx:SecurityModelParser.TupleTypeCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#tuplePartCS.
    def visitTuplePartCS(self, ctx:SecurityModelParser.TuplePartCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#ifExp.
    def visitIfExp(self, ctx:SecurityModelParser.IfExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#numberLiteralExpCS.
    def visitNumberLiteralExpCS(self, ctx:SecurityModelParser.NumberLiteralExpCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#stringLiteralExpCS.
    def visitStringLiteralExpCS(self, ctx:SecurityModelParser.StringLiteralExpCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#booleanLiteralExpCS.
    def visitBooleanLiteralExpCS(self, ctx:SecurityModelParser.BooleanLiteralExpCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#unlimitedNaturalLiteralCS.
    def visitUnlimitedNaturalLiteralCS(self, ctx:SecurityModelParser.UnlimitedNaturalLiteralCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#invalidLiteralExpCS.
    def visitInvalidLiteralExpCS(self, ctx:SecurityModelParser.InvalidLiteralExpCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#nullLiteralExpCS.
    def visitNullLiteralExpCS(self, ctx:SecurityModelParser.NullLiteralExpCSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#unrestrictedName.
    def visitUnrestrictedName(self, ctx:SecurityModelParser.UnrestrictedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecurityModelParser#unreservedName.
    def visitUnreservedName(self, ctx:SecurityModelParser.UnreservedNameContext):
        return self.visitChildren(ctx)



del SecurityModelParser
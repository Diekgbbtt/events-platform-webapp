# Generated from SecurityModel.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SecurityModelParser import SecurityModelParser
else:
    from SecurityModelParser import SecurityModelParser

# This class defines a complete listener for a parse tree produced by SecurityModelParser.
class SecurityModelListener(ParseTreeListener):

    # Enter a parse tree produced by SecurityModelParser#securityModel.
    def enterSecurityModel(self, ctx:SecurityModelParser.SecurityModelContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#securityModel.
    def exitSecurityModel(self, ctx:SecurityModelParser.SecurityModelContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#userClass.
    def enterUserClass(self, ctx:SecurityModelParser.UserClassContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#userClass.
    def exitUserClass(self, ctx:SecurityModelParser.UserClassContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#roles.
    def enterRoles(self, ctx:SecurityModelParser.RolesContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#roles.
    def exitRoles(self, ctx:SecurityModelParser.RolesContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#srole.
    def enterSrole(self, ctx:SecurityModelParser.SroleContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#srole.
    def exitSrole(self, ctx:SecurityModelParser.SroleContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#role.
    def enterRole(self, ctx:SecurityModelParser.RoleContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#role.
    def exitRole(self, ctx:SecurityModelParser.RoleContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#resources.
    def enterResources(self, ctx:SecurityModelParser.ResourcesContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#resources.
    def exitResources(self, ctx:SecurityModelParser.ResourcesContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#resource.
    def enterResource(self, ctx:SecurityModelParser.ResourceContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#resource.
    def exitResource(self, ctx:SecurityModelParser.ResourceContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#ActionUnconstrained.
    def enterActionUnconstrained(self, ctx:SecurityModelParser.ActionUnconstrainedContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#ActionUnconstrained.
    def exitActionUnconstrained(self, ctx:SecurityModelParser.ActionUnconstrainedContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#ActionConstrained.
    def enterActionConstrained(self, ctx:SecurityModelParser.ActionConstrainedContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#ActionConstrained.
    def exitActionConstrained(self, ctx:SecurityModelParser.ActionConstrainedContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#actions.
    def enterActions(self, ctx:SecurityModelParser.ActionsContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#actions.
    def exitActions(self, ctx:SecurityModelParser.ActionsContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#ActionResource.
    def enterActionResource(self, ctx:SecurityModelParser.ActionResourceContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#ActionResource.
    def exitActionResource(self, ctx:SecurityModelParser.ActionResourceContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#ActionAttribute.
    def enterActionAttribute(self, ctx:SecurityModelParser.ActionAttributeContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#ActionAttribute.
    def exitActionAttribute(self, ctx:SecurityModelParser.ActionAttributeContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#constraint.
    def enterConstraint(self, ctx:SecurityModelParser.ConstraintContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#constraint.
    def exitConstraint(self, ctx:SecurityModelParser.ConstraintContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#attributeName.
    def enterAttributeName(self, ctx:SecurityModelParser.AttributeNameContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#attributeName.
    def exitAttributeName(self, ctx:SecurityModelParser.AttributeNameContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#ocl.
    def enterOcl(self, ctx:SecurityModelParser.OclContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#ocl.
    def exitOcl(self, ctx:SecurityModelParser.OclContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#UnaryOperation.
    def enterUnaryOperation(self, ctx:SecurityModelParser.UnaryOperationContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#UnaryOperation.
    def exitUnaryOperation(self, ctx:SecurityModelParser.UnaryOperationContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#AttributeNavigation.
    def enterAttributeNavigation(self, ctx:SecurityModelParser.AttributeNavigationContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#AttributeNavigation.
    def exitAttributeNavigation(self, ctx:SecurityModelParser.AttributeNavigationContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#PrimaryExpression.
    def enterPrimaryExpression(self, ctx:SecurityModelParser.PrimaryExpressionContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#PrimaryExpression.
    def exitPrimaryExpression(self, ctx:SecurityModelParser.PrimaryExpressionContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#ArithmeticBinaryOperation.
    def enterArithmeticBinaryOperation(self, ctx:SecurityModelParser.ArithmeticBinaryOperationContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#ArithmeticBinaryOperation.
    def exitArithmeticBinaryOperation(self, ctx:SecurityModelParser.ArithmeticBinaryOperationContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#SimpleName.
    def enterSimpleName(self, ctx:SecurityModelParser.SimpleNameContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#SimpleName.
    def exitSimpleName(self, ctx:SecurityModelParser.SimpleNameContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#FullQualifiedName.
    def enterFullQualifiedName(self, ctx:SecurityModelParser.FullQualifiedNameContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#FullQualifiedName.
    def exitFullQualifiedName(self, ctx:SecurityModelParser.FullQualifiedNameContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#ComparisonBinaryOperation.
    def enterComparisonBinaryOperation(self, ctx:SecurityModelParser.ComparisonBinaryOperationContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#ComparisonBinaryOperation.
    def exitComparisonBinaryOperation(self, ctx:SecurityModelParser.ComparisonBinaryOperationContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#CollectionCall.
    def enterCollectionCall(self, ctx:SecurityModelParser.CollectionCallContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#CollectionCall.
    def exitCollectionCall(self, ctx:SecurityModelParser.CollectionCallContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#BooleanBinaryOperation.
    def enterBooleanBinaryOperation(self, ctx:SecurityModelParser.BooleanBinaryOperationContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#BooleanBinaryOperation.
    def exitBooleanBinaryOperation(self, ctx:SecurityModelParser.BooleanBinaryOperationContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#MethodCall.
    def enterMethodCall(self, ctx:SecurityModelParser.MethodCallContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#MethodCall.
    def exitMethodCall(self, ctx:SecurityModelParser.MethodCallContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#CallExpression.
    def enterCallExpression(self, ctx:SecurityModelParser.CallExpressionContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#CallExpression.
    def exitCallExpression(self, ctx:SecurityModelParser.CallExpressionContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#FoldExp.
    def enterFoldExp(self, ctx:SecurityModelParser.FoldExpContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#FoldExp.
    def exitFoldExp(self, ctx:SecurityModelParser.FoldExpContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#LambdaExp.
    def enterLambdaExp(self, ctx:SecurityModelParser.LambdaExpContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#LambdaExp.
    def exitLambdaExp(self, ctx:SecurityModelParser.LambdaExpContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#ArgumentsExp.
    def enterArgumentsExp(self, ctx:SecurityModelParser.ArgumentsExpContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#ArgumentsExp.
    def exitArgumentsExp(self, ctx:SecurityModelParser.ArgumentsExpContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#primaryExp.
    def enterPrimaryExp(self, ctx:SecurityModelParser.PrimaryExpContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#primaryExp.
    def exitPrimaryExp(self, ctx:SecurityModelParser.PrimaryExpContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#selfExp.
    def enterSelfExp(self, ctx:SecurityModelParser.SelfExpContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#selfExp.
    def exitSelfExp(self, ctx:SecurityModelParser.SelfExpContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#nestedExp.
    def enterNestedExp(self, ctx:SecurityModelParser.NestedExpContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#nestedExp.
    def exitNestedExp(self, ctx:SecurityModelParser.NestedExpContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#NumberLiteral.
    def enterNumberLiteral(self, ctx:SecurityModelParser.NumberLiteralContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#NumberLiteral.
    def exitNumberLiteral(self, ctx:SecurityModelParser.NumberLiteralContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#StringLiteral.
    def enterStringLiteral(self, ctx:SecurityModelParser.StringLiteralContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#StringLiteral.
    def exitStringLiteral(self, ctx:SecurityModelParser.StringLiteralContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#BooleanLiteral.
    def enterBooleanLiteral(self, ctx:SecurityModelParser.BooleanLiteralContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#BooleanLiteral.
    def exitBooleanLiteral(self, ctx:SecurityModelParser.BooleanLiteralContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#UnlimitedNaturalLiteral.
    def enterUnlimitedNaturalLiteral(self, ctx:SecurityModelParser.UnlimitedNaturalLiteralContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#UnlimitedNaturalLiteral.
    def exitUnlimitedNaturalLiteral(self, ctx:SecurityModelParser.UnlimitedNaturalLiteralContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#InvalidLiteral.
    def enterInvalidLiteral(self, ctx:SecurityModelParser.InvalidLiteralContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#InvalidLiteral.
    def exitInvalidLiteral(self, ctx:SecurityModelParser.InvalidLiteralContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#NullLiteral.
    def enterNullLiteral(self, ctx:SecurityModelParser.NullLiteralContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#NullLiteral.
    def exitNullLiteral(self, ctx:SecurityModelParser.NullLiteralContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#tupleLiteralExp.
    def enterTupleLiteralExp(self, ctx:SecurityModelParser.TupleLiteralExpContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#tupleLiteralExp.
    def exitTupleLiteralExp(self, ctx:SecurityModelParser.TupleLiteralExpContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#tupleLiteralPartCS.
    def enterTupleLiteralPartCS(self, ctx:SecurityModelParser.TupleLiteralPartCSContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#tupleLiteralPartCS.
    def exitTupleLiteralPartCS(self, ctx:SecurityModelParser.TupleLiteralPartCSContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#collectionLiteralExp.
    def enterCollectionLiteralExp(self, ctx:SecurityModelParser.CollectionLiteralExpContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#collectionLiteralExp.
    def exitCollectionLiteralExp(self, ctx:SecurityModelParser.CollectionLiteralExpContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#collectionTypeCS.
    def enterCollectionTypeCS(self, ctx:SecurityModelParser.CollectionTypeCSContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#collectionTypeCS.
    def exitCollectionTypeCS(self, ctx:SecurityModelParser.CollectionTypeCSContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#StringType.
    def enterStringType(self, ctx:SecurityModelParser.StringTypeContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#StringType.
    def exitStringType(self, ctx:SecurityModelParser.StringTypeContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#IntegerType.
    def enterIntegerType(self, ctx:SecurityModelParser.IntegerTypeContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#IntegerType.
    def exitIntegerType(self, ctx:SecurityModelParser.IntegerTypeContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#RealType.
    def enterRealType(self, ctx:SecurityModelParser.RealTypeContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#RealType.
    def exitRealType(self, ctx:SecurityModelParser.RealTypeContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#BooleanType.
    def enterBooleanType(self, ctx:SecurityModelParser.BooleanTypeContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#BooleanType.
    def exitBooleanType(self, ctx:SecurityModelParser.BooleanTypeContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#CollectionType.
    def enterCollectionType(self, ctx:SecurityModelParser.CollectionTypeContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#CollectionType.
    def exitCollectionType(self, ctx:SecurityModelParser.CollectionTypeContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#BagType.
    def enterBagType(self, ctx:SecurityModelParser.BagTypeContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#BagType.
    def exitBagType(self, ctx:SecurityModelParser.BagTypeContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#OrderedSetType.
    def enterOrderedSetType(self, ctx:SecurityModelParser.OrderedSetTypeContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#OrderedSetType.
    def exitOrderedSetType(self, ctx:SecurityModelParser.OrderedSetTypeContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#SequenceType.
    def enterSequenceType(self, ctx:SecurityModelParser.SequenceTypeContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#SequenceType.
    def exitSequenceType(self, ctx:SecurityModelParser.SequenceTypeContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#SetType.
    def enterSetType(self, ctx:SecurityModelParser.SetTypeContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#SetType.
    def exitSetType(self, ctx:SecurityModelParser.SetTypeContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#collectionLiteralPartCS.
    def enterCollectionLiteralPartCS(self, ctx:SecurityModelParser.CollectionLiteralPartCSContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#collectionLiteralPartCS.
    def exitCollectionLiteralPartCS(self, ctx:SecurityModelParser.CollectionLiteralPartCSContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#typeLiteralExp.
    def enterTypeLiteralExp(self, ctx:SecurityModelParser.TypeLiteralExpContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#typeLiteralExp.
    def exitTypeLiteralExp(self, ctx:SecurityModelParser.TypeLiteralExpContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#letExp.
    def enterLetExp(self, ctx:SecurityModelParser.LetExpContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#letExp.
    def exitLetExp(self, ctx:SecurityModelParser.LetExpContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#letVariableCS.
    def enterLetVariableCS(self, ctx:SecurityModelParser.LetVariableCSContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#letVariableCS.
    def exitLetVariableCS(self, ctx:SecurityModelParser.LetVariableCSContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#typeExpCS.
    def enterTypeExpCS(self, ctx:SecurityModelParser.TypeExpCSContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#typeExpCS.
    def exitTypeExpCS(self, ctx:SecurityModelParser.TypeExpCSContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#typeNameExpCS.
    def enterTypeNameExpCS(self, ctx:SecurityModelParser.TypeNameExpCSContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#typeNameExpCS.
    def exitTypeNameExpCS(self, ctx:SecurityModelParser.TypeNameExpCSContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#typeLiteralCS.
    def enterTypeLiteralCS(self, ctx:SecurityModelParser.TypeLiteralCSContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#typeLiteralCS.
    def exitTypeLiteralCS(self, ctx:SecurityModelParser.TypeLiteralCSContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#tupleTypeCS.
    def enterTupleTypeCS(self, ctx:SecurityModelParser.TupleTypeCSContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#tupleTypeCS.
    def exitTupleTypeCS(self, ctx:SecurityModelParser.TupleTypeCSContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#tuplePartCS.
    def enterTuplePartCS(self, ctx:SecurityModelParser.TuplePartCSContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#tuplePartCS.
    def exitTuplePartCS(self, ctx:SecurityModelParser.TuplePartCSContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#ifExp.
    def enterIfExp(self, ctx:SecurityModelParser.IfExpContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#ifExp.
    def exitIfExp(self, ctx:SecurityModelParser.IfExpContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#numberLiteralExpCS.
    def enterNumberLiteralExpCS(self, ctx:SecurityModelParser.NumberLiteralExpCSContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#numberLiteralExpCS.
    def exitNumberLiteralExpCS(self, ctx:SecurityModelParser.NumberLiteralExpCSContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#stringLiteralExpCS.
    def enterStringLiteralExpCS(self, ctx:SecurityModelParser.StringLiteralExpCSContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#stringLiteralExpCS.
    def exitStringLiteralExpCS(self, ctx:SecurityModelParser.StringLiteralExpCSContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#booleanLiteralExpCS.
    def enterBooleanLiteralExpCS(self, ctx:SecurityModelParser.BooleanLiteralExpCSContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#booleanLiteralExpCS.
    def exitBooleanLiteralExpCS(self, ctx:SecurityModelParser.BooleanLiteralExpCSContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#unlimitedNaturalLiteralCS.
    def enterUnlimitedNaturalLiteralCS(self, ctx:SecurityModelParser.UnlimitedNaturalLiteralCSContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#unlimitedNaturalLiteralCS.
    def exitUnlimitedNaturalLiteralCS(self, ctx:SecurityModelParser.UnlimitedNaturalLiteralCSContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#invalidLiteralExpCS.
    def enterInvalidLiteralExpCS(self, ctx:SecurityModelParser.InvalidLiteralExpCSContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#invalidLiteralExpCS.
    def exitInvalidLiteralExpCS(self, ctx:SecurityModelParser.InvalidLiteralExpCSContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#nullLiteralExpCS.
    def enterNullLiteralExpCS(self, ctx:SecurityModelParser.NullLiteralExpCSContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#nullLiteralExpCS.
    def exitNullLiteralExpCS(self, ctx:SecurityModelParser.NullLiteralExpCSContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#unrestrictedName.
    def enterUnrestrictedName(self, ctx:SecurityModelParser.UnrestrictedNameContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#unrestrictedName.
    def exitUnrestrictedName(self, ctx:SecurityModelParser.UnrestrictedNameContext):
        pass


    # Enter a parse tree produced by SecurityModelParser#unreservedName.
    def enterUnreservedName(self, ctx:SecurityModelParser.UnreservedNameContext):
        pass

    # Exit a parse tree produced by SecurityModelParser#unreservedName.
    def exitUnreservedName(self, ctx:SecurityModelParser.UnreservedNameContext):
        pass



del SecurityModelParser
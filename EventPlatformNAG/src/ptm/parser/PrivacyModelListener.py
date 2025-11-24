# Generated from PrivacyModel.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PrivacyModelParser import PrivacyModelParser
else:
    from PrivacyModelParser import PrivacyModelParser

# This class defines a complete listener for a parse tree produced by PrivacyModelParser.
class PrivacyModelListener(ParseTreeListener):

    # Enter a parse tree produced by PrivacyModelParser#privacyModel.
    def enterPrivacyModel(self, ctx:PrivacyModelParser.PrivacyModelContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#privacyModel.
    def exitPrivacyModel(self, ctx:PrivacyModelParser.PrivacyModelContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#personaldata.
    def enterPersonaldata(self, ctx:PrivacyModelParser.PersonaldataContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#personaldata.
    def exitPersonaldata(self, ctx:PrivacyModelParser.PersonaldataContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#resources.
    def enterResources(self, ctx:PrivacyModelParser.ResourcesContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#resources.
    def exitResources(self, ctx:PrivacyModelParser.ResourcesContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#purposes.
    def enterPurposes(self, ctx:PrivacyModelParser.PurposesContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#purposes.
    def exitPurposes(self, ctx:PrivacyModelParser.PurposesContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#SimplePurpose.
    def enterSimplePurpose(self, ctx:PrivacyModelParser.SimplePurposeContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#SimplePurpose.
    def exitSimplePurpose(self, ctx:PrivacyModelParser.SimplePurposeContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#ComplexPurpose.
    def enterComplexPurpose(self, ctx:PrivacyModelParser.ComplexPurposeContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#ComplexPurpose.
    def exitComplexPurpose(self, ctx:PrivacyModelParser.ComplexPurposeContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#apurposes.
    def enterApurposes(self, ctx:PrivacyModelParser.ApurposesContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#apurposes.
    def exitApurposes(self, ctx:PrivacyModelParser.ApurposesContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#apurpose.
    def enterApurpose(self, ctx:PrivacyModelParser.ApurposeContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#apurpose.
    def exitApurpose(self, ctx:PrivacyModelParser.ApurposeContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#dpurposes.
    def enterDpurposes(self, ctx:PrivacyModelParser.DpurposesContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#dpurposes.
    def exitDpurposes(self, ctx:PrivacyModelParser.DpurposesContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#dpurpose.
    def enterDpurpose(self, ctx:PrivacyModelParser.DpurposeContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#dpurpose.
    def exitDpurpose(self, ctx:PrivacyModelParser.DpurposeContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#methodName.
    def enterMethodName(self, ctx:PrivacyModelParser.MethodNameContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#methodName.
    def exitMethodName(self, ctx:PrivacyModelParser.MethodNameContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#constraint.
    def enterConstraint(self, ctx:PrivacyModelParser.ConstraintContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#constraint.
    def exitConstraint(self, ctx:PrivacyModelParser.ConstraintContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#desc.
    def enterDesc(self, ctx:PrivacyModelParser.DescContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#desc.
    def exitDesc(self, ctx:PrivacyModelParser.DescContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#ocl.
    def enterOcl(self, ctx:PrivacyModelParser.OclContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#ocl.
    def exitOcl(self, ctx:PrivacyModelParser.OclContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#UnaryOperation.
    def enterUnaryOperation(self, ctx:PrivacyModelParser.UnaryOperationContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#UnaryOperation.
    def exitUnaryOperation(self, ctx:PrivacyModelParser.UnaryOperationContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#AttributeNavigation.
    def enterAttributeNavigation(self, ctx:PrivacyModelParser.AttributeNavigationContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#AttributeNavigation.
    def exitAttributeNavigation(self, ctx:PrivacyModelParser.AttributeNavigationContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#PrimaryExpression.
    def enterPrimaryExpression(self, ctx:PrivacyModelParser.PrimaryExpressionContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#PrimaryExpression.
    def exitPrimaryExpression(self, ctx:PrivacyModelParser.PrimaryExpressionContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#ArithmeticBinaryOperation.
    def enterArithmeticBinaryOperation(self, ctx:PrivacyModelParser.ArithmeticBinaryOperationContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#ArithmeticBinaryOperation.
    def exitArithmeticBinaryOperation(self, ctx:PrivacyModelParser.ArithmeticBinaryOperationContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#SimpleName.
    def enterSimpleName(self, ctx:PrivacyModelParser.SimpleNameContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#SimpleName.
    def exitSimpleName(self, ctx:PrivacyModelParser.SimpleNameContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#FullQualifiedName.
    def enterFullQualifiedName(self, ctx:PrivacyModelParser.FullQualifiedNameContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#FullQualifiedName.
    def exitFullQualifiedName(self, ctx:PrivacyModelParser.FullQualifiedNameContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#ComparisonBinaryOperation.
    def enterComparisonBinaryOperation(self, ctx:PrivacyModelParser.ComparisonBinaryOperationContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#ComparisonBinaryOperation.
    def exitComparisonBinaryOperation(self, ctx:PrivacyModelParser.ComparisonBinaryOperationContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#CollectionCall.
    def enterCollectionCall(self, ctx:PrivacyModelParser.CollectionCallContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#CollectionCall.
    def exitCollectionCall(self, ctx:PrivacyModelParser.CollectionCallContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#BooleanBinaryOperation.
    def enterBooleanBinaryOperation(self, ctx:PrivacyModelParser.BooleanBinaryOperationContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#BooleanBinaryOperation.
    def exitBooleanBinaryOperation(self, ctx:PrivacyModelParser.BooleanBinaryOperationContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#MethodCall.
    def enterMethodCall(self, ctx:PrivacyModelParser.MethodCallContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#MethodCall.
    def exitMethodCall(self, ctx:PrivacyModelParser.MethodCallContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#CallExpression.
    def enterCallExpression(self, ctx:PrivacyModelParser.CallExpressionContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#CallExpression.
    def exitCallExpression(self, ctx:PrivacyModelParser.CallExpressionContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#FoldExp.
    def enterFoldExp(self, ctx:PrivacyModelParser.FoldExpContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#FoldExp.
    def exitFoldExp(self, ctx:PrivacyModelParser.FoldExpContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#LambdaExp.
    def enterLambdaExp(self, ctx:PrivacyModelParser.LambdaExpContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#LambdaExp.
    def exitLambdaExp(self, ctx:PrivacyModelParser.LambdaExpContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#ArgumentsExp.
    def enterArgumentsExp(self, ctx:PrivacyModelParser.ArgumentsExpContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#ArgumentsExp.
    def exitArgumentsExp(self, ctx:PrivacyModelParser.ArgumentsExpContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#primaryExp.
    def enterPrimaryExp(self, ctx:PrivacyModelParser.PrimaryExpContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#primaryExp.
    def exitPrimaryExp(self, ctx:PrivacyModelParser.PrimaryExpContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#selfExp.
    def enterSelfExp(self, ctx:PrivacyModelParser.SelfExpContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#selfExp.
    def exitSelfExp(self, ctx:PrivacyModelParser.SelfExpContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#nestedExp.
    def enterNestedExp(self, ctx:PrivacyModelParser.NestedExpContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#nestedExp.
    def exitNestedExp(self, ctx:PrivacyModelParser.NestedExpContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#NumberLiteral.
    def enterNumberLiteral(self, ctx:PrivacyModelParser.NumberLiteralContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#NumberLiteral.
    def exitNumberLiteral(self, ctx:PrivacyModelParser.NumberLiteralContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#StringLiteral.
    def enterStringLiteral(self, ctx:PrivacyModelParser.StringLiteralContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#StringLiteral.
    def exitStringLiteral(self, ctx:PrivacyModelParser.StringLiteralContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#BooleanLiteral.
    def enterBooleanLiteral(self, ctx:PrivacyModelParser.BooleanLiteralContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#BooleanLiteral.
    def exitBooleanLiteral(self, ctx:PrivacyModelParser.BooleanLiteralContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#UnlimitedNaturalLiteral.
    def enterUnlimitedNaturalLiteral(self, ctx:PrivacyModelParser.UnlimitedNaturalLiteralContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#UnlimitedNaturalLiteral.
    def exitUnlimitedNaturalLiteral(self, ctx:PrivacyModelParser.UnlimitedNaturalLiteralContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#InvalidLiteral.
    def enterInvalidLiteral(self, ctx:PrivacyModelParser.InvalidLiteralContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#InvalidLiteral.
    def exitInvalidLiteral(self, ctx:PrivacyModelParser.InvalidLiteralContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#NullLiteral.
    def enterNullLiteral(self, ctx:PrivacyModelParser.NullLiteralContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#NullLiteral.
    def exitNullLiteral(self, ctx:PrivacyModelParser.NullLiteralContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#tupleLiteralExp.
    def enterTupleLiteralExp(self, ctx:PrivacyModelParser.TupleLiteralExpContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#tupleLiteralExp.
    def exitTupleLiteralExp(self, ctx:PrivacyModelParser.TupleLiteralExpContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#tupleLiteralPartCS.
    def enterTupleLiteralPartCS(self, ctx:PrivacyModelParser.TupleLiteralPartCSContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#tupleLiteralPartCS.
    def exitTupleLiteralPartCS(self, ctx:PrivacyModelParser.TupleLiteralPartCSContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#collectionLiteralExp.
    def enterCollectionLiteralExp(self, ctx:PrivacyModelParser.CollectionLiteralExpContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#collectionLiteralExp.
    def exitCollectionLiteralExp(self, ctx:PrivacyModelParser.CollectionLiteralExpContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#collectionTypeCS.
    def enterCollectionTypeCS(self, ctx:PrivacyModelParser.CollectionTypeCSContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#collectionTypeCS.
    def exitCollectionTypeCS(self, ctx:PrivacyModelParser.CollectionTypeCSContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#StringType.
    def enterStringType(self, ctx:PrivacyModelParser.StringTypeContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#StringType.
    def exitStringType(self, ctx:PrivacyModelParser.StringTypeContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#IntegerType.
    def enterIntegerType(self, ctx:PrivacyModelParser.IntegerTypeContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#IntegerType.
    def exitIntegerType(self, ctx:PrivacyModelParser.IntegerTypeContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#RealType.
    def enterRealType(self, ctx:PrivacyModelParser.RealTypeContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#RealType.
    def exitRealType(self, ctx:PrivacyModelParser.RealTypeContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#BooleanType.
    def enterBooleanType(self, ctx:PrivacyModelParser.BooleanTypeContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#BooleanType.
    def exitBooleanType(self, ctx:PrivacyModelParser.BooleanTypeContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#CollectionType.
    def enterCollectionType(self, ctx:PrivacyModelParser.CollectionTypeContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#CollectionType.
    def exitCollectionType(self, ctx:PrivacyModelParser.CollectionTypeContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#BagType.
    def enterBagType(self, ctx:PrivacyModelParser.BagTypeContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#BagType.
    def exitBagType(self, ctx:PrivacyModelParser.BagTypeContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#OrderedSetType.
    def enterOrderedSetType(self, ctx:PrivacyModelParser.OrderedSetTypeContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#OrderedSetType.
    def exitOrderedSetType(self, ctx:PrivacyModelParser.OrderedSetTypeContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#SequenceType.
    def enterSequenceType(self, ctx:PrivacyModelParser.SequenceTypeContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#SequenceType.
    def exitSequenceType(self, ctx:PrivacyModelParser.SequenceTypeContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#SetType.
    def enterSetType(self, ctx:PrivacyModelParser.SetTypeContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#SetType.
    def exitSetType(self, ctx:PrivacyModelParser.SetTypeContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#collectionLiteralPartCS.
    def enterCollectionLiteralPartCS(self, ctx:PrivacyModelParser.CollectionLiteralPartCSContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#collectionLiteralPartCS.
    def exitCollectionLiteralPartCS(self, ctx:PrivacyModelParser.CollectionLiteralPartCSContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#typeLiteralExp.
    def enterTypeLiteralExp(self, ctx:PrivacyModelParser.TypeLiteralExpContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#typeLiteralExp.
    def exitTypeLiteralExp(self, ctx:PrivacyModelParser.TypeLiteralExpContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#letExp.
    def enterLetExp(self, ctx:PrivacyModelParser.LetExpContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#letExp.
    def exitLetExp(self, ctx:PrivacyModelParser.LetExpContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#letVariableCS.
    def enterLetVariableCS(self, ctx:PrivacyModelParser.LetVariableCSContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#letVariableCS.
    def exitLetVariableCS(self, ctx:PrivacyModelParser.LetVariableCSContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#typeExpCS.
    def enterTypeExpCS(self, ctx:PrivacyModelParser.TypeExpCSContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#typeExpCS.
    def exitTypeExpCS(self, ctx:PrivacyModelParser.TypeExpCSContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#typeNameExpCS.
    def enterTypeNameExpCS(self, ctx:PrivacyModelParser.TypeNameExpCSContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#typeNameExpCS.
    def exitTypeNameExpCS(self, ctx:PrivacyModelParser.TypeNameExpCSContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#typeLiteralCS.
    def enterTypeLiteralCS(self, ctx:PrivacyModelParser.TypeLiteralCSContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#typeLiteralCS.
    def exitTypeLiteralCS(self, ctx:PrivacyModelParser.TypeLiteralCSContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#tupleTypeCS.
    def enterTupleTypeCS(self, ctx:PrivacyModelParser.TupleTypeCSContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#tupleTypeCS.
    def exitTupleTypeCS(self, ctx:PrivacyModelParser.TupleTypeCSContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#tuplePartCS.
    def enterTuplePartCS(self, ctx:PrivacyModelParser.TuplePartCSContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#tuplePartCS.
    def exitTuplePartCS(self, ctx:PrivacyModelParser.TuplePartCSContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#ifExp.
    def enterIfExp(self, ctx:PrivacyModelParser.IfExpContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#ifExp.
    def exitIfExp(self, ctx:PrivacyModelParser.IfExpContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#numberLiteralExpCS.
    def enterNumberLiteralExpCS(self, ctx:PrivacyModelParser.NumberLiteralExpCSContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#numberLiteralExpCS.
    def exitNumberLiteralExpCS(self, ctx:PrivacyModelParser.NumberLiteralExpCSContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#stringLiteralExpCS.
    def enterStringLiteralExpCS(self, ctx:PrivacyModelParser.StringLiteralExpCSContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#stringLiteralExpCS.
    def exitStringLiteralExpCS(self, ctx:PrivacyModelParser.StringLiteralExpCSContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#booleanLiteralExpCS.
    def enterBooleanLiteralExpCS(self, ctx:PrivacyModelParser.BooleanLiteralExpCSContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#booleanLiteralExpCS.
    def exitBooleanLiteralExpCS(self, ctx:PrivacyModelParser.BooleanLiteralExpCSContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#unlimitedNaturalLiteralCS.
    def enterUnlimitedNaturalLiteralCS(self, ctx:PrivacyModelParser.UnlimitedNaturalLiteralCSContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#unlimitedNaturalLiteralCS.
    def exitUnlimitedNaturalLiteralCS(self, ctx:PrivacyModelParser.UnlimitedNaturalLiteralCSContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#invalidLiteralExpCS.
    def enterInvalidLiteralExpCS(self, ctx:PrivacyModelParser.InvalidLiteralExpCSContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#invalidLiteralExpCS.
    def exitInvalidLiteralExpCS(self, ctx:PrivacyModelParser.InvalidLiteralExpCSContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#nullLiteralExpCS.
    def enterNullLiteralExpCS(self, ctx:PrivacyModelParser.NullLiteralExpCSContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#nullLiteralExpCS.
    def exitNullLiteralExpCS(self, ctx:PrivacyModelParser.NullLiteralExpCSContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#unrestrictedName.
    def enterUnrestrictedName(self, ctx:PrivacyModelParser.UnrestrictedNameContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#unrestrictedName.
    def exitUnrestrictedName(self, ctx:PrivacyModelParser.UnrestrictedNameContext):
        pass


    # Enter a parse tree produced by PrivacyModelParser#unreservedName.
    def enterUnreservedName(self, ctx:PrivacyModelParser.UnreservedNameContext):
        pass

    # Exit a parse tree produced by PrivacyModelParser#unreservedName.
    def exitUnreservedName(self, ctx:PrivacyModelParser.UnreservedNameContext):
        pass



del PrivacyModelParser
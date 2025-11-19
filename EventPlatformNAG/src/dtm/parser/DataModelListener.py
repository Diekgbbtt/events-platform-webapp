# Generated from DataModel.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .DataModelParser import DataModelParser
else:
    from DataModelParser import DataModelParser

# This class defines a complete listener for a parse tree produced by DataModelParser.
class DataModelListener(ParseTreeListener):

    # Enter a parse tree produced by DataModelParser#dataModel.
    def enterDataModel(self, ctx:DataModelParser.DataModelContext):
        pass

    # Exit a parse tree produced by DataModelParser#dataModel.
    def exitDataModel(self, ctx:DataModelParser.DataModelContext):
        pass


    # Enter a parse tree produced by DataModelParser#components.
    def enterComponents(self, ctx:DataModelParser.ComponentsContext):
        pass

    # Exit a parse tree produced by DataModelParser#components.
    def exitComponents(self, ctx:DataModelParser.ComponentsContext):
        pass


    # Enter a parse tree produced by DataModelParser#EntityComponent.
    def enterEntityComponent(self, ctx:DataModelParser.EntityComponentContext):
        pass

    # Exit a parse tree produced by DataModelParser#EntityComponent.
    def exitEntityComponent(self, ctx:DataModelParser.EntityComponentContext):
        pass


    # Enter a parse tree produced by DataModelParser#EnumComponent.
    def enterEnumComponent(self, ctx:DataModelParser.EnumComponentContext):
        pass

    # Exit a parse tree produced by DataModelParser#EnumComponent.
    def exitEnumComponent(self, ctx:DataModelParser.EnumComponentContext):
        pass


    # Enter a parse tree produced by DataModelParser#entity.
    def enterEntity(self, ctx:DataModelParser.EntityContext):
        pass

    # Exit a parse tree produced by DataModelParser#entity.
    def exitEntity(self, ctx:DataModelParser.EntityContext):
        pass


    # Enter a parse tree produced by DataModelParser#entityBody.
    def enterEntityBody(self, ctx:DataModelParser.EntityBodyContext):
        pass

    # Exit a parse tree produced by DataModelParser#entityBody.
    def exitEntityBody(self, ctx:DataModelParser.EntityBodyContext):
        pass


    # Enter a parse tree produced by DataModelParser#Attribute.
    def enterAttribute(self, ctx:DataModelParser.AttributeContext):
        pass

    # Exit a parse tree produced by DataModelParser#Attribute.
    def exitAttribute(self, ctx:DataModelParser.AttributeContext):
        pass


    # Enter a parse tree produced by DataModelParser#End.
    def enterEnd(self, ctx:DataModelParser.EndContext):
        pass

    # Exit a parse tree produced by DataModelParser#End.
    def exitEnd(self, ctx:DataModelParser.EndContext):
        pass


    # Enter a parse tree produced by DataModelParser#Method.
    def enterMethod(self, ctx:DataModelParser.MethodContext):
        pass

    # Exit a parse tree produced by DataModelParser#Method.
    def exitMethod(self, ctx:DataModelParser.MethodContext):
        pass


    # Enter a parse tree produced by DataModelParser#propertyType.
    def enterPropertyType(self, ctx:DataModelParser.PropertyTypeContext):
        pass

    # Exit a parse tree produced by DataModelParser#propertyType.
    def exitPropertyType(self, ctx:DataModelParser.PropertyTypeContext):
        pass


    # Enter a parse tree produced by DataModelParser#collectionType.
    def enterCollectionType(self, ctx:DataModelParser.CollectionTypeContext):
        pass

    # Exit a parse tree produced by DataModelParser#collectionType.
    def exitCollectionType(self, ctx:DataModelParser.CollectionTypeContext):
        pass


    # Enter a parse tree produced by DataModelParser#basicType.
    def enterBasicType(self, ctx:DataModelParser.BasicTypeContext):
        pass

    # Exit a parse tree produced by DataModelParser#basicType.
    def exitBasicType(self, ctx:DataModelParser.BasicTypeContext):
        pass


    # Enter a parse tree produced by DataModelParser#enumm.
    def enterEnumm(self, ctx:DataModelParser.EnummContext):
        pass

    # Exit a parse tree produced by DataModelParser#enumm.
    def exitEnumm(self, ctx:DataModelParser.EnummContext):
        pass


    # Enter a parse tree produced by DataModelParser#enumBody.
    def enterEnumBody(self, ctx:DataModelParser.EnumBodyContext):
        pass

    # Exit a parse tree produced by DataModelParser#enumBody.
    def exitEnumBody(self, ctx:DataModelParser.EnumBodyContext):
        pass


    # Enter a parse tree produced by DataModelParser#propertyName.
    def enterPropertyName(self, ctx:DataModelParser.PropertyNameContext):
        pass

    # Exit a parse tree produced by DataModelParser#propertyName.
    def exitPropertyName(self, ctx:DataModelParser.PropertyNameContext):
        pass


    # Enter a parse tree produced by DataModelParser#collectionTypeName.
    def enterCollectionTypeName(self, ctx:DataModelParser.CollectionTypeNameContext):
        pass

    # Exit a parse tree produced by DataModelParser#collectionTypeName.
    def exitCollectionTypeName(self, ctx:DataModelParser.CollectionTypeNameContext):
        pass


    # Enter a parse tree produced by DataModelParser#primitiveTypeName.
    def enterPrimitiveTypeName(self, ctx:DataModelParser.PrimitiveTypeNameContext):
        pass

    # Exit a parse tree produced by DataModelParser#primitiveTypeName.
    def exitPrimitiveTypeName(self, ctx:DataModelParser.PrimitiveTypeNameContext):
        pass



del DataModelParser
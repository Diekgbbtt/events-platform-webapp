# Generated from DataModel.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .DataModelParser import DataModelParser
else:
    from DataModelParser import DataModelParser

# This class defines a complete generic visitor for a parse tree produced by DataModelParser.

class DataModelVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by DataModelParser#dataModel.
    def visitDataModel(self, ctx:DataModelParser.DataModelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DataModelParser#components.
    def visitComponents(self, ctx:DataModelParser.ComponentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DataModelParser#EntityComponent.
    def visitEntityComponent(self, ctx:DataModelParser.EntityComponentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DataModelParser#EnumComponent.
    def visitEnumComponent(self, ctx:DataModelParser.EnumComponentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DataModelParser#entity.
    def visitEntity(self, ctx:DataModelParser.EntityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DataModelParser#entityBody.
    def visitEntityBody(self, ctx:DataModelParser.EntityBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DataModelParser#Attribute.
    def visitAttribute(self, ctx:DataModelParser.AttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DataModelParser#End.
    def visitEnd(self, ctx:DataModelParser.EndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DataModelParser#Method.
    def visitMethod(self, ctx:DataModelParser.MethodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DataModelParser#propertyType.
    def visitPropertyType(self, ctx:DataModelParser.PropertyTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DataModelParser#collectionType.
    def visitCollectionType(self, ctx:DataModelParser.CollectionTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DataModelParser#basicType.
    def visitBasicType(self, ctx:DataModelParser.BasicTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DataModelParser#enumm.
    def visitEnumm(self, ctx:DataModelParser.EnummContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DataModelParser#enumBody.
    def visitEnumBody(self, ctx:DataModelParser.EnumBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DataModelParser#propertyName.
    def visitPropertyName(self, ctx:DataModelParser.PropertyNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DataModelParser#collectionTypeName.
    def visitCollectionTypeName(self, ctx:DataModelParser.CollectionTypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DataModelParser#primitiveTypeName.
    def visitPrimitiveTypeName(self, ctx:DataModelParser.PrimitiveTypeNameContext):
        return self.visitChildren(ctx)



del DataModelParser
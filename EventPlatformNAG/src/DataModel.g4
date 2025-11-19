grammar DataModel;


dataModel: (components)+;

components: component (components)?;

component:  
      entity  # EntityComponent
    | enumm   # EnumComponent
;

entity: 'entity' TypeName '{' (entityBody)? '}'; 

entityBody: property entityBody?;

property: 
      propertyType propertyName                                             # Attribute
    | propertyType propertyName ('oppositeTo' propertyName | 'in' TypeName) # End
    | ('@entry')? (retType = propertyType)? propertyName 
        '(' (argTypes += propertyType argName += propertyName 
            (','  argTypes += propertyType argName += propertyName)* )? ')' # Method
;

propertyType: collectionType | basicType;

collectionType: collectionTypeName '(' propertyType ')';

basicType: primitiveTypeName | TypeName; 

enumm: 'enum' TypeName '{' enumBody '}';

enumBody: (EnumLiteral | TypeName) enumBody?;

TypeName: [A-Z][a-z_0-9]*;

EnumLiteral: [A-Z][A-Z_0-9]*;

propertyName: ID;



collectionTypeName:
    'Bag'           
|   'OrderedSet'    
|   'Sequence'      
|   'Set'           
;

primitiveTypeName:
    'String'            
|   'Integer'           
|   'Real'              
|   'Boolean'           
;

ID: [a-zA-Z_][a-zA-Z_0-9]*;
WS: [ \t\n\r]+ -> skip;
COMMENT: '//' ~[\r\n]* -> skip;

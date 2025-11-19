grammar OclExpression;

ocl:
    oclExp EOF
;

oclExp:
    expression=oclExp '->' attname=unrestrictedName argExp          # CollectionCall
|   expression=oclExp '.'  attname=unrestrictedName argExp          # MethodCall
|   expression=oclExp '.'  attname=unrestrictedName                 # AttributeNavigation
|   expression=oclExp argExp                                        # CallExpression
|   operator=('-'|'not') expression=oclExp                          # UnaryOperation
|   left=oclExp operator=('*'|'/'|'+'|'-'|'div'|'mod') right=oclExp             # ArithmeticBinaryOperation
|   left=oclExp operator=('='|'<'|'<='|'>'|'>='|'<>') right=oclExp  # ComparisonBinaryOperation
|   left=oclExp operator=('and'|'or'|'implies'|'xor') right=oclExp  # BooleanBinaryOperation
|   primaryExp                                                      # PrimaryExpression
|   unrestrictedName                                                # SimpleName
|   (unrestrictedName '::')+ unreservedName                         # FullQualifiedName
;

argExp:
   '(' varname=unrestrictedName 
        ';' accname=unrestrictedName '=' accvalue=oclExp '|' oclExp ')'             # FoldExp
|  '(' varnames+=unrestrictedName (',' varnames+=unrestrictedName)* '|' oclExp ')'  # LambdaExp
|  '(' (oclExp (',' oclExp)*)? ')'                                                  # ArgumentsExp
;

primaryExp:
		selfExp
|		nestedExp
|		primitiveLiteralExp
|		tupleLiteralExp
|		collectionLiteralExp
|		typeLiteralExp
|		letExp
|		ifExp
;

selfExp:
    'self'
;

nestedExp:
    '(' nested=oclExp ')'
;

primitiveLiteralExp:
	    numberLiteralExpCS          # NumberLiteral
|	    stringLiteralExpCS          # StringLiteral
|	    booleanLiteralExpCS         # BooleanLiteral
|	    unlimitedNaturalLiteralCS   # UnlimitedNaturalLiteral
|	    invalidLiteralExpCS         # InvalidLiteral
|	    nullLiteralExpCS            # NullLiteral
;

tupleLiteralExp:
    'Tuple' '{' tupleLiteralPartCS (',' tupleLiteralPartCS)*'}'
;

tupleLiteralPartCS:
    unrestrictedName (':' typeExpCS)? '=' oclExp
;

collectionLiteralExp:
    collectionTypeCS '{' (expressions+=collectionLiteralPartCS (',' expressions+=collectionLiteralPartCS)*)? '}'
;

collectionTypeCS:
    collectionTypeIdentifier ('(' typeExpCS ')'|'<' typeExpCS '>')?
;

primitiveTypeCS:
    'String'            # StringType
|   'Integer'           # IntegerType
|   'Real'              # RealType
|   'Boolean'           # BooleanType
;

collectionTypeIdentifier:
    'Collection'    # CollectionType
|   'Bag'           # BagType
|   'OrderedSet'    # OrderedSetType
|   'Sequence'      # SequenceType
|   'Set'           # SetType
;

collectionLiteralPartCS:
    oclExp
|   inf=oclExp isInterval='..' sup=oclExp
;

typeLiteralExp:
    typeLiteralCS
;

letExp:
    'let' variables+=letVariableCS (',' variables+=letVariableCS)* 'in' oclExp
;

letVariableCS:
    unrestrictedName (':' typeExpCS)? '=' oclExp
;

typeExpCS:
    typeLiteralCS
|   typeNameExpCS
;

typeNameExpCS:
    unrestrictedName
|   typeNameExpCS ('::' unreservedName)+
;

typeLiteralCS:
    collectionTypeCS
|   primitiveTypeCS
|   tupleTypeCS
;

tupleTypeCS:
    'Tuple' ('(' tuplePartCS (',' tuplePartCS)* ')'
|   '<' tuplePartCS (',' tuplePartCS)* '>')?
;

tuplePartCS:
    unrestrictedName ':' typeExpCS
;

ifExp:
    'if' condition=oclExp 'then' body=oclExp 'else' else_=oclExp 'endif'
;

numberLiteralExpCS:
    INT
|   FLOAT
;

stringLiteralExpCS:
    STRING
;

booleanLiteralExpCS:
    'true'|'false'
;

unlimitedNaturalLiteralCS:
    '*'
;

invalidLiteralExpCS:
    'invalid'
;

nullLiteralExpCS:
    'null'
;

unrestrictedName: ~('('|')'|'true'|'false'|'and'|'else'|'endif'|'false'|'if'|'implies'|'in'|'invalid'|'let'|'not'|'null'|'or'|'self'|'then'|'true'|'xor'|'Bag'|'Boolean'|'Collection'|'Integer'|'Lambda'|'OclAny'|'OclInvalid'|'OclMessage'|'OclSelf'|'OclVoid'|'OrderedSet'|'Real'|'Sequence'|'Set'|'String'|'Tuple');
unreservedName: ~('('|')'|'and'|'else'|'endif'|'false'|'if'|'implies'|'in'|'invalid'|'let'|'not'|'null'|'or'|'self'|'then'|'true'|'xor');

STRING: '\'' ~[']* '\'';
SPECIAL_VARNAME: '_' STRING;
VARNAME: [a-zA-Z_][a-zA-Z_0-9]*;
INT: [0-9]+;
FLOAT:  INT ('.' INT)? (('e'|'E') ('+'|'-')? INT)?;

// COMMENT:LINE_COMMENT|BLOCK_COMMENT|DOCU_COMMENT;
// LINE_COMMENT:'--' .*? '\n';
// BLOCK_COMMENT: '/*' .*? '*/';
// DOCU_COMMENT: '/**' .*? '*/';
WS: [ \n\t\r]+ -> skip;

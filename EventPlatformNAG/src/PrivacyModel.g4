grammar PrivacyModel;
import OclExpression;

privacyModel: personaldata purposes apurposes dpurposes;

personaldata: 'Personal data' '{' resources? '}';

resources: ResourceName ('.' ms+=methodName)? (',' resources)?;

purposes: 'Purposes' '{' purpose? '}';

purpose: PurposeName (',' purpose)?                               #SimplePurpose
  | PurposeName 'includes' (pss += PurposeName)+ (',' purpose)?   #ComplexPurpose
;

apurposes: 'Actual purposes' '{' apurpose? '}';

apurpose: ('main' PurposeName | ResourceName '.' methodName PurposeName) (',' apurpose)?;

dpurposes: 'Declared purposes' '{' dpurpose? '}';

dpurpose: rs+=ResourceName ('.' ms+=methodName)? (',' rs+=ResourceName ('.' ms+=methodName)?)* (constraint desc)? PurposeName (',' dpurpose)?;

PurposeName: [A-Z][A-Z_0-9]+;

ResourceName: [A-Z][a-z_0-9]*;

methodName: ID;

constraint: '[' oclExp ']';

desc: '<' (words+=ID)+ '>';


ID: [a-zA-Z_][a-zA-Z_0-9]*;
WS: [ \t\n\r]+ -> skip;



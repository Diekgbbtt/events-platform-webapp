grammar SecurityModel;
import OclExpression;

securityModel: userClass (roles)+;

userClass: 'USER' ResourceName;

roles: (srole | role) (roles)?;

srole: ('default' | 'anonymous') role;

role: 'Role' RoleName ('extends' RoleName)? '{' (resources | permissions)? '}';

resources: resource (resources)?;

resource: ResourceName '{' (permissions)? '}';

permissions: 
    actions (permissions)?              #ActionUnconstrained
  | actions constraint (permissions)?   #ActionConstrained
;

actions: action (',' actions)?;

action: 
    ActionType                          #ActionResource
  | ActionType ('(' attributeName ')')  #ActionAttribute
;

constraint: '[' oclExp ']';

RoleName: [A-Z][A-Z_0-9]+;

ActionType: 
    'fullAccess'
|   'create'
|   'delete'
|   'read'
|   'update'
|   'add'
|   'remove'
|   'execute'
;

ResourceName: [A-Z][a-z_0-9]*;

attributeName: ID;


ID: [a-zA-Z_][a-zA-Z_0-9]*;
WS: [ \t\n\r]+ -> skip;



# Copyright (c) 2025 All Rights Reserved
# Generated code

from model import Action, Constraint
from ocl.ocl import eval_python as eval_ocl
from types import LambdaType

class SecurityModel:

    # Extensible set of Roles and their hierarchy
    closure = {}
    
    @classmethod
    def close(cls,rs):
        pairs = set([(x,y) for x in rs for y in rs if x.isSubRole(y)])
        relations = {}
        for x,y in pairs:
            if x not in relations:
                relations[x] = []
            relations[x].append(y)
        
        closure = {} 
        def build_closure(n):
            def f(k):
                for y in relations.get(k, []):
                    if n not in closure:
                        closure[n] = set()
                    closure[n].add(y)
                    f(y)
            f(n)

        for k in relations.keys():
            build_closure(k)
        
        for r in rs:
            if r not in closure:
                closure[r] = set()
            closure[r].add(r)

        cls.closure = closure



    # Extensible model (default: deny all)
    model = {}

    # Checks permissions over the role hirearchy 
    @classmethod
    def permit(cls, r, attr, act, self, caller, value=None):
        def __securitycheck__():
            data = self.__class__.__name__
            for role in cls.Role:
                if role <= r:
                    if act == Action.create:
                        if eval_ocl(cls.check(role, data, data, act),caller=caller):
                            return True
                    elif act == Action.read or act == Action.delete:
                        if eval_ocl(cls.check(role, data, attr, act),caller=caller, self=self):
                            return True
                    elif act == Action.update or act == Action.add or act == Action.remove:
                        if eval_ocl(cls.check(role, data, attr, act),caller=caller, self=self, value=value):
                            return True
                    else: 
                        return True # Unsupported action
            return False
        return __securitycheck__()
     
    # Returns relevant constraints according to the model semantics 
    # Params: role: role enum, data: data model class name, attr: attribute name, act: action enum
    # Returns a function from the model that represents authorization constraint 
    @classmethod
    def check(cls, role, data, attr, act):
        try:
            return cls.model[role][data][attr][act]
        except KeyError:
            return Constraint.noAccess
        
    class ModelError(Exception):
        pass
    
    # Check that cls.model is well-formed 
    # 1. It should have the following shape:
    # {role: {data: {attribute: {action: constraint}}}}
    # 2. The types of the keys should be as follows:
    # type of role is cls.Role
    # type of data is str
    # type of attribute is str
    # type of action is Action
    # type of constraint is types.LambdaType
    # Returns: True if the model is well-formed both in terms of shape and types, False otherwise
    @classmethod
    def validate(cls):

        # l
        def checkLambda(l):
            if not type(l) is LambdaType:
                raise SecurityModel.ModelError(f"Constraint {l} should be of type LambdaType")
        
        # {ac: l}
        def checkAction(m):
            if type(m) is dict:
                for a in m:
                    if isinstance(a, Action):
                        checkLambda(m[a])
                    else:
                        raise SecurityModel.ModelError(f"Level 4 key {a} should be of type Action")
            else:
                raise SecurityModel.ModelError(f"Security model for a specific role, data, and attribute should be of type dict")
       
        # {at: {ac: l}}
        def checkAttribute(m):
            if type(m) is dict:
                for a in m:
                    if isinstance(a, str):
                        checkAction(m[a])
                    else:
                        raise SecurityModel.ModelError(f"Level 3 key {a} should be of type str")
            else:
                raise SecurityModel.ModelError(f"Security model for a specific role and data should be of type dict")
        
        # {d: {at: {ac: l}}}
        def checkData(m):
            if type(m) is dict:
                for d in m:
                    if isinstance(d, str):
                        checkAttribute(m[d])
                    else:
                         raise SecurityModel.ModelError(f"Level 2 key {d} should be of type str")
            else:
                raise SecurityModel.ModelError(f"Security model for a specific role should be of type dict")
        
        # {r: {d: {at: {ac: l}}}}
        def checkRole(m):
            if type(m) is dict:
                for r in m:
                    if isinstance(r, cls.Role):
                        checkData(m[r])
                    else:
                        raise SecurityModel.ModelError(f"Level 1 key {r} should be of type Role")
            else:
                raise SecurityModel.ModelError(f"Security model should be of type dict")

        checkRole(cls.model)
        

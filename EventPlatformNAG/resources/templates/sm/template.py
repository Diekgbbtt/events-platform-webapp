# Copyright (c) 2025 All Rights Reserved
# Generated code

from security_model import SecurityModel
from model import Action, Constraint
from enum import auto, Enum
import dtm

class FullAccess(SecurityModel):
    @classmethod
    def permit(cls, r, attr, act, self, caller, value=None):
        def __securitycheck__():
            return True
        return __securitycheck__()


# Security model

class {{projectname}}SecurityModel(SecurityModel):
    class Role(Enum):
        {% for r in sm.roles -%}
        {{ r.name }} = auto()
        {% endfor %}
        def isSubRole(self, obj):
            return ({%- for r in sm.roles -%}
                    {%- if r.extends is defined -%}
                    self == self.{{- r.extends}} and obj == self.{{- r.name}} or 
                    {% endif -%}
                    {%- endfor -%}
                    False)

        def __le__ (self,obj):
            if isinstance(obj,{{projectname}}SecurityModel.Role):
                if SecurityModel.closure == {}:
                    SecurityModel.close({{projectname}}SecurityModel.Role)
                return self in SecurityModel.closure and obj in SecurityModel.closure[self]
            else:
                raise ValueError
    
    model = {{ policy | replace('\'Action.read\'','Action.read') |
                        replace('\'Action.add\'','Action.add') |
                        replace('\'Action.remove\'','Action.remove') |
                        replace('\'Action.update\'','Action.update') |
                        replace('\'Action.create\'','Action.create') |
                        replace('\'Action.delete\'','Action.delete') |
                        replace('\'Constraint.fullAccess\'','Constraint.fullAccess') | 
                        replace('\'Constraint.noAccess\'','Constraint.noAccess') | 
                        r | rr | rrrr}}
    
{{projectname}}SecurityModel.validate()
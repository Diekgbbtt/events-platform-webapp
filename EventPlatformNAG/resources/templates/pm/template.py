# Copyright (c) 2025 All Rights Reserved
# Generated code

from model import Action, Constraint
from enum import auto, Enum
from privacy_model import PrivacyModel
import dtm

class {{projectname}}PrivacyModel(PrivacyModel):

    # Extensible model (default: nothing declared)

    class Purpose(Enum):
        {% if pm.purposes|length == 0 %}
        pass
        {% else %}
        {% for p in pm.purposes -%}
        {{ p.name }} = auto()
        {% endfor %}
        {% endif %}

        def get_subpurposes_names(self):
            ret = []
            for sp in purpose_hierarchy[self]:
                ret.append(sp.name)
                ret.extend(sp.get_subpurposes_names())
            return ret

    personaldata = [
        {% for p in pm.personalData -%}
        {{ p }}{% if not loop.last %},{% endif %}
        {% endfor -%}
    ]
        
    model = {{policy | replace('\'Action.read\'','Action.read') |
                        replace('\'Action.add\'','Action.add') |
                        replace('\'Action.remove\'','Action.remove') |
                        replace('\'Action.update\'','Action.update') |
                        replace('\'Action.create\'','Action.create') |
                        replace('\'Action.delete\'','Action.delete') |
                        replace('\'Constraint.fullAccess\'','Constraint.fullAccess') | 
                        replace('\'Constraint.noAccess\'','Constraint.noAccess') | 
                        r | rrr | rrrr }}

purpose_hierarchy = {
    {%- for p in pm.purposes %}
    {{projectname}}PrivacyModel.Purpose.{{ p.name }}: [
        {%- for sp in p.includes %}
        {{projectname}}PrivacyModel.Purpose.{{ sp }}{% if not loop.last %}, {% endif %}
        {%- endfor %}
    ]{% if not loop.last %}, {% endif %}
    {%- endfor %}
}

{{projectname}}PrivacyModel.validate()
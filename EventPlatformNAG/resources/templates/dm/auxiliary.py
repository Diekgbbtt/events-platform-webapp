# Copyright (c) 2025 All Rights Reserved
# Generated code

from instrumentation import secure
from dtm import {% for c in dm -%}{% if not c.isAssociation %}{{c.class}}, {% endif %}{% endfor %}db
from app import P

{% for c in dm if not c.isAssociation %}
{%- for m in c.methods %}
{%- if not m.entry %}
@secure(db,P({{- get_purpose(m.name)}}))
def {{m.name}}(args={}):
    return {{c.class}}.{{m.name}}(args)
{% endif %}
{% endfor %}
{%- endfor %}
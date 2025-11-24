# Copyright (c) 2025 All Rights Reserved
# Generated code

{% for c in dm if not c.isAssociation %}
{%- for m in c.methods %}
{%- if not m.entry %}
def {{m.name}}(args):
    # TODO: implement the method stub
    return "TODO: Implement the method stub" 
{% endif %}
{% endfor %}
{%- endfor %}
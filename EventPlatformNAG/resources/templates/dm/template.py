# Copyright (c) 2025 All Rights Reserved
# Generated code

from application import app
from flask_user import UserMixin, current_user
from stm import {{projectname}}SecurityModel
from ptm import {{projectname}}PrivacyModel
from ocl.ocl import OCLTerm
from sqlalchemy import UniqueConstraint

# Initialize SQLAlchemy database instance
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Set up deletion interception for security and privacy models
from instrumentation import Secure, setup_deletion_interception
setup_deletion_interception(db.session,{{projectname}}SecurityModel,{{projectname}}PrivacyModel)

# =========================
# Role Constants
# =========================
UNAUTHENTICATED_ROLE = "{{- sm.anonymousRole}}"
{% for role in sm.roles -%}
{{role.name}} = "{{role.name}}"
{% endfor %}


# =========================
# Purpose Constants
# =========================
{% for p in pm.purposes -%}
{{p.name}} = "{{p.name}}"
{% endfor %}


with app.app_context():

    # =========================
    # Association between Consent and Purpose
    # =========================
    # Many-to-many relationship between Consent and Purpose
    consentedpurposes = db.Table('consentedpurposes',
            db.Column('consent_id', db.Integer, db.ForeignKey('consent.id'), nullable=False, primary_key=True),
            db.Column('purpose_id', db.Integer, db.ForeignKey('purpose.id'), nullable=False, primary_key=True)
    )
    {% for c in dm if c.isAssociation-%}
    # =========================
    # Association between {{c.ends[0].target}} and {{c.ends[1].target}}
    # =========================
    {% if c.ends[0].target == c.ends[1].target %}
    class {{c.class | lower}}(db.Model):
        
        id = db.Column(db.Integer, primary_key=True)
        {{c.ends[0].name}}_id = db.Column(db.Integer(), db.ForeignKey('{{- c.ends[0].target | lower}}.id'){%- if c.ends[1].mult != '*' -%}, unique=True{%- endif -%})
        {{c.ends[1].name}}_id = db.Column(db.Integer(), db.ForeignKey('{{- c.ends[1].target | lower}}.id'){%- if c.ends[0].mult != '*' -%}, unique=True{%- endif -%})
    
    {% else %}
    class {{c.class | lower}}(db.Model):
            
        id = db.Column(db.Integer, primary_key=True)
        {{c.ends[0].name}}_id = db.Column(db.Integer(), db.ForeignKey('{{- c.ends[0].target | lower}}.id'){%- if c.ends[1].mult != '*' -%}, unique=True{%- endif -%})
        {{c.ends[1].name}}_id = db.Column(db.Integer(), db.ForeignKey('{{- c.ends[1].target | lower}}.id'){%- if c.ends[0].mult != '*' -%}, unique=True{%- endif -%})
        {{c.ends[0].name}} = db.relationship('{{- c.ends[0].target}}', back_populates='{{c.class | lower}}', uselist=False)
        {{c.ends[1].name}} = db.relationship('{{- c.ends[1].target}}', back_populates='{{c.class | lower}}', uselist=False)
    {% endif %}
    {% endfor %}

    # ENTITIES
    {% for c in dm -%}
    {%- if isUserClass(c,sm) %}
    # =========================
    # Entity {{c.class}} (User class)
    # =========================
    @Secure({{projectname}}SecurityModel,{{projectname}}PrivacyModel)
    class {{c.class}}(db.Model,UserMixin,OCLTerm):

        #Association-end type classes
        {% for ac in dm if ac.isAssociation %}
        {%- if ac.ends[0].target == c.class -%}
        class {{ac.ends[1].name}}List(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = {{ac.class | lower}}({{ac.ends[0].name}}=self._this,{{ac.ends[1].name}}=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = {{ac.class | lower}}.query.filter_by({{ac.ends[0].name}}=self._this,{{ac.ends[1].name}}=e).first()
                db.session.delete(v)
        {% endif -%} 
        {% if ac.ends[1].target == c.class -%} 
        class {{ac.ends[0].name}}List(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = {{ac.class | lower}}({{ac.ends[1].name}}=self._this,{{ac.ends[0].name}}=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = {{ac.class | lower}}.query.filter_by({{ac.ends[1].name}}=self._this,{{ac.ends[0].name}}=e).first()
                db.session.delete(v)
        {% endif -%}     
        {% endfor %}

        #Attributes
        id = db.Column(db.Integer, primary_key=True)
        active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
        roles = db.relationship('Role', secondary='user_roles')
        username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False, server_default='')
        {% for attr in c.attributes -%}
        {{attr.name}} = db.Column({{type(attr.type)}})
        {% endfor %}

        # Association ends
        {% for ac in dm if ac.isAssociation -%}
        {% if ac.ends[0].target == ac.ends[1].target %}
        {%- if ac.ends[0].target == c.class -%}
        {{ac.ends[1].name}} = db.relationship('{{- ac.ends[1].target}}',
                                 secondary='{{- ac.class | lower}}',
                                 cascade="all, delete-orphan", 
                                 primaryjoin=id=={{- ac.class | lower}}.{{- ac.ends[0].name | lower}}_id,
                                 secondaryjoin=id=={{- ac.class | lower}}.{{- ac.ends[1].name | lower}}_id,
                                 back_populates='{{- ac.ends[0].name}}')

        {% endif -%}  
        {%- if ac.ends[1].target == c.class -%}
        {{ac.ends[0].name}} = db.relationship('{{- ac.ends[0].target}}',
                                 secondary='{{- ac.class | lower}}',
                                 cascade="all, delete-orphan", 
                                 primaryjoin=id=={{- ac.class | lower}}.{{- ac.ends[1].name | lower}}_id,
                                 secondaryjoin=id=={{- ac.class | lower}}.{{- ac.ends[0].name | lower}}_id,
                                 back_populates='{{- ac.ends[1].name}}')
        {% endif -%}    
        {% else %}
        {%- if ac.ends[0].target == c.class -%}
        {{ac.class | lower}} = db.relationship('{{ac.class | lower}}', cascade="all, delete-orphan", back_populates='{{ac.ends[0].name}}'{%- if ac.ends[1].mult == '1' -%}, uselist=False{%- endif -%})
        {% if ac.ends[1].mult == '1' -%}
        @property
        def {{ac.ends[1].name}}(self):
            return self.{{ac.class | lower}}.{{ac.ends[1].name}} if self.{{ac.class | lower}} else None

        @{{ac.ends[1].name}}.setter
        def {{ac.ends[1].name}}(self, value):
            if self.{{ac.class | lower}}:
                self.{{ac.class | lower}}.{{ac.ends[1].name}} = value
            else:
                v = {{ac.class | lower}}({{ac.ends[0].name}}=self,{{ac.ends[1].name}}=value)
                db.session.add(v)

        {% else %}
        @property
        def {{ac.ends[1].name}}(self):    
            return {{c.class}}.{{ac.ends[1].name}}List(self, [x.{{ac.ends[1].name}} for x in self.{{ac.class | lower}}]) 
        {% endif %}
        {% endif -%}  
        {%- if ac.ends[1].target == c.class -%}
        {{ac.class | lower}} = db.relationship('{{ac.class | lower}}', cascade="all, delete-orphan", back_populates='{{ac.ends[1].name}}'{%- if ac.ends[0].mult == '1' -%}, uselist=False{%- endif -%})
        {% if ac.ends[0].mult == '1' -%}
        @property
        def {{ac.ends[0].name}}(self):
            return self.{{ac.class | lower}}.{{ac.ends[0].name}} if self.{{ac.class | lower}} else None

        @{{ac.ends[0].name}}.setter
        def {{ac.ends[0].name}}(self, value):
            if self.{{ac.class | lower}}:
                self.{{ac.class | lower}}.{{ac.ends[0].name}} = value
            else:
                v = {{ac.class | lower}}({{ac.ends[1].name}}=self,{{ac.ends[0].name}}=value)
                db.session.add(v)
        {% else %}
        @property
        def {{ac.ends[0].name}}(self):    
            return {{c.class}}.{{ac.ends[0].name}}List(self, [x.{{ac.ends[0].name}} for x in self.{{ac.class | lower}}]) 
        {% endif %}
        {% endif -%}    
        {% endif -%}  
        {% endfor %}
        {%- if isPersonalData(c,pm) -%}
        @property
        def owner(self):
            return self
        {% endif -%}
  
        @property
        def role(self):
            return self.roles[0]
        
        @role.setter
        def role(self,r):
            self.roles = [r]
        
        @property
        def is_authenticated(self):
            return True
        
        def __eq__(self, obj):
            return isinstance(obj,UserMixin) and self.id == obj.id 
        
        @classmethod
        def allInstances(cls):
            return cls.query.all() if hasattr(cls,'query') else super().allInstances()

        {% for m in c.methods %}
        @classmethod
        def {{m.name}}(cls, request):
            from project{% if not m.entry %}_aux{% endif %} import {{m.name}}
            return {{m.name}}(request)
        {% endfor %}

    # =========================
    # Entity Role
    # =========================
    class Role(db.Model,OCLTerm):
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)

        @staticmethod
        def getAuthenticatedRoles():
            return Role.query.filter(Role.name != UNAUTHENTICATED_ROLE).all()

        @classmethod
        def _get_role(cls, role_name):
            return cls.query.filter_by(name=role_name).first()
            
        {% for role in sm.roles -%}
        @classmethod
        @property
        def {{role.name}}(cls):
            return cls._get_role('{{role.name}}')

        {% endfor %}
    
        @classmethod
        def allInstances(cls):
            return cls.query.all() if hasattr(cls,'query') else super().allInstances()
        
    # =========================
    # Entity UserRoles
    # =========================
    class UserRoles(db.Model):
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey('{{- c.class | lower}}.id'), unique=True)
        role_id = db.Column(db.Integer(), db.ForeignKey('role.id'))

        @classmethod
        def allInstances(cls):
            return cls.query.all() if hasattr(cls,'query') else super().allInstances()
    
    {% else %}
    {%- if not c.isAssociation and not c.isEnum %}

    # =========================
    # Entity {{c.class}}
    # =========================
    @Secure({{projectname}}SecurityModel,{{projectname}}PrivacyModel)
    class {{c.class}}(db.Model,OCLTerm):
        
        # Association-end type classes
        {% for ac in dm if ac.isAssociation -%}
        {%- if ac.ends[0].target == c.class -%}
        class {{ac.ends[1].name}}List(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = {{ac.class | lower}}({{ac.ends[0].name}}=self._this,{{ac.ends[1].name}}=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = {{ac.class | lower}}.query.filter_by({{ac.ends[0].name}}=self._this,{{ac.ends[1].name}}=e).first()
                db.session.delete(v)
        {% endif -%} 
        {% if ac.ends[1].target == c.class -%} 
        class {{ac.ends[0].name}}List(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = {{ac.class | lower}}({{ac.ends[1].name}}=self._this,{{ac.ends[0].name}}=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = {{ac.class | lower}}.query.filter_by({{ac.ends[1].name}}=self._this,{{ac.ends[0].name}}=e).first()
                db.session.delete(v)
        {% endif -%}     
        {% endfor %}

        # Attributes
        id = db.Column(db.Integer, primary_key=True)
        {% for attr in c.attributes -%}
        {{attr.name}} = db.Column({{type(attr.type)}})
        {% endfor %}

        # Association ends
        {% for ac in dm if ac.isAssociation -%}
        {% if ac.ends[0].target == ac.ends[1].target %}
        {%- if ac.ends[0].target == c.class -%}
        {{ac.ends[1].name}} = db.relationship('{{- ac.ends[1].target}}',
                                 secondary='{{- ac.class | lower}}',
                                 primaryjoin=id=={{- ac.class | lower}}.{{- ac.ends[0].name | lower}}_id,
                                 secondaryjoin=id=={{- ac.class | lower}}.{{- ac.ends[1].name | lower}}_id,
                                 cascade="all, delete-orphan", 
                                 back_populates='{{- ac.ends[0].name}}')

        {% endif -%}  
        {%- if ac.ends[1].target == c.class -%}
        {{ac.ends[0].name}} = db.relationship('{{- ac.ends[0].target}}',
                                 secondary='{{- ac.class | lower}}',
                                 primaryjoin=id=={{- ac.class | lower}}.{{- ac.ends[1].name | lower}}_id,
                                 secondaryjoin=id=={{- ac.class | lower}}.{{- ac.ends[0].name | lower}}_id,
                                 cascade="all, delete-orphan", 
                                 back_populates='{{- ac.ends[1].name}}')
        {% endif -%}    
        {% else %}
        {%- if ac.ends[0].target == c.class -%}
        {{ac.class | lower}} = db.relationship('{{ac.class | lower}}', cascade="all, delete-orphan", back_populates='{{ac.ends[0].name}}'{%- if ac.ends[1].mult == '1' -%}, uselist=False{%- endif -%})
        @property
        def {{ac.ends[1].name}}(self):
            {% if ac.ends[1].mult == '1' -%}
            return self.{{ac.class | lower}}.{{ac.ends[1].name}} if self.{{ac.class | lower}} else None

        @{{ac.ends[1].name}}.setter
        def {{ac.ends[1].name}}(self, value):
            if self.{{ac.class | lower}}:
                self.{{ac.class | lower}}.{{ac.ends[1].name}} = value
            else:
                v = {{ac.class | lower}}({{ac.ends[0].name}}=self,{{ac.ends[1].name}}=value)
                db.session.add(v)
            {% else %}
            return {{c.class}}.{{ac.ends[1].name}}List(self, [x.{{ac.ends[1].name}} for x in self.{{ac.class | lower}}]) 
            {% endif %}
        {% endif -%}  
        {%- if ac.ends[1].target == c.class -%}
        {{ac.class | lower}} = db.relationship('{{ac.class | lower}}', cascade="all, delete-orphan", back_populates='{{ac.ends[1].name}}'{%- if ac.ends[0].mult == '1' -%}, uselist=False{%- endif -%})
        @property
        def {{ac.ends[0].name}}(self):
            {% if ac.ends[0].mult == '1' -%}
            return self.{{ac.class | lower}}.{{ac.ends[0].name}} if self.{{ac.class | lower}} else None

        @{{ac.ends[0].name}}.setter
        def {{ac.ends[0].name}}(self, value):
            if self.{{ac.class | lower}}:
                self.{{ac.class | lower}}.{{ac.ends[0].name}} = value
            else:
                v = {{ac.class | lower}}({{ac.ends[1].name}}=self,{{ac.ends[0].name}}=value)
                db.session.add(v)
            {% else %}
            return {{c.class}}.{{ac.ends[0].name}}List(self, [x.{{ac.ends[0].name}} for x in self.{{ac.class | lower}}]) 
            {% endif %}
        {% endif -%}    
        {% endif -%}    
        {% endfor %} 
        {%- if isPersonalData(c,pm) -%}
        owner_id = db.Column(db.Integer, db.ForeignKey('{{- sm.userClass | lower}}.id'))
        owner = db.relationship('{{- sm.userClass}}', foreign_keys=owner_id, backref='personal')
        def __init__(self, **kwargs):
            super({{c.class}}, self).__init__(**kwargs)
            if current_user.is_authenticated:
                self.owner=current_user
        {% endif %}
    
        @classmethod
        def allInstances(cls):
            return cls.query.all() if hasattr(cls,'query') else super().allInstances()

        {% for m in c.methods %}
        @classmethod
        def {{m.name}}(cls, request):
            from project{% if not m.entry %}_aux{% endif %} import {{m.name}}
            return {{m.name}}(request)
        {% endfor %}

    {% endif %}
    {% endif %}
    {% endfor %}

    # =========================
    # Entity Purpose
    # =========================
    class Purpose(db.Model,OCLTerm):
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)
        parent_id = db.Column(db.Integer, db.ForeignKey('purpose.id'))
        subpurposes = db.relationship('Purpose')

        def get_subpurposes_names(self):
            ret = []
            for sp in self.subpurposes:
                ret.append(sp.name)
                ret.extend(sp.get_subpurposes_names())  # Recursively get sub-purpose names
            return ret

        # consents = db.relationship('Consent', secondary=consentedpurposes, lazy='subquery',
        # back_populates='purposes')

        def __hash__(self):
            return hash(self.id)
        
        @classmethod
        def allInstances(cls):
            return cls.query.all() if hasattr(cls,'query') else super().allInstances()

    # =========================
    # Entity PersonalData
    # =========================
    class PersonalData(db.Model,OCLTerm):
        id = db.Column(db.Integer(), primary_key=True)
        resource = db.Column(db.String(100))
        subresource = db.Column(db.String(100))
        __table_args__ = (
            UniqueConstraint('resource', 'subresource', name='resource_subresource_uc'),
        )

        @classmethod
        def allInstances(cls):
            return cls.query.all() if hasattr(cls,'query') else super().allInstances()

    # =========================
    # Entity Consent
    # =========================
    class Consent(db.Model,OCLTerm):
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('{{- sm.userClass | lower}}.id'), nullable=False)
        user = db.relationship('{{- sm.userClass}}', foreign_keys=user_id, backref='consents')
        data_id = db.Column(db.Integer, db.ForeignKey('personal_data.id'), nullable=False)
        data = db.relationship('PersonalData', foreign_keys=data_id)
        purposes = db.relationship('Purpose', secondary=consentedpurposes, lazy='subquery')#, back_populates='consents')

        def __hash__(self):
            return hash(self.id)
        
        @classmethod
        def allInstances(cls):
            return cls.query.all() if hasattr(cls,'query') else super().allInstances()
        



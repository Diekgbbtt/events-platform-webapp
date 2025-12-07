# Copyright (c) 2025 All Rights Reserved
# Generated code

from application import app
from flask_user import UserMixin, current_user
from stm import EventPlatformNAGSecurityModel
from ptm import EventPlatformNAGPrivacyModel
from ocl.ocl import OCLTerm
from sqlalchemy import UniqueConstraint

# Initialize SQLAlchemy database instance
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Set up deletion interception for security and privacy models
from instrumentation import Secure, setup_deletion_interception
setup_deletion_interception(db.session,EventPlatformNAGSecurityModel,EventPlatformNAGPrivacyModel)

# =========================
# Role Constants
# =========================
UNAUTHENTICATED_ROLE = "VISITOR"
VISITOR = "VISITOR"
REGULARUSER = "REGULARUSER"
PREMIUMUSER = "PREMIUMUSER"
MODERATOR = "MODERATOR"
ADMIN = "ADMIN"



# =========================
# Purpose Constants
# =========================
RECOMMEND_EVENTS = "RECOMMEND_EVENTS"
CORE = "CORE"
FUNCTIONAL = "FUNCTIONAL"
ANALYTICS = "ANALYTICS"
STATS = "STATS"
INSIGHTS = "INSIGHTS"
TARGETED_MARKETING = "TARGETED_MARKETING"
MASS_MARKETING = "MASS_MARKETING"
MARKETING = "MARKETING"
ANY = "ANY"



with app.app_context():

    # =========================
    # Association between Consent and Purpose
    # =========================
    # Many-to-many relationship between Consent and Purpose
    consentedpurposes = db.Table('consentedpurposes',
            db.Column('consent_id', db.Integer, db.ForeignKey('consent.id'), nullable=False, primary_key=True),
            db.Column('purpose_id', db.Integer, db.ForeignKey('purpose.id'), nullable=False, primary_key=True)
    )
    # =========================
    # Association between Event and Person
    # =========================
    
    class association_events_owner(db.Model):
            
        id = db.Column(db.Integer, primary_key=True)
        events_id = db.Column(db.Integer(), db.ForeignKey('event.id'), unique=True)
        owner_id = db.Column(db.Integer(), db.ForeignKey('person.id'))
        events = db.relationship('Event', back_populates='association_events_owner', uselist=False)
        owner = db.relationship('Person', back_populates='association_events_owner', uselist=False)
    
    # =========================
    # Association between Event and Person
    # =========================
    
    class association_managedby_manages(db.Model):
            
        id = db.Column(db.Integer, primary_key=True)
        manages_id = db.Column(db.Integer(), db.ForeignKey('event.id'))
        managedBy_id = db.Column(db.Integer(), db.ForeignKey('person.id'))
        manages = db.relationship('Event', back_populates='association_managedby_manages', uselist=False)
        managedBy = db.relationship('Person', back_populates='association_managedby_manages', uselist=False)
    
    # =========================
    # Association between Event and Person
    # =========================
    
    class association_attendants_attends(db.Model):
            
        id = db.Column(db.Integer, primary_key=True)
        attends_id = db.Column(db.Integer(), db.ForeignKey('event.id'))
        attendants_id = db.Column(db.Integer(), db.ForeignKey('person.id'))
        attends = db.relationship('Event', back_populates='association_attendants_attends', uselist=False)
        attendants = db.relationship('Person', back_populates='association_attendants_attends', uselist=False)
    
    # =========================
    # Association between Category and Person
    # =========================
    
    class association_subscribers_subscriptions(db.Model):
            
        id = db.Column(db.Integer, primary_key=True)
        subscriptions_id = db.Column(db.Integer(), db.ForeignKey('category.id'))
        subscribers_id = db.Column(db.Integer(), db.ForeignKey('person.id'))
        subscriptions = db.relationship('Category', back_populates='association_subscribers_subscriptions', uselist=False)
        subscribers = db.relationship('Person', back_populates='association_subscribers_subscriptions', uselist=False)
    
    # =========================
    # Association between Category and Person
    # =========================
    
    class association_moderates_moderators(db.Model):
            
        id = db.Column(db.Integer, primary_key=True)
        moderates_id = db.Column(db.Integer(), db.ForeignKey('category.id'))
        moderators_id = db.Column(db.Integer(), db.ForeignKey('person.id'))
        moderates = db.relationship('Category', back_populates='association_moderates_moderators', uselist=False)
        moderators = db.relationship('Person', back_populates='association_moderates_moderators', uselist=False)
    
    # =========================
    # Association between Event and Person
    # =========================
    
    class association_requesters_requests(db.Model):
            
        id = db.Column(db.Integer, primary_key=True)
        requests_id = db.Column(db.Integer(), db.ForeignKey('event.id'))
        requesters_id = db.Column(db.Integer(), db.ForeignKey('person.id'))
        requests = db.relationship('Event', back_populates='association_requesters_requests', uselist=False)
        requesters = db.relationship('Person', back_populates='association_requesters_requests', uselist=False)
    
    # =========================
    # Association between Log and Person
    # =========================
    
    class association_logs_user(db.Model):
            
        id = db.Column(db.Integer, primary_key=True)
        logs_id = db.Column(db.Integer(), db.ForeignKey('log.id'), unique=True)
        user_id = db.Column(db.Integer(), db.ForeignKey('person.id'))
        logs = db.relationship('Log', back_populates='association_logs_user', uselist=False)
        user = db.relationship('Person', back_populates='association_logs_user', uselist=False)
    
    # =========================
    # Association between Invite and Person
    # =========================
    
    class association_invitations_invitee(db.Model):
            
        id = db.Column(db.Integer, primary_key=True)
        invitations_id = db.Column(db.Integer(), db.ForeignKey('invite.id'), unique=True)
        invitee_id = db.Column(db.Integer(), db.ForeignKey('person.id'))
        invitations = db.relationship('Invite', back_populates='association_invitations_invitee', uselist=False)
        invitee = db.relationship('Person', back_populates='association_invitations_invitee', uselist=False)
    
    # =========================
    # Association between Invite and Person
    # =========================
    
    class association_invitedby_invites(db.Model):
            
        id = db.Column(db.Integer, primary_key=True)
        invites_id = db.Column(db.Integer(), db.ForeignKey('invite.id'), unique=True)
        invitedBy_id = db.Column(db.Integer(), db.ForeignKey('person.id'))
        invites = db.relationship('Invite', back_populates='association_invitedby_invites', uselist=False)
        invitedBy = db.relationship('Person', back_populates='association_invitedby_invites', uselist=False)
    
    # =========================
    # Association between Category and Event
    # =========================
    
    class association_categories_events(db.Model):
            
        id = db.Column(db.Integer, primary_key=True)
        categories_id = db.Column(db.Integer(), db.ForeignKey('category.id'))
        events_id = db.Column(db.Integer(), db.ForeignKey('event.id'))
        categories = db.relationship('Category', back_populates='association_categories_events', uselist=False)
        events = db.relationship('Event', back_populates='association_categories_events', uselist=False)
    
    # =========================
    # Association between Log and Event
    # =========================
    
    class association_event_logs(db.Model):
            
        id = db.Column(db.Integer, primary_key=True)
        logs_id = db.Column(db.Integer(), db.ForeignKey('log.id'), unique=True)
        event_id = db.Column(db.Integer(), db.ForeignKey('event.id'))
        logs = db.relationship('Log', back_populates='association_event_logs', uselist=False)
        event = db.relationship('Event', back_populates='association_event_logs', uselist=False)
    
    # =========================
    # Association between Invite and Event
    # =========================
    
    class association_event_invitations(db.Model):
            
        id = db.Column(db.Integer, primary_key=True)
        invitations_id = db.Column(db.Integer(), db.ForeignKey('invite.id'), unique=True)
        event_id = db.Column(db.Integer(), db.ForeignKey('event.id'))
        invitations = db.relationship('Invite', back_populates='association_event_invitations', uselist=False)
        event = db.relationship('Event', back_populates='association_event_invitations', uselist=False)
    
    

    # ENTITIES
    
    # =========================
    # Entity Person (User class)
    # =========================
    @Secure(EventPlatformNAGSecurityModel,EventPlatformNAGPrivacyModel)
    class Person(db.Model,UserMixin,OCLTerm):

        #Association-end type classes
        class eventsList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_events_owner(owner=self._this,events=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_events_owner.query.filter_by(owner=self._this,events=e).first()
                db.session.delete(v)
        class managesList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_managedby_manages(managedBy=self._this,manages=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_managedby_manages.query.filter_by(managedBy=self._this,manages=e).first()
                db.session.delete(v)
        class attendsList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_attendants_attends(attendants=self._this,attends=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_attendants_attends.query.filter_by(attendants=self._this,attends=e).first()
                db.session.delete(v)
        class subscriptionsList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_subscribers_subscriptions(subscribers=self._this,subscriptions=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_subscribers_subscriptions.query.filter_by(subscribers=self._this,subscriptions=e).first()
                db.session.delete(v)
        class moderatesList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_moderates_moderators(moderators=self._this,moderates=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_moderates_moderators.query.filter_by(moderators=self._this,moderates=e).first()
                db.session.delete(v)
        class requestsList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_requesters_requests(requesters=self._this,requests=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_requesters_requests.query.filter_by(requesters=self._this,requests=e).first()
                db.session.delete(v)
        class logsList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_logs_user(user=self._this,logs=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_logs_user.query.filter_by(user=self._this,logs=e).first()
                db.session.delete(v)
        class invitationsList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_invitations_invitee(invitee=self._this,invitations=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_invitations_invitee.query.filter_by(invitee=self._this,invitations=e).first()
                db.session.delete(v)
        class invitesList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_invitedby_invites(invitedBy=self._this,invites=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_invitedby_invites.query.filter_by(invitedBy=self._this,invites=e).first()
                db.session.delete(v)
        

        #Attributes
        id = db.Column(db.Integer, primary_key=True)
        active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
        roles = db.relationship('Role', secondary='user_roles')
        username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False, server_default='')
        name = db.Column(db.String(100, collation="NOCASE"))
        surname = db.Column(db.String(100, collation="NOCASE"))
        gender = db.Column(db.String(100, collation="NOCASE"))
        email = db.Column(db.String(100, collation="NOCASE"))
        

        # Association ends
        association_events_owner = db.relationship('association_events_owner', cascade="all, delete-orphan", back_populates='owner')
        
        @property
        def events(self):    
            return Person.eventsList(self, [x.events for x in self.association_events_owner]) 
        
        association_managedby_manages = db.relationship('association_managedby_manages', cascade="all, delete-orphan", back_populates='managedBy')
        
        @property
        def manages(self):    
            return Person.managesList(self, [x.manages for x in self.association_managedby_manages]) 
        
        association_attendants_attends = db.relationship('association_attendants_attends', cascade="all, delete-orphan", back_populates='attendants')
        
        @property
        def attends(self):    
            return Person.attendsList(self, [x.attends for x in self.association_attendants_attends]) 
        
        association_subscribers_subscriptions = db.relationship('association_subscribers_subscriptions', cascade="all, delete-orphan", back_populates='subscribers')
        
        @property
        def subscriptions(self):    
            return Person.subscriptionsList(self, [x.subscriptions for x in self.association_subscribers_subscriptions]) 
        
        association_moderates_moderators = db.relationship('association_moderates_moderators', cascade="all, delete-orphan", back_populates='moderators')
        
        @property
        def moderates(self):    
            return Person.moderatesList(self, [x.moderates for x in self.association_moderates_moderators]) 
        
        association_requesters_requests = db.relationship('association_requesters_requests', cascade="all, delete-orphan", back_populates='requesters')
        
        @property
        def requests(self):    
            return Person.requestsList(self, [x.requests for x in self.association_requesters_requests]) 
        
        association_logs_user = db.relationship('association_logs_user', cascade="all, delete-orphan", back_populates='user')
        
        @property
        def logs(self):    
            return Person.logsList(self, [x.logs for x in self.association_logs_user]) 
        
        association_invitations_invitee = db.relationship('association_invitations_invitee', cascade="all, delete-orphan", back_populates='invitee')
        
        @property
        def invitations(self):    
            return Person.invitationsList(self, [x.invitations for x in self.association_invitations_invitee]) 
        
        association_invitedby_invites = db.relationship('association_invitedby_invites', cascade="all, delete-orphan", back_populates='invitedBy')
        
        @property
        def invites(self):    
            return Person.invitesList(self, [x.invites for x in self.association_invitedby_invites]) 
        
        @property
        def owner(self):
            return self
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

        
        @classmethod
        def users(cls, request):
            from project import users
            return users(request)
        
        @classmethod
        def user(cls, request):
            from project import user
            return user(request)
        
        @classmethod
        def profile(cls, request):
            from project import profile
            return profile(request)
        
        @classmethod
        def update_user(cls, request):
            from project import update_user
            return update_user(request)
        
        @classmethod
        def join(cls, request):
            from project import join
            return join(request)
        
        @classmethod
        def leave(cls, request):
            from project import leave
            return leave(request)
        
        @classmethod
        def add_moderator(cls, request):
            from project import add_moderator
            return add_moderator(request)
        
        @classmethod
        def remove_moderator(cls, request):
            from project import remove_moderator
            return remove_moderator(request)
        
        @classmethod
        def subscribe(cls, request):
            from project import subscribe
            return subscribe(request)
        
        @classmethod
        def unsubscribe(cls, request):
            from project import unsubscribe
            return unsubscribe(request)
        
        @classmethod
        def recommend_events(cls, request):
            from project_aux import recommend_events
            return recommend_events(request)
        
        @classmethod
        def send_advertisement_to_user(cls, request):
            from project_aux import send_advertisement_to_user
            return send_advertisement_to_user(request)
        
        @classmethod
        def personalized_stats(cls, request):
            from project import personalized_stats
            return personalized_stats(request)
        

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
            
        @classmethod
        @property
        def VISITOR(cls):
            return cls._get_role('VISITOR')

        @classmethod
        @property
        def REGULARUSER(cls):
            return cls._get_role('REGULARUSER')

        @classmethod
        @property
        def PREMIUMUSER(cls):
            return cls._get_role('PREMIUMUSER')

        @classmethod
        @property
        def MODERATOR(cls):
            return cls._get_role('MODERATOR')

        @classmethod
        @property
        def ADMIN(cls):
            return cls._get_role('ADMIN')

        
    
        @classmethod
        def allInstances(cls):
            return cls.query.all() if hasattr(cls,'query') else super().allInstances()
        
    # =========================
    # Entity UserRoles
    # =========================
    class UserRoles(db.Model):
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey('person.id'), unique=True)
        role_id = db.Column(db.Integer(), db.ForeignKey('role.id'))

        @classmethod
        def allInstances(cls):
            return cls.query.all() if hasattr(cls,'query') else super().allInstances()
    
    
    

    # =========================
    # Entity Event
    # =========================
    @Secure(EventPlatformNAGSecurityModel,EventPlatformNAGPrivacyModel)
    class Event(db.Model,OCLTerm):
        
        # Association-end type classes
        class ownerList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_events_owner(events=self._this,owner=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_events_owner.query.filter_by(events=self._this,owner=e).first()
                db.session.delete(v)
        class managedByList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_managedby_manages(manages=self._this,managedBy=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_managedby_manages.query.filter_by(manages=self._this,managedBy=e).first()
                db.session.delete(v)
        class attendantsList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_attendants_attends(attends=self._this,attendants=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_attendants_attends.query.filter_by(attends=self._this,attendants=e).first()
                db.session.delete(v)
        class requestersList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_requesters_requests(requests=self._this,requesters=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_requesters_requests.query.filter_by(requests=self._this,requesters=e).first()
                db.session.delete(v)
        class categoriesList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_categories_events(events=self._this,categories=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_categories_events.query.filter_by(events=self._this,categories=e).first()
                db.session.delete(v)
        class logsList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_event_logs(event=self._this,logs=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_event_logs.query.filter_by(event=self._this,logs=e).first()
                db.session.delete(v)
        class invitationsList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_event_invitations(event=self._this,invitations=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_event_invitations.query.filter_by(event=self._this,invitations=e).first()
                db.session.delete(v)
        

        # Attributes
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(100, collation="NOCASE"))
        description = db.Column(db.String(100, collation="NOCASE"))
        

        # Association ends
        association_events_owner = db.relationship('association_events_owner', cascade="all, delete-orphan", back_populates='events', uselist=False)
        @property
        def owner(self):
            return self.association_events_owner.owner if self.association_events_owner else None

        @owner.setter
        def owner(self, value):
            if self.association_events_owner:
                self.association_events_owner.owner = value
            else:
                v = association_events_owner(events=self,owner=value)
                db.session.add(v)
            
        association_managedby_manages = db.relationship('association_managedby_manages', cascade="all, delete-orphan", back_populates='manages')
        @property
        def managedBy(self):
            
            return Event.managedByList(self, [x.managedBy for x in self.association_managedby_manages]) 
            
        association_attendants_attends = db.relationship('association_attendants_attends', cascade="all, delete-orphan", back_populates='attends')
        @property
        def attendants(self):
            
            return Event.attendantsList(self, [x.attendants for x in self.association_attendants_attends]) 
            
        association_requesters_requests = db.relationship('association_requesters_requests', cascade="all, delete-orphan", back_populates='requests')
        @property
        def requesters(self):
            
            return Event.requestersList(self, [x.requesters for x in self.association_requesters_requests]) 
            
        association_categories_events = db.relationship('association_categories_events', cascade="all, delete-orphan", back_populates='events')
        @property
        def categories(self):
            
            return Event.categoriesList(self, [x.categories for x in self.association_categories_events]) 
            
        association_event_logs = db.relationship('association_event_logs', cascade="all, delete-orphan", back_populates='event')
        @property
        def logs(self):
            
            return Event.logsList(self, [x.logs for x in self.association_event_logs]) 
            
        association_event_invitations = db.relationship('association_event_invitations', cascade="all, delete-orphan", back_populates='event')
        @property
        def invitations(self):
            
            return Event.invitationsList(self, [x.invitations for x in self.association_event_invitations]) 
            
        
    
        @classmethod
        def allInstances(cls):
            return cls.query.all() if hasattr(cls,'query') else super().allInstances()

        
        @classmethod
        def events(cls, request):
            from project import events
            return events(request)
        
        @classmethod
        def create_event(cls, request):
            from project import create_event
            return create_event(request)
        
        @classmethod
        def view_event(cls, request):
            from project import view_event
            return view_event(request)
        
        @classmethod
        def edit_event(cls, request):
            from project import edit_event
            return edit_event(request)
        
        @classmethod
        def update_event(cls, request):
            from project import update_event
            return update_event(request)
        
        @classmethod
        def manage_event(cls, request):
            from project import manage_event
            return manage_event(request)
        
        @classmethod
        def remove_category(cls, request):
            from project import remove_category
            return remove_category(request)
        
        @classmethod
        def promote_manager(cls, request):
            from project import promote_manager
            return promote_manager(request)
        
        @classmethod
        def demote_manager(cls, request):
            from project import demote_manager
            return demote_manager(request)
        
        @classmethod
        def remove_attendee(cls, request):
            from project import remove_attendee
            return remove_attendee(request)
        
        @classmethod
        def accept_request(cls, request):
            from project import accept_request
            return accept_request(request)
        
        @classmethod
        def reject_request(cls, request):
            from project import reject_request
            return reject_request(request)
        
        @classmethod
        def analyze(cls, request):
            from project import analyze
            return analyze(request)
        

    
    
    

    # =========================
    # Entity Category
    # =========================
    @Secure(EventPlatformNAGSecurityModel,EventPlatformNAGPrivacyModel)
    class Category(db.Model,OCLTerm):
        
        # Association-end type classes
        class subscribersList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_subscribers_subscriptions(subscriptions=self._this,subscribers=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_subscribers_subscriptions.query.filter_by(subscriptions=self._this,subscribers=e).first()
                db.session.delete(v)
        class moderatorsList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_moderates_moderators(moderates=self._this,moderators=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_moderates_moderators.query.filter_by(moderates=self._this,moderators=e).first()
                db.session.delete(v)
        class eventsList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_categories_events(categories=self._this,events=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_categories_events.query.filter_by(categories=self._this,events=e).first()
                db.session.delete(v)
        

        # Attributes
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100, collation="NOCASE"))
        

        # Association ends
        association_subscribers_subscriptions = db.relationship('association_subscribers_subscriptions', cascade="all, delete-orphan", back_populates='subscriptions')
        @property
        def subscribers(self):
            
            return Category.subscribersList(self, [x.subscribers for x in self.association_subscribers_subscriptions]) 
            
        association_moderates_moderators = db.relationship('association_moderates_moderators', cascade="all, delete-orphan", back_populates='moderates')
        @property
        def moderators(self):
            
            return Category.moderatorsList(self, [x.moderators for x in self.association_moderates_moderators]) 
            
        association_categories_events = db.relationship('association_categories_events', cascade="all, delete-orphan", back_populates='categories')
        @property
        def events(self):
            
            return Category.eventsList(self, [x.events for x in self.association_categories_events]) 
            
        
    
        @classmethod
        def allInstances(cls):
            return cls.query.all() if hasattr(cls,'query') else super().allInstances()

        
        @classmethod
        def categories(cls, request):
            from project import categories
            return categories(request)
        
        @classmethod
        def create_category(cls, request):
            from project import create_category
            return create_category(request)
        
        @classmethod
        def view_category(cls, request):
            from project import view_category
            return view_category(request)
        
        @classmethod
        def edit_category(cls, request):
            from project import edit_category
            return edit_category(request)
        
        @classmethod
        def update_category(cls, request):
            from project import update_category
            return update_category(request)
        
        @classmethod
        def send_mass_advertisement(cls, request):
            from project import send_mass_advertisement
            return send_mass_advertisement(request)
        
        @classmethod
        def get_candidates(cls, request):
            from project_aux import get_candidates
            return get_candidates(request)
        

    
    
    

    # =========================
    # Entity Ad
    # =========================
    @Secure(EventPlatformNAGSecurityModel,EventPlatformNAGPrivacyModel)
    class Ad(db.Model,OCLTerm):
        
        # Association-end type classes
        

        # Attributes
        id = db.Column(db.Integer, primary_key=True)
        content = db.Column(db.String(100, collation="NOCASE"))
        

        # Association ends
        
    
        @classmethod
        def allInstances(cls):
            return cls.query.all() if hasattr(cls,'query') else super().allInstances()

        
        @classmethod
        def ads(cls, request):
            from project import ads
            return ads(request)
        
        @classmethod
        def create_ad(cls, request):
            from project import create_ad
            return create_ad(request)
        
        @classmethod
        def remove_ad(cls, request):
            from project import remove_ad
            return remove_ad(request)
        
        @classmethod
        def get_personalize_ad(cls, request):
            from project_aux import get_personalize_ad
            return get_personalize_ad(request)
        

    
    
    

    # =========================
    # Entity Log
    # =========================
    @Secure(EventPlatformNAGSecurityModel,EventPlatformNAGPrivacyModel)
    class Log(db.Model,OCLTerm):
        
        # Association-end type classes
        class userList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_logs_user(logs=self._this,user=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_logs_user.query.filter_by(logs=self._this,user=e).first()
                db.session.delete(v)
        class eventList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_event_logs(logs=self._this,event=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_event_logs.query.filter_by(logs=self._this,event=e).first()
                db.session.delete(v)
        

        # Attributes
        id = db.Column(db.Integer, primary_key=True)
        timestamp = db.Column(db.Integer)
        

        # Association ends
        association_logs_user = db.relationship('association_logs_user', cascade="all, delete-orphan", back_populates='logs', uselist=False)
        @property
        def user(self):
            return self.association_logs_user.user if self.association_logs_user else None

        @user.setter
        def user(self, value):
            if self.association_logs_user:
                self.association_logs_user.user = value
            else:
                v = association_logs_user(logs=self,user=value)
                db.session.add(v)
            
        association_event_logs = db.relationship('association_event_logs', cascade="all, delete-orphan", back_populates='logs', uselist=False)
        @property
        def event(self):
            return self.association_event_logs.event if self.association_event_logs else None

        @event.setter
        def event(self, value):
            if self.association_event_logs:
                self.association_event_logs.event = value
            else:
                v = association_event_logs(logs=self,event=value)
                db.session.add(v)
            
        owner_id = db.Column(db.Integer, db.ForeignKey('person.id'))
        owner = db.relationship('Person', foreign_keys=owner_id, backref='personal')
        def __init__(self, **kwargs):
            super(Log, self).__init__(**kwargs)
            if current_user.is_authenticated:
                self.owner=current_user
        
    
        @classmethod
        def allInstances(cls):
            return cls.query.all() if hasattr(cls,'query') else super().allInstances()

        
        @classmethod
        def logs(cls, request):
            from project import logs
            return logs(request)
        

    
    
    

    # =========================
    # Entity Invite
    # =========================
    @Secure(EventPlatformNAGSecurityModel,EventPlatformNAGPrivacyModel)
    class Invite(db.Model,OCLTerm):
        
        # Association-end type classes
        class inviteeList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_invitations_invitee(invitations=self._this,invitee=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_invitations_invitee.query.filter_by(invitations=self._this,invitee=e).first()
                db.session.delete(v)
        class invitedByList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_invitedby_invites(invites=self._this,invitedBy=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_invitedby_invites.query.filter_by(invites=self._this,invitedBy=e).first()
                db.session.delete(v)
        class eventList(list):
            
            def __init__(self,this):
                self._this = this
                super().__init__()
            
            def __init__(self,this, __iterable):
                self._this = this
                super().__init__(__iterable)
            
            def append(self,e):
                v = association_event_invitations(invitations=self._this,event=e)
                db.session.add(v)
                super().append(e)
            
            def remove(self,e):
                super().remove(e)
                v = association_event_invitations.query.filter_by(invitations=self._this,event=e).first()
                db.session.delete(v)
        

        # Attributes
        id = db.Column(db.Integer, primary_key=True)
        

        # Association ends
        association_invitations_invitee = db.relationship('association_invitations_invitee', cascade="all, delete-orphan", back_populates='invitations', uselist=False)
        @property
        def invitee(self):
            return self.association_invitations_invitee.invitee if self.association_invitations_invitee else None

        @invitee.setter
        def invitee(self, value):
            if self.association_invitations_invitee:
                self.association_invitations_invitee.invitee = value
            else:
                v = association_invitations_invitee(invitations=self,invitee=value)
                db.session.add(v)
            
        association_invitedby_invites = db.relationship('association_invitedby_invites', cascade="all, delete-orphan", back_populates='invites', uselist=False)
        @property
        def invitedBy(self):
            return self.association_invitedby_invites.invitedBy if self.association_invitedby_invites else None

        @invitedBy.setter
        def invitedBy(self, value):
            if self.association_invitedby_invites:
                self.association_invitedby_invites.invitedBy = value
            else:
                v = association_invitedby_invites(invites=self,invitedBy=value)
                db.session.add(v)
            
        association_event_invitations = db.relationship('association_event_invitations', cascade="all, delete-orphan", back_populates='invitations', uselist=False)
        @property
        def event(self):
            return self.association_event_invitations.event if self.association_event_invitations else None

        @event.setter
        def event(self, value):
            if self.association_event_invitations:
                self.association_event_invitations.event = value
            else:
                v = association_event_invitations(invitations=self,event=value)
                db.session.add(v)
            
        
    
        @classmethod
        def allInstances(cls):
            return cls.query.all() if hasattr(cls,'query') else super().allInstances()

        
        @classmethod
        def send_invite(cls, request):
            from project import send_invite
            return send_invite(request)
        
        @classmethod
        def accept_invitation(cls, request):
            from project import accept_invitation
            return accept_invitation(request)
        
        @classmethod
        def decline_invitation(cls, request):
            from project import decline_invitation
            return decline_invitation(request)
        

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

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
        user_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
        user = db.relationship('Person', foreign_keys=user_id, backref='consents')
        data_id = db.Column(db.Integer, db.ForeignKey('personal_data.id'), nullable=False)
        data = db.relationship('PersonalData', foreign_keys=data_id)
        purposes = db.relationship('Purpose', secondary=consentedpurposes, lazy='subquery')#, back_populates='consents')

        def __hash__(self):
            return hash(self.id)
        
        @classmethod
        def allInstances(cls):
            return cls.query.all() if hasattr(cls,'query') else super().allInstances()
        


from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin

db = SQLAlchemy()

# VISITOR = "VISITOR" # corresponds to current_user.is_authenticated == False
REGULARUSER = "REGULARUSER"
PREMIUMUSER = "PREMIUMUSER"
MODERATOR = "MODERATOR"
ADMIN = "ADMIN"
# AUTH and SYSTEM roles are not needed explicitly

AnyPurpose = "Any"
FunctionalPurpose = "Functional"
MarketingPurpose = "Marketing"
CorePurpose = "Core"
RecommendEventsPurpose = "RecommendEvents"
TargetedMarketingPurpose = "TargetedMarketing"
MassMarketingPurpose = "MassMarketing"
AnalyticsPurpose = "Analytics"
InsightsPurpose = "Insights"
StatsPurpose = "Stats"

# Associations
mods = db.Table('mods',
        db.Column('category_id', db.Integer, db.ForeignKey('category.id'), nullable=False),
        db.Column('person_id', db.Integer, db.ForeignKey('person.id'), nullable=False)
)

subs = db.Table('subs',
        db.Column('category_id', db.Integer, db.ForeignKey('category.id'), nullable=False),
        db.Column('person_id', db.Integer, db.ForeignKey('person.id'), nullable=False)
)

evts = db.Table('evts',
        db.Column('event_id', db.Integer, db.ForeignKey('event.id'), nullable=False),
        db.Column('category_id', db.Integer, db.ForeignKey('category.id'), nullable=False)
)

atts = db.Table('atts',
        db.Column('person_id', db.Integer, db.ForeignKey('person.id'), nullable=False),
        db.Column('event_id', db.Integer, db.ForeignKey('event.id'), nullable=False)
)

mans = db.Table('mans',
        db.Column('person_id', db.Integer, db.ForeignKey('person.id'), nullable=False),
        db.Column('event_id', db.Integer, db.ForeignKey('event.id'), nullable=False)
)

reqs = db.Table('reqs',
        db.Column('person_id', db.Integer, db.ForeignKey('person.id'), nullable=False),
        db.Column('event_id', db.Integer, db.ForeignKey('event.id'), nullable=False)
)

pgroup = db.Table('pgroup',
        db.Column('pparent_id', db.Integer, db.ForeignKey('purpose.id'), nullable=False),
        db.Column('purpose_id', db.Integer, db.ForeignKey('purpose.id'), nullable=False)
)

# Entities
class Person(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    roles = db.relationship('Role', secondary='user_roles')
    
    name = db.Column(db.String(100, collation='NOCASE'))
    surname = db.Column(db.String(100, collation='NOCASE'))
    username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    
    gender = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)

    events = db.relationship('Event', backref='owner')
    manages = db.relationship('Event', secondary=mans, lazy='subquery', backref='managedBy')
    attends = db.relationship('Event', secondary=atts, lazy='subquery', backref='attendants')
    requests = db.relationship('Event', secondary=reqs, lazy='subquery', backref='requesters')

    @property
    def role(self):
        return self.roles[0]
    @role.setter
    def role(self,r):
        self.roles = [r]
    @property
    def is_authenticated(self):
        return True


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('person.id'), unique=True)
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id'))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    description = db.Column(db.String(2000))

    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    subscribers = db.relationship('Person', secondary=subs, lazy='subquery',
                                  backref=db.backref('subscriptions', lazy=True))
    moderators = db.relationship('Person', secondary=mods, lazy='subquery',
                                 backref=db.backref('moderates', lazy=True))
    events = db.relationship('Event', secondary=evts, lazy='subquery',
                             backref=db.backref('categories', lazy=True))

class Purpose(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    
    parent_id = db.Column(db.Integer, db.ForeignKey('purpose.id'), nullable=True)    
    parent = db.relationship('Purpose', remote_side=[id], backref='children', lazy=True)


class Consent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classname = db.Column(db.String(100))
    propertyname = db.Column(db.String(100))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    purpose_id = db.Column(db.Integer, db.ForeignKey('purpose.id'), nullable=False)
    
    user = db.relationship('Person', backref='consents', lazy=True)
    purpose = db.relationship('Purpose', backref='consents', lazy=True)

class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100))

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=True)
    user = db.relationship('Person', foreign_keys=user_id, backref='logs')
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=True)
    event = db.relationship('Event', foreign_keys=event_id, backref='logs')

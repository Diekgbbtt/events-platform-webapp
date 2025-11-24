from email import message
from flask import Flask, render_template, request, redirect, url_for
from enum import Enum, auto
from flask_sqlalchemy import SQLAlchemy
from flask_user import current_user, login_required, UserManager, UserMixin
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['USER_APP_NAME'] = "Thoughts app"
app.config['USER_ENABLE_EMAIL'] = False      
app.config['USER_ENABLE_USERNAME'] = True    
app.config['USER_REQUIRE_RETYPE_PASSWORD'] = False
app.config['SECRET_KEY'] = '_5#yfasQ8sansaxec/][#1'

db = SQLAlchemy(app)

class Role(Enum):
    USER = auto()
    OTHER = auto()

class Purpose(Enum):
    ADD_NEW_THOUGHTS = auto()

class PersonalData(Enum):
    PERSON_CREATED = auto()

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    thought_id = db.Column(db.Integer, db.ForeignKey('thought.id'))

class Person(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

    myRole = db.Column(db.Enum(Role),default=Role.USER)
    created = db.relationship('Thought', backref='createdBy')
    voted = db.relationship('Vote', backref='voter')

    def isUser(self):
        return self.myRole == Role.USER

class Thought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    votedBy = db.relationship('Vote', backref='votee')

class Consent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    personalData = db.Column(db.Enum(PersonalData), nullable=False)
    purpose = db.Column(db.Enum(Purpose), nullable=False)

with app.app_context():
    db.create_all()

user_manager = UserManager(app, db, Person)

# Authorization features
class SecurityException(Exception):
    def __init__(self, msg):
        self.msg = msg

def check_user(caller):
    # cannot access the page if not a User
    if not caller.isUser():
        raise SecurityException("You are not allowed to access this page: Not a User")

def grant_consent(person, personal_data, purpose):
    existing = Consent.query.filter_by(
        person_id=person.id,
        personalData=personal_data,
        purpose=purpose
    ).first()
    if not existing:
        consent = Consent(
            person_id=person.id,
            personalData=personal_data,
            purpose=purpose
        )
        db.session.add(consent)
        db.session.commit()

def revoke_consent(person, personal_data, purpose):
    consent = Consent.query.filter_by(
        person_id=person.id,
        personalData=personal_data,
        purpose=purpose
    ).first()
    if consent:
        db.session.delete(consent)
        db.session.commit()

def has_consent(person, personal_data, purpose):
    return Consent.query.filter_by(
        person_id=person.id,
        personalData=personal_data,
        purpose=purpose
    ).first() is not None

@app.route('/')
def index():
    thoughts=Thought.query.all()
    return render_template('index.html', table=thoughts)

def check_creation_consent(caller):
    if not has_consent(caller, PersonalData.PERSON_CREATED, Purpose.ADD_NEW_THOUGHTS):
        raise SecurityException("You are not allowed to add new thoughts: No consent")
               
@app.route('/add_thought', methods=['POST'])
@login_required
def add_thought():
    try: 
        check_user(current_user)
        content = request.form["thought"]
        if content != "":
            t = Thought(content=content)
            check_creation_consent(current_user)
            t.createdBy = current_user
            db.session.add(t)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            thoughts = Thought.query.all()
            return render_template('index.html', table=thoughts, invalid_input=True)
    except SecurityException as se:
        thoughts = Thought.query.all()
        return render_template('index.html', table=thoughts, security_violation=True,message=se.msg)

def check_delete(self,caller):
    if self.createdBy.id != caller.id:
        raise SecurityException("You are not allowed to delete this thought: Not own thought")

@app.route('/delete_thought')
@login_required
def delete_thought():
    id = request.args["id"]
    try: 
        i = int(id)
        t = Thought.query.get(i)
        if t != None:
            try:
                check_delete(t,current_user)
                db.session.delete(t)
                db.session.commit()
            except SecurityException as se:
                thoughts = Thought.query.all()
                return render_template('index.html', table=thoughts, security_violation=True,message=se.msg)
        return redirect(url_for('index'))
    except:
        return redirect(url_for('index'))



def check_vote(self,caller):
    if self.createdBy.id==caller.id:
        raise SecurityException("You are not allowed to vote for this thought: Own thought")
    if len([x for x in caller.voted if x.votee==self]) >= 3:
        raise SecurityException("You are not allowed to vote for this thought: Too many votes")


@app.route('/vote_thought')
@login_required
def vote_thought():
    id = request.args["id"]
    try: 
        i = int(id)
        t = Thought.query.get(i)
        c = current_user
        if t != None and c != None:
            try:
                check_vote(t,c)
                v = Vote(voter=c, votee=t)
                db.session.add(v)
                db.session.commit()
                return redirect(url_for('index'))
            except SecurityException as se:
                thoughts = Thought.query.all()
                return render_template('index.html', table=thoughts, security_violation=True,message=se.msg)          
    except:
        return redirect(url_for('index'))

@app.route('/policy', methods=['GET', 'POST'])
@login_required
def policy():
    if request.method == 'POST':
        create_consent = request.form.get('create_consent') == 'on'
        if create_consent:
            grant_consent(current_user, PersonalData.PERSON_CREATED, Purpose.ADD_NEW_THOUGHTS)
        else:
            revoke_consent(current_user, PersonalData.PERSON_CREATED, Purpose.ADD_NEW_THOUGHTS)
        return redirect(url_for('policy'))
    return render_template('policy.html', 
                         PersonalData=PersonalData,
                         Purpose=Purpose,
                         has_consent=has_consent)



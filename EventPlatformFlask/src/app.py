from flask import Flask, render_template, redirect, url_for, Response, request, jsonify
from flask_user import UserManager, user_registered, user_logged_in, current_user
from model import db, Person, Role, Purpose, REGULARUSER, PREMIUMUSER, MODERATOR, ADMIN, Consent, Ad, AnyPurpose, FunctionalPurpose, MarketingPurpose, AnalyticsPurpose, CorePurpose, RecommendEventsPurpose, TargetedMarketingPurpose, MassMarketingPurpose, InsightsPurpose, StatsPurpose
from project import PrivacyException, init
from cedar.authz import SecurityException

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['USER_APP_NAME'] = "Event Platform"
app.config['USER_ENABLE_EMAIL'] = False      
app.config['USER_ENABLE_USERNAME'] = True    
app.config['USER_REQUIRE_RETYPE_PASSWORD'] = False
app.config['SECRET_KEY'] = '2fed4086df4c5dd5d4c3aae4cc90ed53318f8844d450952639caae96ebe41339'
app.config['USER_UNAUTHORIZED_ENDPOINT'] = 'sec-error'
app.config['PURPOSE_LIMITATION_AND_CONSENT_VIOLATION_ENDPOINT'] = 'priv-error'

PURPOSES = [
    AnyPurpose,
    MarketingPurpose,
    TargetedMarketingPurpose,
    MassMarketingPurpose,
    AnalyticsPurpose,
    FunctionalPurpose,
    RecommendEventsPurpose,
    CorePurpose
]

ROLES = [
    REGULARUSER,
    PREMIUMUSER,
    MODERATOR,
    ADMIN
]

@app.route('/sec-error')
def sec_error():
    msg = "You are not allowed to access this page."
    return render_template('sec_error.html', message = msg)

@app.route('/priv-error')
def priv_error():
    msg = "Access denied due to privacy restrictions."
    return render_template('priv_error.html', message = msg)

@user_registered.connect_via(app)
def after_user_registered_hook(sender, user, **extra):
    role = Role.query.filter_by(name=REGULARUSER).one()
    user.role=role 
    db.session.commit()

db.init_app(app)

with app.app_context():
    db.create_all()
    roles = Role.query.all()
    if len(roles) == 0:
        for name in ROLES:
            db.session.add(Role(name=name))
        db.session.commit()

    purposes = Purpose.query.all()
    if len(purposes) == 0:
        for iPurpose, name in enumerate(PURPOSES):
            db.session.add(Purpose(id=iPurpose+1, name=name))
        db.session.commit()

user_manager = UserManager(app, db, Person)

init()

def secure(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SecurityException as se:
            db.session.rollback()
            return render_template(se.page, security_violation = True, se_msg = se.msg, **se.params)
        except PrivacyException as pe:
            db.session.rollback()
            return render_template(pe.page, privacy_violation = True, priv_msg = pe.msg, **pe.params)
    wrapper.__name__ = func.__name__
    return wrapper

@app.route('/')
@secure
def main():
    from project import main 
    result=main()
    if type(result) == Response:
        return result
    else: 
        return render_template('main.html', **result)
        
@app.route('/profile')
@secure
def profile():
    from project import profile 
    result=profile()
    if type(result) == Response:
        return result
    else: 
        return render_template('profile.html', **result)
        
@app.route('/events')
@secure
def events():
    from project import events 
    result=events()
    if type(result) == Response:
        return result
    else: 
        return render_template('events.html', **result)

@app.route('/ads')
@secure
def ads():
    from project import ads 
    result=ads()
    if type(result) == Response:
        return result
    else: 
        return render_template('ads.html', **result)

@app.route('/view_event/<int:id>')
@secure
def view_event(id):
    from project import view_event 
    result=view_event(id)
    if type(result) == Response:
        return result
    else: 
        return render_template('view_event.html', **result)

@app.route('/edit_event/<int:id>')
@secure
def edit_event(id):
    from project import edit_event 
    result=edit_event(id)
    if type(result) == Response:
        return result
    else: 
        return render_template('edit_event.html', **result)

@app.post('/update_event')
@secure
def update_event():
    from project import update_event 
    result=update_event()
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('edit_event',id=result))

@app.route('/join/<int:id>')
@secure
def join(id):
    from project import join 
    result=join(id)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('events'))

@app.route('/leave/<int:id>')
@secure
def leave(id):
    from project import leave 
    result=leave(id)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('profile'))

@app.route('/analyze/<int:id>')
@secure
def analyze(id):
    from project import analyze 
    result=analyze(id)
    if type(result) == Response:
        return result
    else: 
        return render_template('analyze.html', **result)

@app.post('/create_event')
@secure
def create_event():
    from project import create_event 
    result=create_event()
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('events'))

@app.post('/create_ad')
@secure
def create_ad():
    from project import create_ad 
    result=create_ad()
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('ads'))

@app.route('/manage_event/<int:id>')
@secure
def manage_event(id):
    from project import manage_event 
    result=manage_event(id)
    if type(result) == Response:
        return result
    else: 
        return render_template('manage_event.html', **result)

@app.route('/categories')
@secure
def categories():
    from project import categories 
    result=categories()
    if type(result) == Response:
        return result
    else: 
        return render_template('categories.html', **result)

@app.route('/view_category/<int:id>')
@secure
def view_category(id):
    from project import view_category 
    result=view_category(id)
    if type(result) == Response:
        return result
    else: 
        return render_template('view_category.html', **result)

@app.route('/remove_category/<int:id>/<int:c>')
@secure
def remove_category(id,c):
    from project import remove_category 
    result=remove_category(id,c)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('view_category',id=result))

@app.route('/remove_ad/<int:id>')
@secure
def remove_ad(id):
    from project import remove_ad 
    result=remove_ad(id)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('ads'))

@app.route('/edit_category/<int:id>')
@secure
def edit_category(id):
    from project import edit_category 
    result=edit_category(id)
    if type(result) == Response:
        return result
    else: 
        return render_template('edit_category.html', **result)

@app.route('/add_moderator/<int:id>/<int:c>')
@secure
def add_moderator(id,c):
    from project import add_moderator 
    result=add_moderator(id,c)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('edit_category',id=c))

@app.route('/remove_moderator/<int:id>/<int:c>')
@secure
def remove_moderator(id,c):
    from project import remove_moderator 
    result=remove_moderator(id,c)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('edit_category',id=c))

@app.post('/update_category')
@secure
def update_category():
    from project import update_category 
    result=update_category()
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('edit_category',id=result))
    
@app.route('/subscribe/<int:id>')
@secure
def subscribe(id):
    from project import subscribe 
    result=subscribe(id)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('categories'))

@app.route('/send_mass_advertisement/<int:id>')
@secure
def send_mass_advertisement(id):
    from project import send_mass_advertisement 
    result=send_mass_advertisement(id)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('categories'))

@app.route('/unsubscribe/<int:id>')
@secure
def unsubscribe(id):
    from project import unsubscribe 
    result=unsubscribe(id)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('profile'))

@app.post('/create_category')
@secure
def create_category():
    from project import create_category 
    result=create_category()
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('categories'))

@app.route('/users')
@secure
def users():
    from project import users
    result=users()
    if type(result) == Response:
        return result
    else: 
        return render_template('users.html', **result) 
        
@app.route('/user/<int:id>')
@secure
def user(id):
    from project import user 
    result=user(id)
    if type(result) == Response:
        return result
    else: 
        return render_template('user.html', **result) 
        
@app.post('/update_user')
@secure
def update_user():
    from project import update_user 
    result=update_user()
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('user',id=result))

@app.route('/promote_manager/<int:id>/<int:e>')
@secure
def promote_manager(id,e):
    from project import promote_manager 
    result=promote_manager(id,e)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('manage_event',id=result))

@app.route('/demote_manager/<int:id>/<int:e>')
@secure
def demote_manager(id,e):
    from project import demote_manager 
    result=demote_manager(id,e)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('manage_event',id=result))

@app.route('/remove_attendee/<int:id>/<int:e>')
@secure
def remove_attendee(id,e):
    from project import remove_attendee 
    result=remove_attendee(id,e)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('manage_event',id=result))

@app.route('/accept_request/<int:id>/<int:e>')
@secure
def accept_request(id,e):
    from project import accept_request 
    result=accept_request(id,e)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('manage_event',id=result))


@app.route('/reject_request/<int:id>/<int:e>')
@secure
def reject_request(id,e):
    from project import reject_request 
    result=reject_request(id,e)
    if type(result) == Response:
        return result
    else: 
        return redirect(url_for('manage_event',id=result))

@app.route('/logs')
@secure
def logs():
    from project import logs 
    result=logs()
    if type(result) == Response:
        return result
    else: 
        return render_template('logs.html', **result) 

@app.route('/policy')
def policy():
    if current_user.is_authenticated:
        consents = current_user.consents
        from project import PRIVACY_INPUT 
        return render_template('policy.html', dpurposes=PRIVACY_INPUT, consents=consents)
    else:
        return redirect(url_for('user.login'))

@app.route('/revoke_consent', methods=['DELETE'])
def revoke_consent():
    if current_user.is_authenticated:
        data = request.get_json()
        my_purpose = Purpose.query.filter_by(name=data.get('purpose')).first()
        consents = Consent.query.filter_by(person_id=current_user.id, purpose_id=my_purpose.id, classname=data.get('class_name'), propertyname=data.get('property_name')).all()
        for consent in consents:
            db.session.delete(consent)
        db.session.commit()
        return jsonify({ 'success': True })
    else:
        return redirect(url_for('sec-error'))

@app.route('/grant_consent', methods=['POST'])
def grant_consent():
    if current_user.is_authenticated:
        data = request.get_json()
        my_purpose = Purpose.query.filter_by(name=data.get('purpose')).first()
        db.session.add(Consent(classname=data.get('class_name'),propertyname=data.get('property_name'),user=current_user,purpose=my_purpose))
        db.session.commit()
        return redirect(url_for('policy'))
    else:
        return redirect(url_for('sec-error'))
    

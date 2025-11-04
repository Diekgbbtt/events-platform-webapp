from flask import request
from flask_user import current_user, login_required
from model import db, Person, Role, Event, Category, Purpose, Ad, AnyPurpose, FunctionalPurpose, MarketingPurpose, AnalyticsPurpose, CorePurpose, RecommendEventsPurpose, TargetedMarketingPurpose, MassMarketingPurpose, Log, MODERATOR
from dto import PersonDTO, EventDTO, CategoryDTO, RoleDTO, AdDTO, LogDTO, RESTRICTED
import hashlib
import random
import sys
import os
import time
from cedar.authz import CedarClient, EntitySerializer, SecurityException

PURPOSES = [
    AnyPurpose, 
    FunctionalPurpose, 
    MarketingPurpose, 
    AnalyticsPurpose, 
    CorePurpose, 
    RecommendEventsPurpose, 
    TargetedMarketingPurpose, 
    MassMarketingPurpose
]

# Setup Cedar
serializer = EntitySerializer()
# TODO

POLICY_PATH = os.path.join(os.path.dirname(__file__), "cedar", "main.cedar")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "cedar", "main.cedarschema")

with open(POLICY_PATH, "r", encoding="utf-8") as policy_file:
    policies = policy_file.read()
    try:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
            schema = schema_file.read()
    except FileNotFoundError:
        schema = None
    cedar = CedarClient(policies, serializer, schema, verbose = True)

"""
Define your privacy input here. 
We introduce the privacy policy in the following structure:
PRIVACY_INPUT is a dictionary that contains all purpose items from the set of purposes PURPOSES
    Each element in PRIVACY_INPUT declares a purpose from PURPOSES, containing:
      - A list of data pairs (class_name, property_name) that describe personal data to be accessed (e.g., (Person, name)).
        (if no personal data is declared, leave the value as an empty list).
      - A dictionary of the children purpose.
        (if there are no child purposes, leave the value as an empty dictionary).
      - (Optional) An additional constraint description. This is for displaying in the privacy notice only, 
        as the actual implementation of the constraint must be implemented by you.
        If there is no additional constraint, you do not have to add it.

The following elements serve as an example. 
Your task is to define them according to the privacy requirements in the project description.
"""

PRIVACY_INPUT = {
    AnyPurpose: {
        "data": [("Person", "name"), ("Person", "manages")],
        "children": {
            MarketingPurpose: {
                "data": [],
                "children": {
                    MassMarketingPurpose: {
                        "data": [("Category", "name")],
                        "children": {},
                        "constraintDesc": "some other conditions"
                    }
                }
            }
        }
    },
    # This is only an example; your task is to define the elements according 
    # to the privacy requirements outlined in the project description.
    FunctionalPurpose: {
        "data": [("Person", "name")],
        "children": {},
        "constraintDesc": "some conditions"
    }
    # ...
}


"""
Throw this exception when action violates the privacy policy
You can either use the default error page or redirect to
another page (+ its params), which will then have a
notification at the bottom
"""
class PrivacyException(Exception):
    def __init__(self, msg = 'Not allowed', page = 'priv_error.html', params = {}):
        self.msg = msg
        self.page = page
        self.params = params

"""
Helper function for Cedar authorization checks
Returns True if allowed, False if not allowed (SecurityException caught)
"""
def check_cedar_permission(_caller, _action, _resource, context={}, entities=None):
    try:
        cedar.assert_allowed(_caller, _action, _resource, context=context, entities=entities)
        return True
    except SecurityException:
        return False

"""
Helper function to safely get attribute with Cedar authorization
If not authorized, returns RESTRICTED instead of the actual value
"""
def get_authorized_attribute(_self, _property, _caller, _action, _self_resource, context={}, entities=None):
    if check_cedar_permission(_caller, _action, _self_resource, context=context, entities=entities):
        return getattr(_self, _property)
    else:
        return RESTRICTED

"""
Use in case you need to initialize something
"""
def init():
    pass    

def main():
    user = PersonDTO.copy(current_user) 
    recommended = recommend_events(user) if user.is_authenticated else []
    return {'user' : user, 'recommended_events': recommended}

def users():
    users = PersonDTO.copies(Person.query.all())
    return {'users' : users}

def user(id):
    user = PersonDTO.copy(Person.query.get(id))
    roles = RoleDTO.copies(Role.query.all())
    return {'user' : user, 'roles' : roles}

def profile():
    user = PersonDTO.copy(current_user)
    ad = get_personalize_ad(user) if user.is_authenticated else None
    return {'user': user, 'ad': ad}

def update_user():
    user = Person.query.get(request.form["id"])
    # Updating user's name field if it has changed
    if request.form["name"] and user.name != request.form["name"]:
        user.name = request.form["name"]
    # Updating user's surname field if it has changed
    if request.form["surname"] and user.surname != request.form["surname"]:
        user.surname = request.form["surname"]
    # Updating user's email field if it has changed
    if request.form["email"] and user.email != request.form["email"]:
        user.email = request.form["email"]
    # Updating user's gender field if it has changed
    new_gender = request.form["gender"]
    if new_gender == "":
        new_gender = None
    if new_gender != user.gender:
        user.gender = new_gender
    # Updating user's role if it has changed
    if user.role.name != request.form["role"]:
        user.role = Role.query.filter_by(name=request.form["role"]).first()
    db.session.commit()
    return request.form["id"]

def join(id):
    event = Event.query.get(id)
    if current_user.id not in [p.id for p in event.requesters]:
        p = Person.query.get(current_user.id)
        event.requesters.append(p)
        db.session.commit()

def leave(id):
    event = Event.query.get(id)
    if current_user.id in [p.id for p in event.attendants]:
        p = Person.query.get(current_user.id)
        event.attendants.remove(p)
        db.session.commit()

def add_moderator(id,c):
    user = Person.query.get(id)
    category = Category.query.get(c)
    if user not in category.moderators:
        category.moderators.append(user)
        db.session.commit()

def remove_moderator(id,c):
    user = Person.query.get(id)
    category = Category.query.get(c)
    if user in category.moderators:
        category.moderators.remove(user)
        db.session.commit()

def subscribe(id):
    category = Category.query.get(id)
    if category not in current_user.subscriptions:
        current_user.subscriptions.append(category)
        db.session.commit()
    
def unsubscribe(id):
    category = Category.query.get(id)
    if category in current_user.subscriptions:
        current_user.subscriptions.remove(category)
        db.session.commit()
        
def events():   
    events = EventDTO.copies(Event.query.all())
    categories = CategoryDTO.copies(Category.query.all())
    return {'events': events, 'categories': categories}
    
def create_event():
    event = Event()
    event.owner = current_user
    event.managedBy.append(current_user)
    event.attendants.append(current_user)
    event.title = request.form["title"]
    event.description = request.form["description"]
    categories = request.form.getlist("categories")
    for cid in categories:
        c = Category.query.get(cid)
        event.categories.append(c)
    db.session.add(event)
    db.session.commit()

def view_event(id):
    event = Event.query.get(id)
    event_dto = EventDTO.copy(event)
    # Create a log entry for viewing the event
    log = Log()
    log.timestamp = int(time.time())
    log.user = current_user if current_user.is_authenticated else None
    log.event = event
    db.session.add(log)
    db.session.commit()
    return {'event': event_dto}

def edit_event(id):
    event = EventDTO.copy(Event.query.get(id))
    categories = CategoryDTO.copies(Category.query.all())
    return {'event': event, 'categories': categories}

def update_event():
    event = Event.query.get(request.form["id"])
    # Updating event's title if it has changed
    if event.title != request.form["title"]:
        event.title = request.form["title"]
    # Updating event's description if it has changed
    if event.description != request.form["description"]:
        event.description = request.form["description"]
    # Updating event's categories if they have changed
    new_categories = [int(id) for id in request.form.getlist("categories")]
    current_categories = [c.id for c in event.categories]
    if set(current_categories) != set(new_categories):
        ids_to_remove = set(current_categories) - set(new_categories)
        ids_to_add = set(new_categories) - set(current_categories)
        # Only remove the deleted ones
        for cid in ids_to_remove:
            c = Category.query.get(cid)
            event.categories.remove(c)
        # and add the new ones
        for cid in ids_to_add:
            c = Category.query.get(cid)
            event.categories.append(c)
    db.session.commit()
    return request.form["id"]

def manage_event(id):
    event = EventDTO.copy(Event.query.get(id))
    return {'event': event}

def remove_category(id,c):
    event = Event.query.get(id)
    category = Category.query.get(c)
    if event in category.events:
        category.events.remove(event)
        db.session.commit()
    return c

def promote_manager(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    if user not in event.managedBy:
        event.managedBy.append(user)
        db.session.commit()
    return e

def demote_manager(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    if user in event.managedBy:
        event.managedBy.remove(user)
        db.session.commit()
    return e

def remove_attendee(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    if user in event.attendants:
        event.attendants.remove(user)
        db.session.commit()
    return e

def accept_request(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    if user not in event.attendants:
        event.attendants.append(user)
    event.requesters.remove(user)
    db.session.commit()
    return e

def reject_request(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    event.requesters.remove(user)
    db.session.commit()
    return e

def categories():
    categories = CategoryDTO.copies(Category.query.all())
    return {'categories': categories}

def create_category():
    category = Category()
    category.name = request.form["name"]
    db.session.add(category)
    db.session.commit()

def view_category(id):
    category = CategoryDTO.copy(Category.query.get(id))
    return {'category': category}

def edit_category(id):
    cat = Category.query.get(id)
    category = CategoryDTO.copy(cat)
    candidates = PersonDTO.copies(get_candidates(cat))
    return {'category': category, 'candidates': candidates}

def update_category():
    category = Category.query.get(request.form["id"])
    if category.name != request.form["name"]:
        category.name = request.form["name"]
    db.session.commit()
    return request.form["id"]

def ads():  
    ads = AdDTO.copies(Ad.query.all())
    return {'ads': ads}

def remove_ad(id):
    ad = Ad.query.get(id)
    db.session.delete(ad)
    db.session.commit()

def create_ad():
    ad = Ad()
    ad.content = request.form["content"]
    db.session.add(ad)
    db.session.commit()

def send_mass_advertisement(id):
    category = Category.query.get(id)
    for subscriber in category.subscribers:
        send_advertisement_to_user(subscriber) 

def analyze(id):
    event = EventDTO.copy(Event.query.get(id))
    gender_counts = {"male": 0, "female": 0, "unknown": 0}
    for p in event.attendants:
        gender = p.gender if p.gender in gender_counts else "unknown"
        gender_counts[gender] += 1    
    return {
        'event': event,
        'male': gender_counts['male'],
        'female': gender_counts['female'],
        'unknown': gender_counts['unknown']
    }

def logs():
    logs = LogDTO.copies(Log.query.all())
    def format_timestamp(timestamp):
        try:
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
        except:
            return timestamp
    return {'logs': logs, 'format_timestamp': format_timestamp}

def recommend_events(user):
    subscribed_event_ids = []
    for category in user.subscriptions:
        category = CategoryDTO.copy(Category.query.get(category.id))
        subscribed_event_ids.extend([e.id for e in category.events])
    viewing_event_ids = []
    for log in user.logs:
        log = LogDTO.copy(Log.query.get(log.id))
        viewing_event_ids.append(log.event.id)
    recommend_event_ids = list(set(subscribed_event_ids + viewing_event_ids) - set([event.id for event in user.attends]))
    recommend_events = [
        EventDTO.copy(Event.query.get(id))
        for id in recommend_event_ids
    ]
    return recommend_events

def get_personalize_ad(user):
    seed_string = f"{user.id}{user.name}{user.gender}"
    seed_value = int(hashlib.sha256(seed_string.encode()).hexdigest(), 16)
    random.seed(seed_value)
    ads = AdDTO.copies(Ad.query.all())
    if len(ads) == 0:
        return None
    else:
        return ads[random.randint(1, len(ads)) - 1]

def send_advertisement_to_user(user):
    if user.email:
        print(f'A generic advertisement was sent to {user.name} at email: {user.email}.', file=sys.stderr)

def get_candidates(cat):
    all_ids = [m.id for m in Person.query.all() if MODERATOR == m.role.name]
    mod_ids = [m.id for m in cat.moderators]
    candidate_ids = list(set(all_ids) - set(mod_ids)) 
    return [Person.query.get(id) for id in candidate_ids]
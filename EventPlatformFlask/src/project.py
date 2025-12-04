from flask import request
from flask_user import current_user, login_required
from model import ADMIN, db, Person, Role, Event, Category, Purpose, Ad, Consent, AnyPurpose, FunctionalPurpose, MarketingPurpose, AnalyticsPurpose, CorePurpose, RecommendEventsPurpose, TargetedMarketingPurpose, MassMarketingPurpose, Log, MODERATOR
from dto import PersonDTO, EventDTO, CategoryDTO, RoleDTO, AdDTO, LogDTO, InviteDTO, RESTRICTED, _clear_cache
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
        "data": [("Person", "name"), ("Person", "surname"), ("Person", "gender"), ("Person", "role"), ("Person", "email"), ("Person", "subscriptions"), ("Person", "logs"), ("Log", "event")],
        "children": {
            MarketingPurpose: {
                "data": [("Person", "name"), ("Person", "gender"), ("Person", "email")],
                "children": {
                    TargetedMarketingPurpose: {
                        "data": [("Category", "name"), ("Person", "gender")],
                        "children": {},
                        "constraintDesc": ""
                    },
                    MassMarketingPurpose: {
                        "data": [("Category", "name"), ("Person", "email")],
                        "children": {},
                        "constraintDesc": ""
                    }
                }
            },
            AnalyticsPurpose: {
                "data": [("Person", "gender")],
                "children": {},
                "constraintDesc": ""
            },
            FunctionalPurpose: {
                "data": [("Person", "logs"), ("Log", "event"), ("Person", "name"), ("Person", "surname"), ("Person", "gender"), ("Person", "role"), ("Person", "email")], # could be Person::name instead as it is what
                "children": {
                    RecommendEventsPurpose: {
                        "data": [("Person", "logs")],
                        "children": {
                            RecommendEventsPurpose: {
                                "data": [("Person", "subscriptions")],
                                "children": {},
                                "constraintDesc": " you are a REGULARUSER"
                            }
                        },
                        "constraintDesc": ""
                    },
                    CorePurpose: {
                        "data": [("Person", "name"), ("Person", "surname"), ("Person", "gender"), ("Person", "role"), ("Person", "email"), ("Person", "subscriptions")],
                        "children": {},
                        "constraintDesc": ""
                    }
                },
                "constraintDesc": ""
            }
        }
    }
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

def check_access_consent(owner: Person, entity: str, attribute: str, purposes: list[str]):
    try:
        has_consent(owner, entity, attribute, purposes)
        return True
    except PrivacyException:
        return False

"""
Helper function to safely get attribute with Cedar authorization
If not authorized, returns RESTRICTED instead of the actual value
"""
def get_authorized_attribute(_self, _property, _caller, _action, _self_resource, context={}, entities=None):
    
    value = getattr(_self, _property)
    
    if isinstance(value, list):
        authorized_list = []
        if not current_user.is_authenticated:
            return []
        for v in value:
            # if check_cedar_permission(_caller, _action, _self_resource, context={"requester" : {"id" : v.id}}, entities=entities):
            if check_cedar_permission(_caller, _action, _self_resource, context={"requesterusr" : v.username.strip()}, entities=entities):
               authorized_list.append(v)
        return authorized_list

    elif current_user.is_authenticated and check_cedar_permission(_caller, _action, _self_resource, context=context, entities=entities):
        return value
    return RESTRICTED



def has_consent(owner: Person, entity: str, attribute: str, purposes: list[str]):
    
    owner_consent = (
        Consent.query.join(Purpose)
        .filter(
            Consent.person_id == owner.id,
            Consent.classname == entity,
            Consent.propertyname == attribute,
            Purpose.name.in_(purposes)
        )
        .first()
    )
    
    if not owner_consent:
        purposes_label = "', '".join(purposes)
        raise PrivacyException(msg=fr"consent to access '{attribute}' of '{entity}' for purposes '{purposes_label}' not granted by '{owner.username}' ")

def has_consents(owner: Person, entity: str, attributes: list[str], purposes: list[str]):
    for a in attributes:
        try:
            has_consent(owner, entity, a, purposes)
        except PrivacyException as pe:
            raise pe

"""
Use in case you need to initialize something
"""
def init():
    pass    

def main():
    recommended = []
    user = current_user
    if current_user.is_authenticated:
        event_recommendation_perm = (
            check_access_consent(current_user, "Person", "logs", [RecommendEventsPurpose, FunctionalPurpose, AnyPurpose])
            and check_access_consent(current_user, "Log", "event", [FunctionalPurpose, AnyPurpose])
        )
        if current_user.role == "REGULARUSER":
            event_recommendation_perm = (
                event_recommendation_perm
                and check_access_consent(current_user, "Person", "subscriptions", [RecommendEventsPurpose, FunctionalPurpose, AnyPurpose])
            )     
        
        user = PersonDTO.copy(_serialize_user(current_user, ["name", "surname"]))
        recommended = recommend_events(user) if event_recommendation_perm else []

    return {'user' : user, 'recommended_events': recommended}

def users():
    users = Person.query.all()
    users_dto = []
    for u in users:
        u_dto = PersonDTO(
                id=u.id,
                name=u.name if check_access_consent(u, "Person", "name", [CorePurpose, FunctionalPurpose, AnyPurpose]) else RESTRICTED,
                surname=u.surname if check_access_consent(u, "Person", "surname", [CorePurpose, FunctionalPurpose, AnyPurpose]) else RESTRICTED
                )
        _clear_cache()
        users_dto.append(u_dto)
    return {'users' : users_dto}


def _serialize_user(user: Person, personal_data : list[str] = []):
    if user is None:
        return None
    # TODO maybe externalise to a _restricted_person_dto method that restrict attributes according to the calling method  
    user_dto = PersonDTO(user.id,
                        name=user.name,
                        surname=user.surname,
                        gender=user.gender,
                        email=user.email,
                        roles=RoleDTO.copies(user.roles),
                        events=EventDTO.copies(user.events),
                        manages=EventDTO.copies(user.manages),
                        attends=EventDTO.copies(user.attends),
                        requests=EventDTO.copies(user.requests),
                        subscriptions=CategoryDTO.copies(user.subscriptions),
                        moderates=CategoryDTO.copies(user.moderates),
                        invitations=InviteDTO.copies(user.invitations),
                        invites=InviteDTO.copies(user.invites)
                )   
    _clear_cache()
    can_read_person = (
        current_user.is_authenticated
        and check_cedar_permission(
            _caller=current_user, _action="readPerson", _resource=user
        )
    )

    if not can_read_person:
        user_dto.password = RESTRICTED
        if not (current_user.is_authenticated and check_cedar_permission(current_user, "moderatorReadEmail", user)):
            user_dto.email = RESTRICTED
        user_dto.gender = RESTRICTED
        user_dto.name = RESTRICTED
        user_dto.surname = RESTRICTED
        user_dto.events = []
        user_dto.manages = []
        user_dto.attends = []
        user_dto.requests = []
        user_dto.subscriptions = []
        user_dto.logs = []
        user_dto.invitations = []
        user_dto.invites = []
        return user_dto

    return _serialize_user_privacy(user, user_dto, personal_data)

def _serialize_user_privacy(user: Person, user_dto: PersonDTO, personal_data : list[str] = []):
    for pd in personal_data or []:
        if not hasattr(user_dto, pd):
            continue
        value = getattr(user_dto, pd)
        if value == RESTRICTED:
            continue
        if not check_access_consent(user, "Person", pd, [CorePurpose, FunctionalPurpose, AnyPurpose]):
            setattr(user_dto, pd, [] if isinstance(value, list) else RESTRICTED)
    return user_dto

def user(id):
    user = Person.query.get(id)
    user_dto = _serialize_user(user, ["name", "surname", "gender", "role", "email", "subscriptions"])
    roles_dto = RoleDTO.copies(Role.query.all())
    return {'user' : user_dto, 'roles' : roles_dto}

def profile():
    if not current_user.is_authenticated:
        return {'user': PersonDTO.copy(current_user), 'ad': None}
    
    ad_permission = (
    check_access_consent(current_user, "Person", "gender", [TargetedMarketingPurpose, MarketingPurpose, AnyPurpose])
    and check_access_consent(current_user, "Person", "name", [MarketingPurpose, AnyPurpose])
    )
    user_dto = _serialize_user(current_user, ["subscriptions"])
    ad = get_personalize_ad(user_dto) if ad_permission else None
    
    return {'user': user_dto, 'ad': ad}

def update_user():
    try:
        if not current_user.is_authenticated:
            raise SecurityException(
                msg="not authenticated users can't request to join events", page="sec_error.html"
            )
        user = Person.query.get(request.form["id"])
        has_consents(user, "Person", ["name", "surname", "gender", "email", "role"], [CorePurpose, FunctionalPurpose, AnyPurpose])
        cedar.assert_allowed(principal=current_user, action="updateUser", resource=user)
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
            if check_cedar_permission(_caller=current_user, _action="updateUserRole", _resource=user):
                user.role = Role.query.filter_by(name=request.form["role"]).first()
        db.session.commit()
        return request.form["id"]
    except SecurityException as se:
        db.session.rollback()
        raise se

def join(id):
    if not current_user.is_authenticated:
        raise SecurityException(
            msg="not authenticated users can't request to join events", page="sec_error.html"
        )
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
    try:
        if not current_user.is_authenticated:
            raise SecurityException (
                msg=f"create event not allowed for not authenticated users", page='sec_error.html'
            )
        user = Person.query.get(id)
        category = Category.query.get(c)
        cedar.assert_allowed(principal=current_user, action="addCategoryModerator", resource=category)
        if user not in category.moderators:
            category.moderators.append(user)
            db.session.commit()
    except SecurityException as se:
        db.session.rollback()
        raise se

def remove_moderator(id,c):
    try:    
        if not current_user.is_authenticated:
            raise SecurityException (
                    msg=f"create event not allowed for not authenticated users", page='sec_error.html'
            )
        user = Person.query.get(id)
        category = Category.query.get(c)
        cedar.assert_allowed(principal=current_user, action="removeCategoryModerator", resource=category, context={"removedModerator" : serializer._entity_pointer(user)})
        if user in category.moderators:
            category.moderators.remove(user)
            db.session.commit()
    except SecurityException as se:
        db.session.rollback()
        raise se

def subscribe(id):
    if current_user.is_authenticated:
        has_consent(current_user, "Person", "subscriptions", [CorePurpose, FunctionalPurpose, AnyPurpose])
        # if current_user.role == "REGULARUSER":
        # has_consent(current_user, "Person", "subscriptions", [RecommendEventsPurpose, FunctionalPurpose, AnyPurpose])
        category = Category.query.get(id)
        if category not in current_user.subscriptions:
            current_user.subscriptions.append(category)
            db.session.commit()
    
def unsubscribe(id):
    if current_user.is_authenticated:
        has_consent(current_user, "Person", "subscriptions", [CorePurpose, FunctionalPurpose, AnyPurpose])
        # if current_user.role == "REGULARUSER":
        #  has_consent(current_user, "Person", "subscriptions", [RecommendEventsPurpose, FunctionalPurpose, AnyPurpose])
        category = Category.query.get(id)
        if category in current_user.subscriptions:
            current_user.subscriptions.remove(category)
            db.session.commit()
        
def _restricted_person_dtos(people):
    restricted = []
    for person in people:
        restricted.append(
            PersonDTO(
                id=person.id,
                name=person.name if check_access_consent(person, "Person", "name", [CorePurpose, FunctionalPurpose, AnyPurpose]) else RESTRICTED,
                surname=person.surname if check_access_consent(person, "Person", "surname", [CorePurpose, FunctionalPurpose, AnyPurpose]) else RESTRICTED,
            )
        )
        _clear_cache()
    return restricted


def _serialize_event(event):
    accessible_requests = []
    
    if current_user.is_authenticated:
        if event.owner.id == current_user.id or any(current_user.id == manager.id for manager in event.managedBy):
            accessible_requests = event.requesters
        else:
            # cedar policy 'principal in Role::"ADMIN"'
            for r in event.requesters:
                if check_cedar_permission(
                    _caller=current_user,
                    _action="readEventRequesters",
                    _resource=event,
                    context={"requesterusr": r.username.strip()},
                ):
                    accessible_requests.append(r)

    requesters_dto = _restricted_person_dtos(accessible_requests)
    managers_dto = _restricted_person_dtos(event.managedBy)
    attendants_dto = _restricted_person_dtos(event.attendants)
    
    event_dto = EventDTO(
        id=event.id,
        title=event.title,
        description=event.description,
        owner=event.owner,
        categories=CategoryDTO._clones(event.categories),
        managedBy=managers_dto,
        attendants=attendants_dto,
        requesters=requesters_dto,
        logs=_serialize_logs(event.logs),
    )
    _clear_cache()

    return event_dto

def events():   
    events = Event.query.all()
    events_dto = []
    for e in events:
        owner_dto = PersonDTO(
                    id=e.owner.id,
                    name=e.owner.name if check_access_consent(e.owner, "Person", "name", [CorePurpose, FunctionalPurpose, AnyPurpose]) else RESTRICTED,
                    surname=e.owner.surname if check_access_consent(e.owner, "Person", "surname", [CorePurpose, FunctionalPurpose, AnyPurpose]) else RESTRICTED,
                    )
        events_dto.append(
            EventDTO(
            id=e.id,
            title=e.title,
            description=e.description,
            owner=owner_dto,
            categories=[],
            managedBy=[],
            attendants=[],
            requesters=[],
            logs=[],
            )
        )
        _clear_cache()

    categories = CategoryDTO.copies(Category.query.all())
    return {'events': events_dto, 'categories': categories}
    
def create_event():
    try:
        if not current_user.is_authenticated:
            raise SecurityException (
                msg=f"create event not allowed for not authenticated users", page='sec_error.html'
            )
        has_consents(current_user, "Person", ["name", "surname", "gender", "email", "role"], [CorePurpose, FunctionalPurpose, AnyPurpose])
        current_user_events = Person.query.get(current_user.id).events
        cedar.assert_allowed(principal=current_user, action="addEvent", resource='EventsContainer::"Global"', context={"userEvents" : len(current_user_events)})
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
    except SecurityException as se:
        db.session.rollback()
        raise se


def view_event(id):
    
    user_access_consent = True
    if current_user.is_authenticated:
        for pd in ["name", "surname", "gender", "email", "role"]: 
            user_access_consent = check_access_consent(current_user, "Person", pd, [CorePurpose, FunctionalPurpose, AnyPurpose])
    
    event = Event.query.get(id)
    log = Log()
    log.timestamp = int(time.time())
    log.user = current_user if current_user.is_authenticated and user_access_consent else None
    log.event = event
    db.session.add(log)
    db.session.commit()
    event_dto = EventDTO.copy(event)
    event_dto.attendants = _restricted_person_dtos(event.attendants)
    return {'event': event_dto}

def edit_event(id):
    event = EventDTO.copy(Event.query.get(id))
    categories = CategoryDTO.copies(Category.query.all())
    return {'event': event, 'categories': categories}

def update_event():
    try:
        if not current_user.is_authenticated:
            raise SecurityException(
                msg="update event not allowed for not authenticated users", page='sec_error.html'
            )
        
        event = Event.query.get(request.form["id"])
  
        cedar.assert_allowed(principal=current_user, action="updateEvent", resource=event)
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
        # principal could be moderator of both categories that are beign added and removed 
            ids_to_remove = set(current_categories) - set(new_categories)
            ids_to_add = set(new_categories) - set(current_categories)
            # Only remove the deleted ones
            for cid in ids_to_remove:
                c = Category.query.get(cid)
                if check_cedar_permission(_caller=current_user, _action="removeCategoryEvent", _resource=c, context={"eventmanagers" : [serializer._entity_pointer(p) for p in event.managedBy]}):
                    event.categories.remove(c)
            # and add the new ones
            for cid in ids_to_add:
                c = Category.query.get(cid)
                if check_cedar_permission(_caller=current_user, _action="addCategoryEvent", _resource=c, context={"eventmanagers" : [serializer._entity_pointer(p) for p in event.managedBy]}):
                    event.categories.append(c)
        db.session.commit()
        return request.form["id"]
    except SecurityException as se:
        db.session.rollback()
        raise se

def manage_event(id):
    event_dto = _serialize_event(Event.query.get(id))
    return {'event' : event_dto, 'users' : get_invite_candidates(event_dto)}


def remove_category(id,c):
    try:
        if not current_user.is_authenticated:
            raise SecurityException(
                msg="not authenticated users can't remove events from categories"
            )
        event = Event.query.get(id)
        category = Category.query.get(c)
        cedar.assert_allowed(principal=current_user, action="removeCategoryEvent", resource=category, context={"eventmanagers" : [serializer._entity_pointer(p) for p in event.managedBy]})
        if event in category.events:
            category.events.remove(event)
            db.session.commit()
        return c
    except SecurityException as se:
        db.session.rollback()
        raise se
def promote_manager(id,e):
    try:
        if not current_user.is_authenticated:
            raise SecurityException(
            msg="promote event attendants to managers not allowed for not authenticated users", page='sec_error.html'
            )
        user = Person.query.get(id)
        event = Event.query.get(e)
        # for authZ policies that involve verification of ADMIN role I assume it is not required to check for consent as ADMIN is allegedly the owner of the platform, all other kind of users request lead firstly to an authZ deny decision 
        # has_consent(user, "Person", "role", [CorePurpose, FunctionalPurpose, AnyPurpose])
        cedar.assert_allowed(principal=current_user, action="promoteAttendant", resource=event)
        if user not in event.managedBy:
            event.managedBy.append(user)
            db.session.commit()
        return e
    except SecurityException as se:
        db.session.rollback()
        raise se

def demote_manager(id,e):
    try:
        if not current_user.is_authenticated:
            raise SecurityException(
            msg="demote event managers not allowed for not authenticated users", page='sec_error.html'
            )
        user = Person.query.get(id)
        event = Event.query.get(e)
        # for authZ policies that involve verification of ADMIN role I assume it is not required to check for consent as ADMIN is allegedly the owner of the platform, all other kind of users request lead firstly to an authZ deny decision 
        # has_consent(user, "Person", "role", [CorePurpose, FunctionalPurpose, AnyPurpose])
        cedar.assert_allowed(principal=current_user, action="demoteManager", resource=event, context={"demotedManager" : serializer._entity_pointer(subject=user)})
        if user in event.managedBy:
            event.managedBy.remove(user)
            db.session.commit()
        return e
    except SecurityException as se:
        db.session.rollback()
        raise se

def remove_attendee(id,e):
    try:
        if not current_user.is_authenticated:
            raise SecurityException(
            msg="remove event attendants not allowed for not authenticated users", page='sec_error.html'
            )
        user = Person.query.get(id)
        event = Event.query.get(e)
        cedar.assert_allowed(principal=current_user, action="removeAttendant", resource=event, context={"removedAttendant" : serializer._entity_pointer(subject=user)})
        if user in event.attendants:
            event.attendants.remove(user)
            db.session.commit()
        return e
    except SecurityException as se:
        db.session.rollback()
        raise se
def accept_request(id,e):
    try:
        if not current_user.is_authenticated:
            raise SecurityException(
            msg="accept event requests not allowed for not authenticated users", page='sec_error.html'
            )
        user = Person.query.get(id)
        event = Event.query.get(e)
        cedar.assert_allowed(principal=current_user, action="acceptRequest", resource=event)
        if user not in event.attendants:
            event.attendants.append(user)
        event.requesters.remove(user)
        db.session.commit()
        return e
    except SecurityException as se:
        db.session.rollback()
        raise se

def reject_request(id,e):
    try:
        if not current_user.is_authenticated:
            raise SecurityException(
            msg="reject event requests not allowed for not authenticated users", page='sec_error.html'
            )
        user = Person.query.get(id)
        event = Event.query.get(e)
        cedar.assert_allowed(principal=current_user, action="rejectRequest", resource=event, context={"rejectedRequester" : serializer._entity_pointer(user)})
        event.requesters.remove(user)
        db.session.commit()
        return e
    except SecurityException as se:
        db.session.rollback()
        raise se
def categories():
    categories = CategoryDTO.copies(Category.query.all())
    return {'categories': categories}

def create_category():
    try:
        if not current_user.is_authenticated:
            raise SecurityException(
                msg="not authenticated users can't create new categories"
            )
        # for authZ policies that involve verification of ADMIN role I assume it is not required to check for consent as ADMIN is allegedly the owner of the platform, all other kind of users request lead firstly to an authZ deny decision 
        cedar.assert_allowed(principal=current_user, action="addCategory", resource='CategoriesContainer::"Global"')
        category = Category()
        category.name = request.form["name"]
        db.session.add(category)
        db.session.commit()
    except SecurityException as se:
        db.session.rollback()
        raise se

def _serialize_category(category):

    consenting_subscribers = [
        subscriber
        for subscriber in category.subscribers
        if check_access_consent(
            subscriber,
            "Person",
            "subscriptions",
            [CorePurpose, FunctionalPurpose, AnyPurpose],
        )
    ]
    consenting_moderators = [
        moderator
        for moderator in category.moderators
        if check_access_consent(
            moderator,
            "Person",
            "subscriptions",
            [CorePurpose, FunctionalPurpose, AnyPurpose],
        )
    ]
    can_read_subscribers = current_user.is_authenticated and check_cedar_permission(
        _caller=current_user,
        _action="readCategorySubscribers",
        _resource=category,
    )
    subscriber_dtos = (
        _restricted_person_dtos(consenting_subscribers) if can_read_subscribers else []
    )
    moderator_dtos = _restricted_person_dtos(consenting_moderators)
    events_dto = []
    for event in category.events:
        owner_dto = _restricted_person_dtos([event.owner])[0] if event.owner else RESTRICTED
        events_dto.append(
            EventDTO(
                id=event.id,
                title=event.title,
                description=event.description,
                owner=owner_dto,
            )
        )
    _clear_cache()
    cat_dto = CategoryDTO(
        id=category.id,
        name=category.name,
        subscribers=subscriber_dtos,
        moderators=moderator_dtos,
        events=events_dto
    )
    _clear_cache()
    return cat_dto


def view_category(id):
    category_dto = _serialize_category(Category.query.get(id))
    return {'category': category_dto}

def edit_category(id):
    cat = Category.query.get(id)
    cat_dto = _serialize_category(cat)
    cands_dto = get_candidates(cat)
        
    return {'category': cat_dto, 'candidates': cands_dto}

def update_category():
    if not current_user.is_authenticated:
        raise SecurityException (
            msg="Analyze event not allowed for not authenticated users", page='sec_error.html'
            )
    category = Category.query.get(request.form["id"])
    cedar.assert_allowed(principal=current_user, action="updateCategory", resource=category)
    if category.name != request.form["name"]:
        category.name = request.form["name"]
    db.session.commit()
    return request.form["id"]

def ads():  
    ads = AdDTO.copies(Ad.query.all())
    return {'ads': ads}

def remove_ad(id):
    try:
        if not current_user.is_authenticated:
            raise SecurityException (
            msg="Create Ad not allowed for not authenticated users", page='sec_error.html'
            )
        ad = Ad.query.get(id)
        cedar.assert_allowed(principal=current_user, action="removeAd", resource=ad)
        db.session.delete(ad)
        db.session.commit()
    except SecurityException as se:
        db.session.rollback()
        raise se
def create_ad():
    try:
        if not current_user.is_authenticated:
            raise SecurityException (
                msg="Create Ad not allowed for not authenticated users", page='sec_error.html'
            )
        cedar.assert_allowed(principal=current_user, action="addAd", resource='AdContainer::"Global"')
        ad = Ad()
        ad.content = request.form["content"]
        db.session.add(ad)
        db.session.commit()
    except SecurityException as se:
        db.session.rollback()
        raise se

def send_mass_advertisement(id):
    try:
        if not current_user.is_authenticated:
            raise SecurityException (
            msg="Analyze event not allowed for not authenticated users", page='sec_error.html'
            )
        category = Category.query.get(id)
        cedar.assert_allowed(principal=current_user, action="addAd", resource='AdContainer::"Global"')
        for sub in category.subscribers:
            if check_access_consent(sub, "Person", "subscriptions", [CorePurpose, FunctionalPurpose, AnyPurpose]):
                send_advertisement_to_user(sub) 
    except SecurityException as se:
        db.session.rollback()
        raise se


def analyze(id):
    try:
        if not current_user.is_authenticated:
            raise SecurityException (
            msg="Analyze event not allowed for not authenticated users", page='sec_error.html'
            )
        cedar.assert_allowed(principal=current_user, action="analyze", resource='Event::"Global"')
        event = EventDTO.copy(Event.query.get(id))
        gender_counts = {"male": 0, "female": 0, "unknown": 0}
        for a in event.attendants:
            if check_access_consent(a, "Person", "gender", [AnalyticsPurpose, AnyPurpose]):
                gender = a.gender if a.gender in gender_counts else "unknown"
                gender_counts[gender] += 1    
        return {
            'event': event,
            'male': gender_counts['male'],
            'female': gender_counts['female'],
            'unknown': gender_counts['unknown']
        }
    except SecurityException as se:
        raise se


def _serialize_log(log: Log):
    
    if log.user != None:

        log_dto = LogDTO(
            id=log.id,
            timestamp=log.timestamp,
            event=EventDTO.copy(log.event) if check_access_consent(log.user, "Person", "logs", [FunctionalPurpose, AnyPurpose]) else RESTRICTED,
            user=PersonDTO.copy(log.user) if check_access_consent(log.user, "Person", "name", [CorePurpose, FunctionalPurpose, AnyPurpose]) else RESTRICTED
        )
        _clear_cache()
        return log_dto
    else:
        return LogDTO.copy(log)


def _serialize_logs(logs: list[Log]):
    logs_dto: list[LogDTO] = []
    if current_user.is_authenticated:     
        if not check_cedar_permission(_caller=current_user, _action="readAllLogs", _resource='LogContainer::"Global"'):
            for l in logs:
                if check_cedar_permission(_caller=current_user, _action="readLog", _resource=l):
                    logs_dto.append(_serialize_log(l))
        else:
            for l in logs:
                logs_dto.append(_serialize_log(l))
    
    return logs_dto

def logs():
    if not current_user.is_authenticated:
        raise SecurityException(
            msg="not authenticated users can't read logs", page="sec_error.html"
        )

    logs_dto = _serialize_logs(Log.query.all())

    def format_timestamp(timestamp):
        try:
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
        except:
            return timestamp
    
    return {'logs': logs_dto, 'format_timestamp': format_timestamp}

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
    if user.email and check_access_consent(user, "Person", "email", [MassMarketingPurpose, MarketingPurpose, AnyPurpose]):
        print(f'A generic advertisement was sent to {user.name} at email: {user.email}.', file=sys.stderr)
    else:
        print(f'{user.name} with email: {user.email}. either does not have sent an email or did not consent for its access with a massMarketingPurpose', file=sys.stderr)

def get_candidates(cat):
    # Given the responsibility of all moderators, I assume no access consent verification is required
    all_ids = [m.id for m in Person.query.all() if MODERATOR == m.role.name]
    mod_ids = [m.id for m in cat.moderators]
    candidate_ids = list(set(all_ids) - set(mod_ids)) 
    candidates = [Person.query.get(id) for id in candidate_ids]
    consenting_candidates = [
        c
        for c in candidates
        if check_access_consent(
            c,
            "Person",
            "subscriptions",
            [CorePurpose, FunctionalPurpose, AnyPurpose],
        )
    ]
    return _restricted_person_dtos(consenting_candidates)

# New code for phase 3 - ChangeRequest code

from model import Invite, InsightsPurpose, StatsPurpose
from dto import InviteDTO

def personalized_stats(id):
    user=Person.query.get(id)
    user_dto=PersonDTO.copy(user)
    return {'user' : user_dto}

def send_invite(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    invite = Invite(
        event=event,
        invitedBy=current_user,
        invitee=user
    )
    db.session.add(invite)
    db.session.commit()

def accept_invitation(id):
    invite = Invite.query.get(id)
    event = invite.event
    user = invite.invitee
    event.attendants.append(user)
    db.session.delete(invite)
    db.session.commit()

def decline_invitation(id):
    invite = Invite.query.get(id)
    db.session.delete(invite)
    db.session.commit()

# This is a sample of how one can extend the functionality of the manage_event
# using the get_invite_candidates function.
# def manage_event(id):
#     event = EventDTO.copy(Event.query.get(id))
#     return {'event' : event, 'users' : get_invite_candidates(event)}

def get_invite_candidates(event_dto):
    all_users = Person.query.all()
    invitees = list([i.invitee.id for i in event_dto.invitations])
    attendants = list([a.id for a in event_dto.attendants])
    requesters = list([r.id for r in event_dto.requesters])
    users = []
    for u in all_users:
        if u.id not in invitees and u.id not in attendants and u.id not in requesters:
            users.append(u)
    return PersonDTO.copies(users)

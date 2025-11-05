"""Data Transfer Object (DTO)

This module defines a class of DTOs for every data
model class, e.g., PersonDTO is a DTO class for
the Person data model class. 

DTOs are used to build a subset of the data model, 
which is to be passed to a web page template and 
rendered/shown to a user. 

By building and passing a DTO instead of a data 
model class we ensure that the web page template 
can only use limited information and display it 
to the user.

Each DTO class has a constructor with key-value 
parameters, as well as a "copy" method.
The copy method takes an object of the 
correspoding data model class as a parameter and 
instantiates its DTO. Copy method also instantiates 
DTOs of the data model objects directly associated with
object passed as the parameter. Associations ends 
of the passed object are complete w.r.t. their data model
counterparts, whereas other instantiated DTO's may not
have complete association ends after copy terminates.

In other words copy(obj: Person) -> PersonDTO
instantiates DTOs coresponsing to the subset of the 
data model centered around obj.

For example, suppose we have the following data model 
objects 

p1: Person 
    attendants <------> attends e1: Event
                                    events <------> categories c1: Categories

PersonDTO.copy(p1) produces

p1': PersonDTO
     attendants <------> attends e1': EventDTO
                                      events = []

After creating DTOs (via constructors or the copy method)
one may assign the RESTRICTED object (see below) to its 
attributes or 0-1 association ends. Also, a 0-* association
end can be filtered, or restricted completely by assigning
[] to it.

"""
from flask_login import AnonymousUserMixin
from typing import Iterator

class Restrict(list,Iterator):
    def __repr__(self):
        return "RESTRICTED"
    def __getattr__(self,attr):
        return self
    def __setattr__(self,attr,value):
        return self  
    def __call__(self, *args, **kwargs):
        return self
    def __len__(self):
        return 0
    def append(self, object):
        pass
    def clear(self):
        pass
    def copy(self):
        return self
    def count(self, value):
        return self 
    def extend(self, iterable):
        pass
    def index(self, value, start, stop):
        return self
    def insert(self, index, object):
        pass
    def pop(self, index):
        return self 
    def remove(self, value):
        pass
    def reverse(self):
        pass 
    def sort(self, *, key, reverse):
        pass 
    def __gt__(self, value):
        return self 
    def __ge__(self, value):
        return self  
    def __lt__(self, value):
        return self  
    def __le__(self, value):
        return self  
        
RESTRICTED = Restrict()
"""RESTRICTED Object

Whenever some information (e.g., an attribute value) 
may not be used by a web page template, one can assign
the RESTRICTED object to it. 

"""

def _clear_cache():
    PersonDTO._cache = {}
    RoleDTO._cache = {}
    EventDTO._cache = {}
    CategoryDTO._cache = {}
    AdDTO._cache = {}

class AdDTO:
    _cache = {}

    def _clone(clone):
        if not clone.id in AdDTO._cache:
            AdDTO._cache[clone.id] = AdDTO(clone.id,
                                           content=clone.content) 
        return AdDTO._cache[clone.id]

    def _clones(clones):
        return list(map(lambda o: AdDTO._clone(o),clones))

    def copy(copy, bulk=False):
        a = AdDTO(copy.id, content=copy.content)
        if not bulk:
            _clear_cache()
        return a

    def copies(copies):
        r = list(map(lambda o: AdDTO.copy(o,bulk=True),copies))
        _clear_cache()
        return r

    def __init__(self,id,content=RESTRICTED):
        self.id=id
        self.content=content

class PersonDTO:
    _cache = {}

    def _clone(clone):
        if not clone.id in PersonDTO._cache:
            PersonDTO._cache[clone.id] = PersonDTO(clone.id,
                                                name=clone.name,
                                                surname=clone.surname,
                                                username=clone.username,
                                                password=clone.password,
                                                email=clone.email,
                                                gender=clone.gender) 
        return PersonDTO._cache[clone.id]
       

    def _clones(clones):
        return list(map(lambda o: PersonDTO._clone(o),clones))

    def copy(copy, bulk=False):
        if isinstance(copy,AnonymousUserMixin):
            return copy
        else:
            r = PersonDTO(copy.id,
                        name=copy.name,
                        surname=copy.surname,
                        username=copy.username,
                        password=copy.password,
                        email=copy.email,
                        gender=copy.gender,
                        roles=RoleDTO._clones(copy.roles),
                        events=EventDTO._clones(copy.events),
                        manages=EventDTO._clones(copy.manages),
                        attends=EventDTO._clones(copy.attends),
                        requests=EventDTO._clones(copy.requests),
                        subscriptions=CategoryDTO._clones(copy.subscriptions),
                        moderates=CategoryDTO._clones(copy.moderates),
                        logs=LogDTO._clones(copy.logs))
            if not bulk:
                    _clear_cache()
            return r

    def copies(copies):
        r = list(map(lambda o: PersonDTO.copy(o,bulk=True),copies))
        _clear_cache()
        return r

    def __init__(self,id,
                name=RESTRICTED, 
                surname=RESTRICTED, 
                username=RESTRICTED, 
                password=RESTRICTED,
                email=RESTRICTED,
                gender=RESTRICTED,
                roles=RESTRICTED,
                events=[],
                manages=[],
                attends=[],
                requests=[],
                subscriptions=[],
                moderates=[],
                logs=[]):
        self.id=id
        self.name=name
        self.surname=surname
        self.username=username
        self.password=password
        self.email=email
        self.gender=gender
        self.roles=list(set(roles))
        self.events=list(set(events))
        for e in events:
            e.owner=self
        self.manages=list(set(manages))
        for e in manages:
            if self not in e.managedBy:
                e.managedBy.append(self)
        self.attends=list(set(attends))
        for e in attends:
            if self not in e.attendants:
                e.attendants.append(self)
        self.requests=list(set(requests))
        for e in requests:
            if self not in e.requesters:
                e.requesters.append(self)
        self.subscriptions=list(set(subscriptions))
        for c in subscriptions:
            if self not in c.subscribers:
                c.subscribers.append(self)
        self.moderates=list(set(moderates))
        for c in moderates:
            if self not in c.moderators:
                c.moderators.append(self)
        self.logs=list(set(logs))
        for l in logs:
            l.user = self

    @property
    def role(self):
        if self.roles == RESTRICTED or self.roles == []:
            return RESTRICTED
        return self.roles[0]
    @role.setter
    def role(self,r):
        self.roles = [r]
    @property
    def managed(self):
        return list(set(self.events + self.manages))
    @property
    def is_authenticated(self):
        return True

class RoleDTO:
    _cache = {}

    def _clone(clone):
        if not clone.id in RoleDTO._cache:
            RoleDTO._cache[clone.id] = RoleDTO(clone.id,clone.name) 
        return RoleDTO._cache[clone.id]
       

    def _clones(clones):
        return list(map(lambda o: RoleDTO._clone(o),clones))

    def copy(copy, bulk=False):
        r = RoleDTO(copy.id,copy.name)
        if not bulk:
            _clear_cache()
        return r

    def copies(copies):
        return list(map(lambda o: RoleDTO.copy(o, bulk=True),copies))

    def __init__(self, id, name):
        self.id=id
        self.name=name
           

class EventDTO:
    _cache = {}

    def _clone(clone):
        if not clone.id in EventDTO._cache:
            EventDTO._cache[clone.id] = EventDTO(clone.id,
                                                title=clone.title,
                                                description=clone.description) 
        return EventDTO._cache[clone.id]
       

    def _clones(clones):
        return list(map(lambda o: EventDTO._clone(o),clones))


    def copy(copy, bulk=False):
        r = EventDTO(copy.id,
                     title=copy.title,
                     description=copy.description,
                     owner=PersonDTO._clone(copy.owner),
                     categories=CategoryDTO._clones(copy.categories),
                     managedBy=PersonDTO._clones(copy.managedBy),
                     attendants=PersonDTO._clones(copy.attendants),
                     requesters=PersonDTO._clones(copy.requesters),
                     logs=LogDTO._clones(copy.logs))
        if not bulk:
            _clear_cache()
        return r

    def copies(copies):
        r = list(map(lambda o: EventDTO.copy(o,bulk=True),copies))
        _clear_cache()
        return r

    def __init__(self,id,
                title=RESTRICTED,
                description=RESTRICTED,
                owner=RESTRICTED,
                categories=[],
                managedBy=[],
                attendants=[],
                requesters=[],
                logs=[]):
        self.id=id
        self.title=title
        self.description=description
        self.owner=owner
        self.categories=list(set(categories))
        for c in categories:
                if self not in c.events:
                        c.events.append(self)
        self.managedBy=list(set(managedBy))
        for u in managedBy:
                if self not in u.manages:
                        u.manages.append(self)
        self.attendants=list(set(attendants))
        for u in attendants:
                if self not in u.attends:
                        u.attends.append(self)
        self.requesters=list(set(requesters))
        for u in requesters:
                if self not in u.requests:
                        u.requests.append(self)
        self.logs=list(set(logs))
        for l in logs:
            l.event = self

class CategoryDTO:
    _cache = {}

    def _clone(clone):
        if not clone.id in CategoryDTO._cache:
            CategoryDTO._cache[clone.id] = CategoryDTO(clone.id,
                                                name=clone.name) 
        return CategoryDTO._cache[clone.id]
       

    def _clones(clones):
        return list(map(lambda o: CategoryDTO._clone(o),clones))

    def copy(copy, bulk=False):
        r = CategoryDTO(copy.id,
                     name=copy.name,
                     subscribers=PersonDTO._clones(copy.subscribers),
                     moderators=PersonDTO._clones(copy.moderators),
                     events=EventDTO._clones(copy.events))
        if not bulk:
                _clear_cache()
        return r

    def copies(copies):
        r = list(map(lambda o: CategoryDTO.copy(o,bulk=True),copies))
        _clear_cache()
        return r

    def __init__(self,id,
                name=RESTRICTED,
                subscribers=[],
                moderators=[],
                events=[]):
        self.id=id
        self.name=name
        self.subscribers=list(set(subscribers))
        for u in subscribers:
                if self not in u.subscriptions:
                        u.subscriptions.append(self)
        self.moderators=list(set(moderators))
        for u in moderators:
                if self not in u.moderates:
                        u.moderates.append(self)
        self.events=list(set(events))
        for e in events:
                if self not in e.categories:
                        e.categories.append(self)


class LogDTO:
    _cache = {}

    def _clone(clone):
        if not clone.id in LogDTO._cache:
            LogDTO._cache[clone.id] = LogDTO(clone.id,
                                                timestamp=clone.timestamp) 
        return LogDTO._cache[clone.id]
       

    def _clones(clones):
        return list(map(lambda o: LogDTO._clone(o),clones))

    def copy(copy, bulk=False):
        r = LogDTO(copy.id,
                     copy.timestamp,
                     event=EventDTO._clone(copy.event),
                     user=PersonDTO._clone(copy.user))
        if not bulk:
                _clear_cache()
        return r

    def copies(copies):
        r = list(map(lambda o: LogDTO.copy(o,bulk=True),copies))
        _clear_cache()
        return r

    def __init__(self,id,timestamp,
                event=RESTRICTED,
                user=RESTRICTED):
        self.id=id
        self.timestamp=timestamp
        self.event=event
        if event != RESTRICTED:
            if self not in event.logs:
                event.logs.append(self)
        self.user=user
        if user != RESTRICTED:
            if self not in user.logs:
                user.logs.append(self)

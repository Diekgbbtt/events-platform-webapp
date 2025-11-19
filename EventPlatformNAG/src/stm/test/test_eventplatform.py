from dtm.compiler import compile as dcompile
from stm.compiler import compile as scompile
import pytest

data_model = """
entity Person {
    String name
    String surname
    String username
    String password
    
    Set(Event) events in Event_ownership
    Set(Event) manages in Event_managership
    Set(Event) attends in Event_attendance

    Set(Category) subscriptions in Category_subscription
    Set(Category) moderates in Category_moderate

    Set(Event) requests in Event_request
}

entity Event {
    String title
    String description
    Boolean private

    Person owner in Event_ownership
    Set(Person) managedBy in Event_managership
    Set(Person) attendants in Event_attendance

    Set(Category) categories in Event_category
    
    Set(Person) requesters in Event_request
}

entity Category {
    String name

    Set(Person) subscribers in Category_subscription
    Set(Person) moderators in Category_moderate

    Set(Event) events in Event_category
}
"""

security_model = """
USER Person

Role NONE {
    Person {
        create 

        update(username) [self.username = null]

        update(password) [self.password = null]

        update(role) [self.role = null and value = Role::FREEUSER]

        read(username), 
        read(password), 
        read(role) 
    }
}

Role VISITOR {
    Person {
        read(moderates) 
    }
    Event {
        read(private), 
        read(categories) 

        read(title), 
        read(description), 
        read(owner) [not self.private]
    }
    Category {
        read(name),
        read(moderators),
        read(events) 
    }
}

default Role FREEUSER extends VISITOR {
    Event {
        create

        update(private) [self.owner = caller and not value]
        
        read(title),
        read(description), 
        read(owner) [self.owner = caller or self.attendants->includes(caller)]

        add(categories),
        remove(categories),
        update(title),
        update(description) [self.managedBy->includes(caller)] 

        update(owner) [self.owner = null and value = caller]      

        read(attendants),
        read(managedBy) [not self.private or self.attendants->includes(caller)]

        add(managedBy) [caller = self.owner and (value = self.owner or self.attendants->includes(value))]

        remove(managedBy) [value <> caller and caller = self.owner]

	add(attendants) [value = self.owner 
                         or (self.managedBy->includes(caller) 
                         and self.requesters->includes(value))]
        remove(attendants) [(value = caller and caller <> self.owner and not self.managedBy->includes(caller))
                            or (value <> caller and self.owner <> value 
                                and not self.managedBy->includes(value) 
                                and self.managedBy->includes(caller))]
	
        add(requesters) [not self.private and value = caller]
        
        read(requesters) [self.managedBy->includes(caller)]
        
        remove(requesters) [self.managedBy->includes(caller) or value = caller]
    }
    Person {
	read(name),
        read(surname),
        read(username),
        read(role) 

        update(name),
        update(surname),
        update(username),
        update(password),
        read(events),
        read(manages),
        read(attends),
        read(requests),
        read(subscriptions) [caller = self]

        add(events) [value.owner = null]
    
        add(manages) [caller = value.owner and (self = value.owner or value.attendants->includes(self))]

        remove(manages) [self <> caller and caller = value.owner]

    	add(attends) [self = value.owner
      		      or (value.managedBy->includes(caller) and value.requesters->includes(self))]

        remove(attends) [(self = caller and caller <> value.owner 
                          and not value.managedBy->includes(caller))
                         or (self <> caller and value.owner <> self 
                             and not value.managedBy->includes(self) 
                             and value.managedBy->includes(caller))]

        remove(subscriptions),
        remove(moderates) [caller = self]

        add(requests) [not value.private and self = caller]

        remove(requests) [value.managedBy->includes(caller) or self = caller]
    }
    Category {
	remove(subscribers),
    	remove(moderators) [caller = value]

        add(events),
        remove(events) [value.managedBy->includes(caller)]
    }
}

Role PREMIUMUSER extends FREEUSER {
    Person {
        add(subscriptions) [caller = self]

        add(requests) [self = caller]
    }
    Event {
        add(requesters) [value = caller]

    	update(private) [self.owner = caller]
	
    }
    Category {
	add(subscribers) [caller = value]
    }
}

Role MODERATOR extends PREMIUMUSER {
    Event {
	remove(categories) [caller.moderates->includes(value)]
    }
    Category {
	read(subscribers) [self.moderators->includes(caller)]

        remove(events) [caller.moderates->includes(self)]
    }
}

Role ADMIN extends PREMIUMUSER {
    Person {
	update(role) [value <> null and value <> Role::NONE 
                      and value <> Role::VISITOR and (self.role <> Role::MODERATOR 
                                                      or self.moderates->isEmpty())]

        update(password),
        delete 

        add(moderates), remove(moderates) [self.role = Role::MODERATOR]     
    }
    Category {
	create,
    	delete,
    	update(name) 

    	add(moderators), 
	    remove(moderators) [value.role = Role::MODERATOR]
    }
}

Role SYSTEM {
    Person {
        fullAccess
    }
    Event {
        fullAccess
    }
    Category {
        fullAccess
    }
}
"""

@pytest.mark.safe
def test_EventPlatform():
    dm = dcompile(data_model)
    sm = scompile(dm,security_model)
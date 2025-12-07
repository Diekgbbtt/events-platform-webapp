# Copyright (c) 2025 All Rights Reserved
# Generated code

from flask import render_template, session
from flask_user import current_user
from stm import EventPlatformNAGSecurityModel
from model import Action
import inspect
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


class SecurityException(Exception):
    def __init__(self, msg = 'Not allowed by the securty model', page = 'error.html', params = {}):
        self.msg = msg
        self.page = page
        self.params = params

class PrivacyException(Exception):
    def __init__(self, msg = 'Not allowed by the privacy model', page = 'error.html', params = {}):
        self.msg = msg
        self.page = page
        self.params = params

def get_context():
    def __securecontext__():
        roles = {
            'VISITOR': EventPlatformNAGSecurityModel.Role.VISITOR,
            'REGULARUSER': EventPlatformNAGSecurityModel.Role.REGULARUSER,
            'PREMIUMUSER': EventPlatformNAGSecurityModel.Role.PREMIUMUSER,
            'MODERATOR': EventPlatformNAGSecurityModel.Role.MODERATOR,
            'ADMIN': EventPlatformNAGSecurityModel.Role.ADMIN,
            }
        c = current_user if not current_user.is_anonymous else None
        r = c.role if not c is None else EventPlatformNAGSecurityModel.Role.VISITOR
        return (c,roles[r.name])
    return __securecontext__()

def secure(db,ps):
    def f(func):
        def __securedentrypoint__(*args, **kwargs):
            pss = []
            for p in ps():
                pss.append(p.name)
                pss.extend(p.get_subpurposes_names())
            pss = list(set(pss))
            try:
                if 'purpose' not in session:
                    session['purpose'] = []
                session['purpose'].extend(pss)
                return func(*args, **kwargs)
            except (SecurityException, PrivacyException) as se:
                db.session.rollback()
                return render_template(se.page, security_violation = True, msg = se.msg, **se.params)
            finally:
                for i in range(len(pss)):
                    session['purpose'].pop()

        __securedentrypoint__.__name__ = func.__name__
        return __securedentrypoint__
    return f

def check_context(c):
    return '__securedentrypoint__' in c and '__securitycheck__' not in c and '__privacycheck__' not in c and '__securecontext__' not in c and 'orm_setup_cursor_result' not in c and '_initialize_instance' not in c

class SecuredAttribute():
        
    def __init__(self, attr, resource, sm, pm):
        self._attr = attr
        self._resource = resource
        self._sm = sm
        self._pm = pm

    def __getattr__(self, attr):
        return getattr(self._attr, attr)

    def __set__(self, instance, value):
        if not isinstance(value, list):
            context = list(map(lambda x: x.function, inspect.getouterframes(inspect.currentframe())))
            if check_context(context):    
                resource = instance
                caller, role = get_context()
                if hasattr(self._attr,'name'):
                    attr = self._attr.name 
                else:
                    # attr = self._attr.__str__().split(".")[-1]
                    attr = self._attr.fset.__name__
                purpose = session['purpose'] if 'purpose' in session else []
                if self._sm.permit(role,attr,Action.update,resource,caller,value):
                    if self._pm.permit(purpose,attr,Action.update,resource,caller,value):
                        self._attr.__set__(instance,value)
                    else:
                        resource = resource.__class__.__name__
                        raise PrivacyException(msg = f"It is not allowed to use attribute of the '{resource}' class for '{purpose}' purposes")

                else:
                    caller = "User '" + caller.username + "'" if caller is not None else "VISITOR user"
                    resource = resource.__class__.__name__
                    raise SecurityException(msg = f"{caller} with '{role.name}' role is not allowed to update attribute of the '{resource}' class")
            else:
                self._attr.__set__(instance,value) # SYSTEM actions - do not check
        else:
            self._attr.__set__(instance,value)


    def __delete__(self, instance):
        self._attr.__delete__(instance)

    def __get__(self, instance, owner):
        context = list(map(lambda x: x.function, inspect.getouterframes(inspect.currentframe())))
        if check_context(context):
            resource = instance
            caller, role = get_context()
            ret = self._attr.__get__(instance,owner)
            if isinstance(ret, list):
                attr = self._attr._annotations['proxy_key'] if hasattr(self._attr,'_annotations') else self._attr.fget.__name__
                purpose = session['purpose'] if 'purpose' in session else []
                return SecuredList(ret, self._attr, resource, self._sm, self._pm, (role, purpose, attr, Action.read, resource, caller))
            elif isinstance(self._attr,property):
                attr = self._attr.fget.__name__
                purpose = session['purpose'] if 'purpose' in session else []
                if self._sm.permit(role, attr, Action.read, resource, caller):
                    if self._pm.permit(purpose, attr, Action.read, resource, caller):
                        return ret
                    else:
                        # resource = resource.__class__.__name__
                        # raise PrivacyException(msg = f"It is not allowed to use '{attr}' attribute
                        # of the '{resource}' class for '{purpose}' purposes")
                        return Restrict()
                else:
                    # role = caller.role if not caller.is_anonymous else EventPlatformNAGSecurityModel.Role.VISITOR
                    # caller = "User '" + caller.username + "'" if not caller.is_anonymous else "VISITOR user"
                    # role = role.name
                    # resource = resource.__class__.__name__
                    # raise SecurityException(msg = f"{caller} with '{role}' role is not allowed to
                    # read '{attr}' attribute of the '{resource}' class")
                    return Restrict()
        
            else:
                if hasattr(self._attr,'name'):
                    attr = self._attr.name 
                else:
                    # attr = self._attr.__str__().split(".")[-1]
                    attr = self._attr.__name__
                purpose = session['purpose'] if 'purpose' in session else []
                if self._sm.permit(role, attr, Action.read, resource, caller):
                    if self._pm.permit(purpose, attr, Action.read, resource, caller):
                        return ret
                    else:
                        # resource = resource.__class__.__name__
                        # raise PrivacyException(msg = f"It is not allowed to use '{attr}' attribute
                        # of the '{resource}' class for '{purpose}' purposes")
                        return Restrict()
                else:
                    # role = caller.role if not caller.is_anonymous else EventPlatformNAGSecurityModel.Role.VISITOR
                    # caller = "User '" + caller.username + "'" if not caller.is_anonymous else "VISITOR user"
                    # role = role.name
                    # resource = resource.__class__.__name__
                    # raise SecurityException(msg = f"{caller} with '{role}' role is not allowed to
                    # read '{attr}' attribute of the '{resource}' class")
                    return Restrict()
        else:
            return self._attr.__get__(instance,owner) # SYSTEM actions - do not check

class SecureAccess:

    def __call__(self, target):
        qualified_names = ['_ctx', '_sm', '_pm', 'append', 'remove', '_list', '_attr', '_instance']
        orig_attr = target.__getattribute__
        def customgetattr(self, name):
            if name in qualified_names:
                return orig_attr(self, name)
            else:
                (role, purpose, attr, act, resource, caller) = self._ctx
                if self._sm.permit(role, attr, act, resource, caller):
                    if self._pm.permit(purpose, attr, act, resource, caller):
                        return orig_attr(self, name)
                    else: 
                        return Restrict()
                else:
                    return Restrict()
        target.__getattribute__ = customgetattr
        return target

@SecureAccess()
class SecuredList(list):

    def __init__(self, list, attr, instance, sm, pm, ctx):
        super().__init__(list)
        self._list = list
        self._attr = attr
        self._instance = instance
        self._sm = sm
        self._pm = pm
        self._ctx = ctx

    def check(self, func):
        (role, purpose, attr, act, resource, caller) = self._ctx
        if self._sm.permit(role, attr, act, resource, caller):
            if self._pm.permit(purpose, attr, act, resource, caller):
                return func()
            else: 
                return Restrict()
        else:
            return Restrict()

    def __len__(self):
        res = self.check(super().__len__)
        return res if type(res) is int else 0

    def __getitem__(self,key):
        return self.check(lambda: super().__getitem__(key))

    def __iter__(self):
        return self.check(super().__iter__)
    
    def __getattr__(self, attr):
        return getattr(self._list, attr)

    def __repr__(self) -> str:
        return f'{self._list}'

    def append(self, value):
        context = list(map(lambda x: x.function, inspect.getouterframes(inspect.currentframe())))
        if check_context(context):
            resource = self._instance
            caller, role = get_context()
            attr = self._attr._annotations['proxy_key'] if hasattr(self._attr,'_annotations') else self._attr.fget.__name__
            purpose = session['purpose'] if 'purpose' in session else []
            if self._sm.permit(role,attr,Action.add,resource,caller,value):
                if self._pm.permit(purpose,attr,Action.add,resource,caller,value):
                    self._list.append(value)
                else:
                    resource = resource.__class__.__name__
                    raise PrivacyException(msg = f"It is not allowed to use attribute of the '{resource}' class for '{purpose}' purposes")
            else:
                caller = "User '" + caller.username + "'" if caller is not None else "VISITOR user"
                resource = resource.__class__.__name__
                raise SecurityException(msg = f"{caller} with '{role.name}' role is not allowed to add value to the attribute of the '{resource}' class")
        else:
            self._list.append(value) # SYSTEM actions - do not check

    def remove(self, value):
        context = list(map(lambda x: x.function, inspect.getouterframes(inspect.currentframe())))
        if check_context(context):
            resource = self._instance
            caller, role = get_context()
            attr = self._attr._annotations['proxy_key'] if hasattr(self._attr,'_annotations') else self._attr.fget.__name__
            purpose = session['purpose'] if 'purpose' in session else []
            if self._sm.permit(role,attr,Action.remove,resource,caller,value):
                if self._pm.permit(purpose,attr,Action.remove,resource,caller,value):
                    self._list.remove(value)
                else:
                    resource = resource.__class__.__name__
                    raise PrivacyException(msg = f"It is not allowed to use attribute of the '{resource}' class for '{purpose}' purposes")
            else:
                caller = "User '" + caller.username + "'" if caller is not None else "VISITOR user"
                resource = resource.__class__.__name__
                raise SecurityException(msg = f"{caller} with '{role.name}' role is not allowed to remove value from attribute of the '{resource}' class")
        else:
            self._list.remove(value) # SYSTEM actions - do not check


def secure_init(i,sm,pm):
    def wrapper(self,*args,**kwargs):
        context = list(map(lambda x: x.function, inspect.getouterframes(inspect.currentframe())))
        if check_context(context):
            resource = self
            attr = self.__class__.__name__
            caller, role = get_context()
            # purpose = session['purpose'] if 'purpose' in session else []
            if sm.permit(role,attr,Action.create,resource,caller):
                # if pm.permit(purpose,attr,Action.create,resource,caller):
                return i(self,*args,**kwargs)
                # else:
                    # raise PrivacyException(msg = f"It is not allowed to use '{self.__class__.__name__}' class for '{purpose}' purposes")
            else:
                raise SecurityException(msg = f"{caller} with '{role.name}' role is not allowed to create instances of the '{self.__class__.__name__}' class")
        else:
            return i(self,*args,**kwargs) # SYSTEM actions - do not check
    return wrapper


class Secure:
    resources = {'Person': ['role', 'name', 'surname', 'gender', 'email', 'events', 'manages', 'attends', 'subscriptions', 'moderates', 'requests', 'logs', 'invitations', 'invites'], 'Event': ['title', 'description', 'owner', 'managedBy', 'attendants', 'requesters', 'categories', 'logs', 'invitations'], 'Category': ['name', 'subscribers', 'moderators', 'events'], 'Ad': ['content'], 'Log': ['timestamp', 'user', 'event'], 'Invite': ['invitee', 'invitedBy', 'event']}

    def __init__(self,sm,pm):
        self._sm = sm
        self._pm = pm
    def __call__(self,data):
        sm = self._sm
        pm = self._pm
        toProtect = Secure.resources[data.__name__]

        # Init
        i = getattr(data,'__init__')
        ii = secure_init(i,sm,pm)
        setattr(data,'__init__',ii)

        # Attributes and association ends
        for attr in toProtect:
            orig_attr = getattr(data,attr)
            new_attr = SecuredAttribute(orig_attr,data,sm,pm)
            setattr(data,attr,new_attr)


        return data

# Deletion interception
def setup_deletion_interception(db_session,sm,pm):
    original_delete = db_session.delete
    
    def intercepted_delete(instance):
        context = list(map(lambda x: x.function, inspect.getouterframes(inspect.currentframe())))
        if check_context(context) and instance.__class__.__name__ in Secure.resources.keys():
            resource = instance
            attr = instance.__class__.__name__
            caller, role = get_context()
            # purpose = session['purpose'] if 'purpose' in session else []
            if sm.permit(role,attr,Action.delete,resource,caller):
                # if pm.permit(purpose,attr,Action.delete,resource,caller):
                return original_delete(instance)
                # else:
                    # raise PrivacyException(msg = f"It is not allowed to use '{self.__class__.__name__}' class for '{purpose}' purposes")
            else:
                raise SecurityException(msg = f"{caller} with '{role.name}' role is not allowed to delete instances of the '{instance.__class__.__name__}' class")
        else:
            return original_delete(instance) # SYSTEM actions - do not check
                                             # Association deletions
    
    db_session.delete = intercepted_delete
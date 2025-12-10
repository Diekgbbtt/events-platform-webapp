# Copyright (c) 2025 All Rights Reserved
# Generated code

from model import Action, Constraint
from enum import auto, Enum
from privacy_model import PrivacyModel
import dtm

class EventPlatformNAGPrivacyModel(PrivacyModel):

    # Extensible model (default: nothing declared)

    class Purpose(Enum):
        
        RECOMMEND_EVENTS = auto()
        CORE = auto()
        FUNCTIONAL = auto()
        ANALYTICS = auto()
        STATS = auto()
        INSIGHTS = auto()
        TARGETED_MARKETING = auto()
        MASS_MARKETING = auto()
        MARKETING = auto()
        ANY = auto()
        
        

        def get_subpurposes_names(self):
            ret = []
            for sp in purpose_hierarchy[self]:
                ret.append(sp.name)
                ret.extend(sp.get_subpurposes_names())
            return ret

    personaldata = [
        {'resource': 'Person', 'subresource': 'name'},
        {'resource': 'Person', 'subresource': 'surname'},
        {'resource': 'Person', 'subresource': 'role'},
        {'resource': 'Person', 'subresource': 'gender'},
        {'resource': 'Person', 'subresource': 'email'},
        {'resource': 'Person', 'subresource': 'subscriptions'},
        {'resource': 'Person', 'subresource': 'logs'},
        {'resource': 'Person', 'subresource': 'attends'},
        {'resource': 'Log', 'subresource': 'event'}
        ]
        
    model = [(Purpose.MARKETING, [{'resource': 'Person', 'subresource': 'name'}], Constraint.fullAccess, 'true'), (Purpose.TARGETED_MARKETING, [{'resource': 'Person', 'subresource': 'gender'}], Constraint.fullAccess, 'true'), (Purpose.MASS_MARKETING, [{'resource': 'Person', 'subresource': 'email'}], Constraint.fullAccess, 'true'), (Purpose.STATS, [{'resource': 'Person', 'subresource': 'attends'}], lambda self= None: self.dot('attends').size() > 2, 'you attend more than two events'), (Purpose.STATS, [{'resource': 'Person', 'subresource': 'name'}], lambda self= None: self.dot('attends').size() > 2, 'you attend more than two events'), (Purpose.STATS, [{'resource': 'Person', 'subresource': 'subscriptions'}], lambda self= None: self.dot('attends').size() > 2, 'you attend more than two events'), (Purpose.ANALYTICS, [{'resource': 'Person', 'subresource': 'gender'}], Constraint.fullAccess, 'true'), (Purpose.FUNCTIONAL, [{'resource': 'Log', 'subresource': 'event'}], Constraint.fullAccess, 'true'), (Purpose.FUNCTIONAL, [{'resource': 'Person', 'subresource': 'attends'}], Constraint.fullAccess, 'true'), (Purpose.RECOMMEND_EVENTS, [{'resource': 'Person', 'subresource': 'subscriptions'}], lambda self= None: self.dot('role') == dtm.Role.REGULARUSER, 'you are a regularuser'), (Purpose.RECOMMEND_EVENTS, [{'resource': 'Person', 'subresource': 'logs'}], Constraint.fullAccess, 'true'), (Purpose.CORE, [{'resource': 'Person', 'subresource': 'name'}], Constraint.fullAccess, 'true'), (Purpose.CORE, [{'resource': 'Person', 'subresource': 'surname'}], Constraint.fullAccess, 'true'), (Purpose.CORE, [{'resource': 'Person', 'subresource': 'role'}], Constraint.fullAccess, 'true'), (Purpose.CORE, [{'resource': 'Person', 'subresource': 'gender'}], Constraint.fullAccess, 'true'), (Purpose.CORE, [{'resource': 'Person', 'subresource': 'email'}], Constraint.fullAccess, 'true'), (Purpose.CORE, [{'resource': 'Person', 'subresource': 'subscriptions'}], Constraint.fullAccess, 'true'), (Purpose.CORE, [{'resource': 'Person', 'subresource': 'logs'}], Constraint.fullAccess, 'true')]

purpose_hierarchy = {
    EventPlatformNAGPrivacyModel.Purpose.RECOMMEND_EVENTS: [
    ], 
    EventPlatformNAGPrivacyModel.Purpose.CORE: [
    ], 
    EventPlatformNAGPrivacyModel.Purpose.FUNCTIONAL: [
        EventPlatformNAGPrivacyModel.Purpose.RECOMMEND_EVENTS, 
        EventPlatformNAGPrivacyModel.Purpose.CORE
    ], 
    EventPlatformNAGPrivacyModel.Purpose.ANALYTICS: [
    ], 
    EventPlatformNAGPrivacyModel.Purpose.STATS: [
    ], 
    EventPlatformNAGPrivacyModel.Purpose.INSIGHTS: [
        EventPlatformNAGPrivacyModel.Purpose.STATS, 
        EventPlatformNAGPrivacyModel.Purpose.ANALYTICS
    ], 
    EventPlatformNAGPrivacyModel.Purpose.TARGETED_MARKETING: [
    ], 
    EventPlatformNAGPrivacyModel.Purpose.MASS_MARKETING: [
    ], 
    EventPlatformNAGPrivacyModel.Purpose.MARKETING: [
        EventPlatformNAGPrivacyModel.Purpose.TARGETED_MARKETING, 
        EventPlatformNAGPrivacyModel.Purpose.MASS_MARKETING
    ], 
    EventPlatformNAGPrivacyModel.Purpose.ANY: [
        EventPlatformNAGPrivacyModel.Purpose.FUNCTIONAL, 
        EventPlatformNAGPrivacyModel.Purpose.INSIGHTS, 
        EventPlatformNAGPrivacyModel.Purpose.MARKETING
    ]
}

EventPlatformNAGPrivacyModel.validate()
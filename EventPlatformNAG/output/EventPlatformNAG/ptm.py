# Copyright (c) 2025 All Rights Reserved
# Generated code

from model import Action, Constraint
from enum import auto, Enum
from privacy_model import PrivacyModel
import dtm

class EventPlatformNAGPrivacyModel(PrivacyModel):

    # Extensible model (default: nothing declared)

    class Purpose(Enum):
        
        pass
        

        def get_subpurposes_names(self):
            ret = []
            for sp in purpose_hierarchy[self]:
                ret.append(sp.name)
                ret.extend(sp.get_subpurposes_names())
            return ret

    personaldata = [
        ]
        
    model = [(Purpose.ANY, [{'resource': 'Person', 'subresource': 'name'}], Constraint.fullAccess, 'true'), (Purpose.ANY, [{'resource': 'Person', 'subresource': 'surname'}], Constraint.fullAccess, 'true'), (Purpose.ANY, [{'resource': 'Person', 'subresource': 'role'}], Constraint.fullAccess, 'true'), (Purpose.ANY, [{'resource': 'Person', 'subresource': 'gender'}], Constraint.fullAccess, 'true'), (Purpose.ANY, [{'resource': 'Person', 'subresource': 'email'}], Constraint.fullAccess, 'true'), (Purpose.ANY, [{'resource': 'Person', 'subresource': 'subscriptions'}], Constraint.fullAccess, 'true'), (Purpose.ANY, [{'resource': 'Person', 'subresource': 'logs'}], Constraint.fullAccess, 'true'), (Purpose.ANY, [{'resource': 'Log', 'subresource': 'event'}], Constraint.fullAccess, 'true'), (Purpose.MARKETING, [{'resource': 'Person', 'subresource': 'name'}], Constraint.fullAccess, 'true'), (Purpose.MARKETING, [{'resource': 'Person', 'subresource': 'gender'}], Constraint.fullAccess, 'true'), (Purpose.MARKETING, [{'resource': 'Person', 'subresource': 'email'}], Constraint.fullAccess, 'true'), (Purpose.TARGETED_MARKETING, [{'resource': 'Person', 'subresource': 'gender'}], Constraint.fullAccess, 'true'), (Purpose.MASS_MARKETING, [{'resource': 'Person', 'subresource': 'email'}], Constraint.fullAccess, 'true'), (Purpose.ANALYTICS, [{'resource': 'Person', 'subresource': 'gender'}], Constraint.fullAccess, 'true'), (Purpose.FUNCTIONAL, [{'resource': 'Log', 'subresource': 'event'}], Constraint.fullAccess, 'true'), (Purpose.FUNCTIONAL, [{'resource': 'Person', 'subresource': 'name'}], Constraint.fullAccess, 'true'), (Purpose.FUNCTIONAL, [{'resource': 'Person', 'subresource': 'surname'}], Constraint.fullAccess, 'true'), (Purpose.FUNCTIONAL, [{'resource': 'Person', 'subresource': 'role'}], Constraint.fullAccess, 'true'), (Purpose.FUNCTIONAL, [{'resource': 'Person', 'subresource': 'gender'}], Constraint.fullAccess, 'true'), (Purpose.FUNCTIONAL, [{'resource': 'Person', 'subresource': 'email'}], Constraint.fullAccess, 'true'), (Purpose.FUNCTIONAL, [{'resource': 'Person', 'subresource': 'subscriptions'}], Constraint.fullAccess, 'true'), (Purpose.FUNCTIONAL, [{'resource': 'Person', 'subresource': 'logs'}], Constraint.fullAccess, 'true'), (Purpose.RECOMMEND_EVENTS, [{'resource': 'Person', 'subresource': 'subscriptions'}], lambda self= None: self.dot('role') == dtm.Role.REGULARUSER, 'you are a regularuser'), (Purpose.RECOMMEND_EVENTS, [{'resource': 'Person', 'subresource': 'logs'}], Constraint.fullAccess, 'true'), (Purpose.CORE, [{'resource': 'Person', 'subresource': 'name'}], Constraint.fullAccess, 'true'), (Purpose.CORE, [{'resource': 'Person', 'subresource': 'surname'}], Constraint.fullAccess, 'true'), (Purpose.CORE, [{'resource': 'Person', 'subresource': 'role'}], Constraint.fullAccess, 'true'), (Purpose.CORE, [{'resource': 'Person', 'subresource': 'gender'}], Constraint.fullAccess, 'true'), (Purpose.CORE, [{'resource': 'Person', 'subresource': 'email'}], Constraint.fullAccess, 'true'), (Purpose.CORE, [{'resource': 'Person', 'subresource': 'subscriptions'}], Constraint.fullAccess, 'true'), (Purpose.CORE, [{'resource': 'Person', 'subresource': 'logs'}], Constraint.fullAccess, 'true')]

purpose_hierarchy = {
}

EventPlatformNAGPrivacyModel.validate()
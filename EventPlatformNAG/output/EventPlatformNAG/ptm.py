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
        
    model = []

purpose_hierarchy = {
}

EventPlatformNAGPrivacyModel.validate()
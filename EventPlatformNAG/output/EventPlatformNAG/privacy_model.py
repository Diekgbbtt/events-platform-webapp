# Copyright (c) 2025 All Rights Reserved
# Generated code

from model import Action
from flask_user import current_user
from ocl.ocl import eval_python as eval_ocl
from types import LambdaType

class PrivacyModel:

    class ModelError(Exception):
        pass

    # Checks permissions over the role hirearchy 
    @classmethod
    def permit(cls, aps, attr, act, self, caller, value=None):
        def __privacycheck__():
            data = self.__class__.__name__
            if hasattr(self, "owner") and any(pd['resource'] == data and pd['subresource'] == attr for pd in cls.personaldata):
                data = self.__class__.__name__
                if act == Action.read:
                    return cls.check2(aps, data, attr, caller, self)
                elif act == Action.update or act == Action.add or act == Action.remove:
                    return cls.check3(aps, data, attr, caller, self, value)  
                else:
                    return True # Unsupported actions: execute; Meaningless actions: create, delete
            else:
                return True
        return __privacycheck__()

    # def class_check(ls,data):
    #     for l in ls:
    #         d = l.get("resource", None)
    #         if d is not None:
    #             if data == d:
    #                 return True
    #     return False
    
    def resource_check(ls, data, attr):
        for l in ls:
            d = l.get("resource", None)
            a = l.get("subresource", None)
            if a is not None and d is not None:
                if data == d and attr == a:
                    return True
        return False

    # # For actions with 'caller' constraints only
    # @classmethod
    # def check1(cls, ap, data, caller):
    #     model = list(filter(lambda dp: PrivacyModel.class_check(dp[1], data) and eval_ocl(dp[2]), cls.model))
    #     dps = list(map(lambda dp: dp[0].name,model))
    #     consents = [c for c in current_user.consents if c.data.name == data]
    #     return cls.check(ap,dps,consents)

    # Example of a dp:
    # (Purpose.MARKETING, [{'resource': 'Person', 'subresource': 'name'}], Constraint.fullAccess, 'true')
    @classmethod
    def check2(cls, ap, data, attr, caller, self):
        model = list(filter(lambda dp: PrivacyModel.resource_check(dp[1], data, attr) and eval_ocl(dp[2],self=self), cls.model))
        dps = list(map(lambda dp: dp[0],model))
        if self.owner is not None:
            consents = [c for c in self.owner.consents if c.data.resource == data and c.data.subresource == attr]
            return cls.check_dp(ap, dps) and cls.check_cn(ap, consents)
        else:
            return cls.check_dp(ap, dps)

    @classmethod
    def check3(cls, ap, data, attr, caller, self, value):
        model = list(filter(lambda dp: PrivacyModel.resource_check(dp[1], data, attr) and eval_ocl(dp[2],self=self), cls.model))
        dps = list(map(lambda dp: dp[0],model))
        if self.owner is not None:
            consents = [c for c in self.owner.consents if c.data.resource == data and c.data.subresource == attr]
            return cls.check_dp(ap, dps) and cls.check_cn(ap, consents)
        else:
            return cls.check_dp(ap, dps)

    @classmethod
    def check_dp(cls, ap, dps):
        dpss = []
        for p in dps:
            dpss.append(p.name)
            dpss.extend(p.get_subpurposes_names())
        return set(ap).issubset(set(dpss))

    @classmethod
    def check_cn(cls, ap, consents):
        cps = [p for c in consents for p in c.purposes]
        cpss = []
        for p in cps:
            cpss.append(p.name)
            cpss.extend(p.get_subpurposes_names())
        return set(ap).issubset(set(cpss))

    # Extensible model (default: nothing declared)
    model = []

    # The following well-formed check will be performed on the privacy model
    # 1. The privacy model contains of the collection of privacy policies of the right format: 
    #     1a. Purpose is of type purpose
    #     1b. The data is the collection of different resources, in which, each of type dict and contains a resource, and a subresrouce
    #     1c. Constraint is of type Lambda
    #     1d. Description is of type string.
    @classmethod
    def validate(cls):

        def checkPurpose(p):
            if not isinstance(p, cls.Purpose):
                raise PrivacyModel.ModelError(f"Privacy policy purpose {p} should be of type Purpose")

        def checkResource(r):
            if not isinstance(r, str):
                raise PrivacyModel.ModelError(f"Privacy policy data resource {r} should be of type str")

        def checkSubResrouce(r):
            if not isinstance(r, str):
                raise PrivacyModel.ModelError(f"Privacy policy data subresource {r} should be of type str")

        def checkResourceData(data):
            if type(data) is dict:
                if 'resource' in data:
                    checkResource(data['resource'])
                else:
                    raise PrivacyModel.ModelError(f"Privacy data {data} should contain a resource")
                if 'subresource' in data:
                    checkSubResrouce(data['subresource'])
                else:
                    raise PrivacyModel.ModelError(f"Privacy data {data} should contain a subresource")
            else:
                raise PrivacyModel.ModelError(f"Privacy resource {resource} should be of type dict")

        def checkLambda(l):
            if not type(l) is LambdaType:
                raise PrivacyModel.ModelError(f"Constraint {l} should be of type LambdaType")

        def checkData(d):
            [checkResourceData(data) for data in d]

        def checkDesc(d):
            if not isinstance(d, str):
                raise PrivacyModel.ModelError(f"Privacy policy description {d} should be of type str")

        def checkPrivacyPolicy(p):
            checkPurpose(p[0])
            checkData(p[1])
            checkLambda(p[2])
            checkDesc(p[3])

        def checkPrivacyModel(dp,pd):
            [checkPrivacyPolicy(p) for p in dp] # declared purposes
            [checkResourceData(p) for p in pd] # personal data
        
        checkPrivacyModel(cls.model,cls.personaldata)
# Copyright (c) 2025 All Rights Reserved
# Generated code

from instrumentation import secure
from dtm import Person, Event, Category, Ad, Log, Invite, db
from app import P












@secure(db,P(['RECOMMEND_EVENTS']))
def recommend_events(args={}):
    return Person.recommend_events(args)


@secure(db,P(['MASS_MARKETING']))
def send_advertisement_to_user(args={}):
    return Person.send_advertisement_to_user(args)






















@secure(db,P(['CORE']))
def get_candidates(args={}):
    return Category.get_candidates(args)





@secure(db,P(['TARGETED_MARKETING', 'MARKETING']))
def get_personalize_ad(args={}):
    return Ad.get_personalize_ad(args)






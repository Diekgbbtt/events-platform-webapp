# Copyright (c) 2025 All Rights Reserved
# Generated code

from application import app
from flask import render_template, redirect, url_for, request, jsonify
from flask_user import UserManager, user_registered, login_required, current_user
from dtm import {% for c in dm -%}{% if not c.isAssociation %}{{c.class}}, {% endif %}{% endfor %}db
from dtm import {% for r in sm.roles -%} {{r.name}}, {% endfor %}Role
from dtm import {% for p in pm.purposes -%} {{p.name}}, {% endfor %}Purpose, Consent, PersonalData
from instrumentation import SecurityException, secure
from ptm import {{projectname}}PrivacyModel
import logging

@user_registered.connect_via(app)
def after_user_registered_hook(sender, user, **extra):
    role = Role.query.filter_by(name={{- sm.defaultRole}}).one()
    user.role=role
    db.session.commit()

db.init_app(app)

# Silence passlib warning due to Flask-User not using the latest passlib version
logging.getLogger('passlib').setLevel(logging.ERROR)

with app.app_context():
    db.create_all()

    roles = Role.query.all()
    if len(roles) == 0:
        {% for r in sm.roles -%} 
        db.session.add(Role(name={{- r.name}}))
        {% endfor -%}
        db.session.commit()

    purposes = Purpose.query.all()
    if len(purposes) == 0:
        {% for p in pm.purposes -%} 
        db.session.add(Purpose(name={{- p.name}}))
        {% endfor -%}
        db.session.commit()
        {% for p in pm.purposes -%} 
        p = Purpose.query.filter_by(name={{- p.name}}).first()
        {% for sp in p.includes -%} 
            p.subpurposes.append(Purpose.query.filter_by(name={{- sp}}).first())
        {% endfor -%}
        db.session.commit()
        {% endfor %}
    personaldata = PersonalData.query.all()
    if len(personaldata) == 0:
        {% for p in pm.personalData -%} 
        db.session.add(PersonalData(resource='{{p['resource']}}', subresource='{{p['subresource']}}'))
        {% endfor -%}
        db.session.commit()

    def P(ls):
        def lazy():
            return list(map(lambda x: Purpose.query.filter_by(name=x).first(),ls))
        return lazy

user_manager = UserManager(app, db, {{- sm.userClass}})

# ENDPOINTS

def build_purpose_hierarchy(model):
    purpose_hierarchy = {}
    all_purposes = set()
    sub_purposes = set()
    for p, rs, _, d in model:
        purpose = Purpose.query.filter_by(name=p.name).first()
        all_purposes.add(purpose.name)
        if purpose.name not in purpose_hierarchy:
            purpose_hierarchy[purpose.name] = []
        subpurposes = purpose.subpurposes if hasattr(purpose, 'subpurposes') else []
        for subpurpose in subpurposes:
            if subpurpose.name not in purpose_hierarchy[purpose.name]:
                purpose_hierarchy[purpose.name].append(subpurpose)
            if subpurpose.name not in purpose_hierarchy:
                purpose_hierarchy[subpurpose.name] = []
            sub_purposes.add(subpurpose.name)
    top_level_purposes = list(all_purposes - sub_purposes)
    return purpose_hierarchy, top_level_purposes

def find_personal_data(resource, subresource):
    pds = list(PersonalData.query.all())
    for pd in pds:
        if pd.resource == resource and pd.subresource == subresource:
            return pd
    return None

@app.get('/policy')
@login_required
@secure(db,P([]))
def policy():
    consents = Consent.query.filter_by(user_id=current_user.id).all()
    model = {{projectname}}PrivacyModel.model
    hierarchymodel, toplevel = build_purpose_hierarchy(model)
    newmodel = {}
    tmpmodel = {}
    for p,rs,_,d in model:
        purpose = Purpose.query.filter_by(name=p.name).first()

        for r in rs:
            data = find_personal_data(r['resource'],r['subresource'])
            c = list(filter((lambda x: purpose in x.purposes and x.data == data),consents))
            a = r.get("subresource",r.get("ends", None))
            r = r["resource"]
            c = c[0] if len(c) > 0 else None
            if  tmpmodel.get((purpose,r,d,c),None) != None and a != None:
                tmpmodel[(purpose,r,d,c)].append(a)
            else:
                tmpmodel[(purpose,r,d,c)] = [a] if a != None else []

    for k in tmpmodel.keys():
        (p,r,d,c) = k
        a = tmpmodel[k]
        if p not in newmodel:
            newmodel[p] = [(a,r,d,c)]
        else:
            newmodel[p].append((a,r,d,c))
    return render_template('privacy.html', model=newmodel, hierarchymodel=hierarchymodel, toplevel=toplevel)

@app.route('/add_consent/<int:purposeid>', methods=['POST'])
@login_required
# @secure(db,P([]))
def add_consent(purposeid):
    data = request.get_json()
    pd = find_personal_data(data.get('personalData'), data.get('classData'))
    p = Purpose.query.filter_by(id=purposeid).first()
    c = Consent.query.filter_by(user_id=current_user.id,data=pd).first()
    
    if c is not None and p in c.purposes:
        return redirect(url_for('policy'))
    c = Consent(data=pd, user=current_user)
    c.purposes.append(p)
    db.session.add(c)
    db.session.commit()
    return redirect(url_for('policy'))

@app.route('/remove_consent/<int:purposeid>', methods=['DELETE'])
@login_required
# @secure(db,P([]))
def remove_consent(purposeid):
    data = request.get_json()
    pd = find_personal_data(data.get('personalData'), data.get('classData'))
    p = Purpose.query.filter_by(id=purposeid).first()
    cs = Consent.query.filter_by(user_id=current_user.id,data=pd).all()

    for c in cs:
        if p in c.purposes:
            db.session.delete(c)
    db.session.commit()

    return jsonify({ 'success': True })
def error():
    msg = "You are not allowed to access this page: Not a User"
    return render_template('error.html', message = msg)

@app.route('/')
@secure(db,P({{- get_purpose('main')}}))
def main():
    from project import main 
    return main(request)
{% for c in dm if not c.isAssociation %}
{%- for m in c.methods %}
{%- if m.entry %}
@app.route('/{{- m.name}}', methods=['POST', 'GET'])
@secure(db,P({{- get_purpose(m.name)}}))
def {{m.name}}():
    return {{c.class}}.{{m.name}}(request)
{% endif %}
{% endfor %}
{%- endfor %}

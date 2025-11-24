###############################################################
#                                                             #
#                       NuActionGUI Tool                      #
#                                                             #
###############################################################
# Organization: InfSec Group, D-INFK, ETH Zurich              #
# Authors:      Srdan Krstic, Hoang Nguyen                    #
# License:      MIT License                                   #
#                                                             #
# Description:                                                #
# Simple Py generator for privacy enhanced web applications   #
#                                                             #
###############################################################

#!/usr/bin/env python3

import os
import shutil
import re
from jinja2 import Environment, FileSystemLoader, select_autoescape

"""
Simple Python generator for privacy enhanced web applications
"""
BASE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

"""
Directory navigation
"""
def clean_dir(*path):
    dir = os.path.join(BASE_DIRECTORY, *path)
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)

def set_working_directory(*path):
    dir = os.path.join(BASE_DIRECTORY, *path)
    os.chdir(dir)

"""
Auxiliary functions
"""

types = {"String":'db.String(100, collation="NOCASE")',
         "Boolean":'db.Boolean',
         "Integer":'db.Integer',
         "None": "NoneType"}

def model_type(t):
    """
    Get Python corresponding types
    """
    if t in types:
        return types[t]
    return t


def isPersonalData(c, pm):
    """
    return True if c is a personalData w.r.t. model pm
    """
    for p in pm['personalData']:
        if p['resource'] == c['class']:
            return True
    return False

def label(c,met,pm):
    """
    label actual purposes to method met of class c w.r.t. model pm
    """
    # TODO: Extend with the multiple purposes
    for p in pm['purposes']:
        for end in p['endpoints']:
            if end['class'] == c['class'] and end['met'] == met:
                return f"(purpose=\"p['name']\")"
    return ""

def isUserClass(c,sm):
    uc = sm.get('userClass',"User")
    return c['class'] == uc


### Main generator

def generate_class(projectname,dm,sm,pm,of,re):
    """
    Generate class
    """
    class_file = os.path.join(BASE_DIRECTORY, of, projectname, f"dtm.py")
    app_file = os.path.join(BASE_DIRECTORY, of, projectname, f"app.py")
    app_aux_file = os.path.join(BASE_DIRECTORY, of, projectname, f"auxiliary.py")
    project_file = os.path.join(BASE_DIRECTORY, of, projectname, f"project.py")
    project_aux_file = os.path.join(BASE_DIRECTORY, of, projectname, f"project_aux.py")
    application_file = os.path.join(BASE_DIRECTORY, of, projectname, f"application.py")

    set_working_directory("resources", "templates", "dm")
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape()
    )

    t = env.get_template("template.py")
    t.globals['type'] = model_type
    t.globals['label'] = label
    t.globals['isPersonalData'] = isPersonalData
    t.globals['isUserClass'] = isUserClass

    render = t.render(projectname=projectname,dm=dm,sm=sm,pm=pm)

    with open(class_file,"w+",encoding="utf-8") as f:
        f.write(render)


    def get_purpose(m):
        ret = {}
        for p in pm["purposes"]:
            for e in p["endpoints"]:
                if e["met"] not in ret:
                    ret[e["met"]] = []
                ret[e["met"]].append(p["name"])
        return ret.get(m,[])
    
    t = env.get_template("app.py")
    t.globals['type'] = type
    t.globals['label'] = label
    t.globals['isPersonalData'] = isPersonalData
    t.globals['isUserClass'] = isUserClass
    t.globals['get_purpose'] = get_purpose

    render = t.render(projectname=projectname,dm=dm,sm=sm,pm=pm)

    with open(app_file,"w+",encoding="utf-8") as f:
        f.write(render)

    t = env.get_template("auxiliary.py")
    t.globals['type'] = type
    t.globals['label'] = label
    t.globals['isPersonalData'] = isPersonalData
    t.globals['isUserClass'] = isUserClass
    t.globals['get_purpose'] = get_purpose

    render = t.render(projectname=projectname,dm=dm,sm=sm,pm=pm)

    with open(app_aux_file,"w+",encoding="utf-8") as f:
        f.write(render)

    if not re:
        t = env.get_template("project.py")
        t.globals['type'] = type
        t.globals['label'] = label
        t.globals['isPersonalData'] = isPersonalData
        t.globals['isUserClass'] = isUserClass
        t.globals['get_purpose'] = get_purpose

        render = t.render(projectname=projectname,dm=dm,sm=sm,pm=pm)

        with open(project_file,"w+",encoding="utf-8") as f:
            f.write(render)

        t = env.get_template("project_aux.py")
        t.globals['type'] = type
        t.globals['label'] = label
        t.globals['isPersonalData'] = isPersonalData
        t.globals['isUserClass'] = isUserClass
        t.globals['get_purpose'] = get_purpose

        render = t.render(projectname=projectname,dm=dm,sm=sm,pm=pm)

        with open(project_aux_file,"w+",encoding="utf-8") as f:
            f.write(render)

    t = env.get_template("application.py")

    render = t.render()

    with open(application_file,"w+",encoding="utf-8") as f:
        f.write(render)

aAuth = {
    "true"  : "Constraint.fullAccess",
    "false" : "Constraint.noAccess",
}

def refactor_security_policies(security_policies, datamodel):
    return security_policies



def get_resources(dm,sm):
    resources = {}
    for c in dm:
        if "isAssociation" in c:
            c0 = c["ends"][0]["target"]
            c1 = c["ends"][1]["target"]
            if c0 not in resources:
                resources[c0] = []
            resources[c0] += [c["ends"][1]["name"]]
            if c1 not in resources:
                resources[c1] = []
            resources[c1] += [c["ends"][0]["name"]]

        elif "isEnum" in c:
            # Skip enumerations or process them differently if needed
            continue

        else:
            if c["class"] not in resources:
                if c["class"] == sm.get('userClass',"User"):
                    resources[c["class"]] = ['role']
                else:
                    resources[c["class"]] = []
            resources[c["class"]] += list(map(lambda a: a["name"],c["attributes"]))


    return resources

def r(text):
    return re.sub(r'\'\(lambda(.*?)\)\'', r'lambda\1', text)

def rrrr(text):
    return re.sub(r'\"\(lambda(.*?)\)\"', r'lambda\1', text)

def rr(text):
    return re.sub(r'\'Role\.([_a-zA-Z][_a-zA-Z0-9]*)\'', r'Role.\1', text)

def rrr(text):
    return re.sub(r'\'Purpose\.([_a-zA-Z][_a-zA-Z0-9]*)\'', r'Purpose.\1', text)


def set_up_security(projectname,dm,sm,pm,of):
    filenames = ['instrumentation', 'security_model', 'template']

    set_working_directory("resources", "templates", "sm")
    env = Environment(
            loader=FileSystemLoader("."),
            autoescape=select_autoescape()
        )
    env.filters['r'] = r
    env.filters['rr'] = rr
    env.filters['rrrr'] = rrrr
    

    for filename in filenames:
        target = os.path.join(BASE_DIRECTORY, of, projectname, f"stm.py") if filename == "template" else os.path.join(BASE_DIRECTORY, of, projectname, f"{filename}.py")
        
        if os.path.exists(target):
            os.remove(target)

        policy = refactor_security_policies(sm["policy"], dm) if filename == "template" else ""
        resources = get_resources(dm,sm) if filename == "instrumentation" else ""
        
        t = env.get_template(f"{filename}.py")
        
        render = t.render(projectname=projectname,dm=dm,pm=pm,sm=sm,policy=policy,resources=resources)
        with open(target,"w+",encoding="utf-8") as f:
            f.write(render)

    

def set_up_aux(projectname,dm,of):
    
    set_working_directory("resources", "templates", "auxiliary")
    
    application_user_target = os.path.join(BASE_DIRECTORY, of, projectname)

    shutil.copy('model.py', os.path.join(application_user_target, 'model.py'))
    shutil.copytree('templates', os.path.join(application_user_target,'templates'))
    shutil.copytree('static', os.path.join(application_user_target,'static'))
    
    env = Environment(
            loader=FileSystemLoader("."),
            autoescape=select_autoescape()
    )

    set_working_directory("resources", "templates", "auxiliary", "templates")

    t = env.get_template("template.html")
    
    render = t.render(projectname=projectname)
    target = os.path.join(application_user_target,'templates', "template.html")
    with open(target,"w+",encoding="utf-8") as f:
        f.write(render)

    t = env.get_template("main.html")
    
    flatten = lambda x: [y for z in x for y in z]
    endpoints = flatten(
        list(map(
            lambda c: list(
                map(lambda d: d["name"], filter(lambda m: m.get("entry", False), c["methods"]))
            ),
            filter(lambda c: "methods" in c, dm)
        ))
    )
    endpoints = list(map(lambda e: "    <a class=\"list-group-item list-group-item-action\" href={{ url_for('" + e + "') }}>" + e + "</a>",endpoints))
    render = t.render(projectname=projectname,endpoints=endpoints)
    target = os.path.join(application_user_target,'templates', "main.html")
    with open(target,"w+",encoding="utf-8") as f:
        f.write(render)

        

def refactor_privacy(pm):
    ret = []
    for l in pm["policy"]:
        ocl = aAuth[l["constraint"]["ocl"]] if l["constraint"]["ocl"] in aAuth else l["constraint"]["ocl"]
        desc = "true" if l["constraint"]["ocl"] in aAuth else l["constraint"]["desc"]
        ret.append(("Purpose."+l["purpose"], l["resources"], ocl, desc))
    return ret


def set_up_privacy(projectname,dm,sm,pm,of):

    set_working_directory("resources", "templates", "pm")
    application_user_target = os.path.join(BASE_DIRECTORY, of, projectname)

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape()
    )
    env.filters['r'] = r
    env.filters['rrr'] = rrr
    env.filters['rrrr'] = rrrr

    t = env.get_template("privacy_model.py")
    target = os.path.join(application_user_target, "privacy_model.py")
    
    if os.path.exists(target):
        os.remove(target)
        
    render = t.render(projectname=projectname,dm=dm,pm=pm,sm=sm)
    with open(target,"w+",encoding="utf-8") as f:
        f.write(render)

    t = env.get_template("template.py")
    target = os.path.join(application_user_target, "ptm.py")
    
    if os.path.exists(target):
        os.remove(target)

    policy = refactor_privacy(pm)
        
    render = t.render(projectname=projectname,dm=dm,pm=pm,sm=sm, policy=policy)
    with open(target,"w+",encoding="utf-8") as f:
        f.write(render)


   
def generate_project(projectname,dm,sm,pm,of,re):
    """
    Code generation from models
    """
    set_up_security(projectname,dm,sm,pm,of)
    set_up_privacy(projectname,dm,sm,pm,of)
    if not re:
        set_up_aux(projectname,dm,of)
    generate_class(projectname,dm,sm,pm,of,re)

def transform(name,dm,sm,pm,re,of):
    if not re:
        of_path = os.path.join(BASE_DIRECTORY, of)
        if not os.path.exists(of_path):
            os.mkdir(of_path)
        clean_dir(of, name)
    generate_project(name,dm,sm,pm,of,re)

    

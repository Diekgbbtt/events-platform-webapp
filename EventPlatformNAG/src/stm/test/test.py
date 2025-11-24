from dtm.compiler import compile as dcompile
from stm.compiler import compile as scompile
import pytest

data_model = """
entity Researcher{
    String name
    Boolean student
    Set(Integer) academic_years

    Set(Paper) recommendPapers()

    Set(Paper) papers in Authorship
    Set(Paper) reviews in Reviewership
    Set(Researcher) students in Advisorship
    Set(Researcher) advisers in Advisorship
}

entity Paper{
    String title
    Integer year
    Status status

    publish()
    assignReviewer(Researcher r)

    Set(Researcher) authors in Authorship
    Set(Researcher) reviewers in Reviewership
}

enum Status {
    SUBMITTED
    UNDER_REVIEW
    SHEPHERDING
    ACCEPTED
    REJECTED
}
"""

dm = dcompile(data_model)

### User class exists
@pytest.mark.safe
def test_user_class_not_exist_dtm():
    security_model = """
USER Not_researcher
default Role NORMAL{
    Researcher{
        read(name), update(name) [self = caller]
    }
    Paper{
        read(title) [self.published]
    }
}
Role COMMITTEE{    
}
Role CHAIR{    
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_user_class_exist_dtm():
    security_model = """
USER Researcher
default Role NORMAL{
    Researcher{
        read(name), update(name) [self = caller]
    }
    Paper{
        read(title) [self.published]
    }
}
Role COMMITTEE{    
}
Role CHAIR{    
}
"""
    sm = scompile(dm,security_model)

### Empty role
@pytest.mark.safe
def test_empty_role():
    security_model = """
USER Researcher
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)

### No default role
@pytest.mark.safe
def test_no_default_role():
    security_model = """
USER Researcher

Role COMMITTEE {    
}

Role CHAIR {    
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
### Two default roles
@pytest.mark.safe
def test_two_default_roles():
    security_model = """
USER Researcher

default Role COMMITTEE {    
}

default Role CHAIR {    
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)

### role hierarchy
@pytest.mark.safe
def test_role_hierarchy():
    security_model = """
USER Researcher

default Role COMMITTEE {    
}

Role CHAIR extends COMMITTEE {    
}
"""
    sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_role_hierarchy_invalid():
    security_model = """
USER Researcher

default Role COMMITTEE {    
}

Role CHAIR extends NOTCOMMITTEE {    
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_role_hierarchy_invalid_2():
    security_model = """
USER Researcher

default Role COMMITTEE extends COMMITTEE {    
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
### role name is wellformed
@pytest.mark.safe
def test_role_name_wellformedness():
    security_model = """
USER Researcher

default Role notProperRole {    
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_role_name_wellformedness_1():
    security_model = """
USER Researcher

default Role PROPER_ROLE {    
}
"""
    sm = scompile(dm,security_model)
        
## Test permissions without resource
@pytest.mark.safe
def test_fullAccess():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        fullAccess
    }
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_create():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        create
    }
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_delete():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        delete
    }
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_read():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        read
    }
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_update():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        update
    }
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_add():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        add
    }
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_remove():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        remove
    }
}
"""
    sm = scompile(dm,security_model)
    
def test_execute():
    security_model = """
USER Researcher

default Role ADMIN { 
    execute
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_all_actions():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        create
        delete
        read
        update
        add
        remove
        execute
    }
}
"""

## Test permissions with resource

@pytest.mark.safe
def test_read_resources():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        read(name), read(student), read(academic_years), read(papers), read(reviews),
        read(students), read(advisers)
    }
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_read_resources_invalid():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        read(notname)
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)

@pytest.mark.safe
def test_create_resources():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        create
    }
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_delete_resources():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        delete
    }
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_update_resources():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        update(name), update(student)
    }
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_update_resources_invalid():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        update(notname)
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
    
def test_update_resources_invalid_2():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        update(academic_years)
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_add_resources():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        add(students), add(papers)
    }
}
"""
    sm = scompile(dm,security_model)
    
def test_add_resources_1():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        add(academic_years)
    }
}
"""
    sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_add_resources_invalid():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        add(name)
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_remove_resources():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        remove(students), remove(papers)
    }
}
"""
    sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_remove_resources_invalid():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        remove(name)
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_remove_resources_invalid():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        remove(authors)
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)

## Checking OCL constraints
@pytest.mark.safe
def test_read_resources_ocl():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        read(name), read(student), read(academic_years), read(papers), read(reviews),
        read(students), read(advisers) [self = null]
    }
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_read_resources_ocl_1():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        read(name), read(student), read(academic_years), read(papers), read(reviews),
        read(students), read(advisers) [caller = null]
    }
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_read_resources_ocl_2():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        read(name), read(student), read(academic_years), read(papers), read(reviews),
        read(students), read(advisers) [target = null]
    }
}
"""   
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_read_resources_ocl_3():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        read(name), read(student), read(academic_years), read(papers), read(reviews),
        read(students), read(advisers) [value = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)

@pytest.mark.safe
def test_create_resources_ocl():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        create [self = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_create_resources_ocl_1():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        create [caller = null]
    }
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_create_resources_ocl_2():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        create [value = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_create_resources_ocl_3():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        create [target = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_delete_resources_ocl():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        delete [self = null]
    }
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_delete_resources_ocl_1():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        delete [caller = null]
    }
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_delete_resources_ocl_2():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        delete [value = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_delete_resources_ocl_3():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        delete [target = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_update_resources_ocl():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        update(name), update(student) [self = null]
    }
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_update_resources_ocl_1():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        update(name), update(student) [caller = null]
    }
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_update_resources_ocl_2():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        update(name), update(student) [value = null]
    }
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_update_resources_ocl_3():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        update(name), update(student) [target = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_add_resources_ocl():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        add(students) [self = null]
    }
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_add_resources_ocl_1():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        add(students) [caller = null]
    }
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_add_resources_ocl_2():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        add(students) [value = null]
    }
}
"""
    sm = scompile(dm,security_model)

    
@pytest.mark.safe
def test_add_resources_ocl_3():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        add(students) [target = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_remove_resources_ocl():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        remove(students) [self = null]
    }
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_remove_resources_ocl_1():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        remove(students) [caller = null]
    }
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_remove_resources_ocl_2():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        remove(students) [value = null]
    }
}
"""
    sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_remove_resources_ocl_3():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        remove(students) [target = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
    
@pytest.mark.safe
def test_create_read_ocl():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        create, read(name) [self = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_create_update_ocl():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        create, update(name) [self = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_create_update_ocl_1():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        create, update(name) [value = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_create_add_ocl():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        create, add(students) [self = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_create_add_ocl_1():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        create, add(students) [target = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_create_remove_ocl():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        create, remove(students) [self = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_create_remove_ocl_1():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        create, remove(students) [target = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_read_update_ocl():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        read(name), update(students) [value = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_read_update_ocl_1():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        read(name), update(students) [target = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_read_remove_ocl():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        read(name), add(students) [value = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_read_add_ocl_1():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        read(name), add(students) [target = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_read_remove_ocl():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        read(name), remove(students) [value = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_read_remove_ocl_1():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        read(name), remove(students) [target = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_update_add_ocl():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        update(name), add(students) [value = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_update_add_ocl_1():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        update(name), add(students) [target = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_update_remove_ocl():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        update(name), remove(students) [value = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)
        
@pytest.mark.safe
def test_update_remove_ocl_1():
    security_model = """
USER Researcher

default Role ADMIN { 
    Researcher{
        update(name), remove(students) [target = null]
    }
}
"""
    with pytest.raises(Exception):
        sm = scompile(dm,security_model)

# TODO: what to test
# lexer: ROLENAMES, Resourcenames, attributenames
# parser: check malformed models
# check role hirearchy
# well-formdness of the data model (name attribute is not in the Researcher)
#     - resource exists
#     - subresource exists
# well-formedness of authorization constraints
# well-formedness of actions (e.g., add(attribure) not allowed)
# multiple actions 
# composite actions (without subresource: read, update )
# End-to-end run with the transform.py

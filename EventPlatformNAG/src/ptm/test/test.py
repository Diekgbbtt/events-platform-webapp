from dtm.compiler import compile as dcompile
from stm.compiler import compile as scompile
from ptm.compiler import compile as pcompile
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

security_model = """
USER Researcher
default Role NORMAL{
}
Role COMMITTEE{    
}
Role CHAIR{    
}
"""

sm = scompile(dm,security_model)

### Personal data exists
@pytest.mark.safe
def test_personal_data_not_exist_dtm():
    privacy_model = """
Personal data { 
    Not_Researcher 
}
Purposes {}
Actual purposes {}
Declared purposes {}
"""
    with pytest.raises(Exception):
        pm = pcompile(dm,sm,privacy_model)
        
@pytest.mark.safe
def test_personal_data_exist_dtm():
    privacy_model = """
Personal data { 
    Researcher 
}
Purposes {}
Actual purposes {}
Declared purposes {}
"""
    pm = pcompile(dm,sm,privacy_model)

### Missing parts
@pytest.mark.safe
def test_no_personal_data():
    privacy_model = """
Purposes {}
Actual purposes {}
Declared purposes {}
"""
    with pytest.raises(Exception):
        pm = pcompile(dm,sm,privacy_model)

@pytest.mark.safe
def test_no_purposes():
    privacy_model = """
Personal data {}
Actual purposes {}
Declared purposes {}
"""
    with pytest.raises(Exception):
        pm = pcompile(dm,sm,privacy_model)

@pytest.mark.safe
def test_no_actual():
    privacy_model = """
Personal data {}
Purposes {}
Declared purposes {}
"""
    with pytest.raises(Exception):
        pm = pcompile(dm,sm,privacy_model)

@pytest.mark.safe
def test_no_declared():
    privacy_model = """
Personal data {}
Purposes {}
Actual purposes {}
"""
    with pytest.raises(Exception):
        pm = pcompile(dm,sm,privacy_model)

@pytest.mark.safe
def test_minimal_model():
    privacy_model = """
Personal data {}
Purposes {}
Actual purposes {}
Declared purposes {}
"""
    pm = pcompile(dm,sm,privacy_model)

### Purposes
@pytest.mark.safe
def test_simple_purpose():
    privacy_model = """
Personal data {}
Purposes {
    AA, BB, CC
}
Actual purposes {}
Declared purposes {}
"""
    pm = pcompile(dm,sm,privacy_model)

@pytest.mark.safe
def test_complex_purpose_1():
    privacy_model = """
Personal data {}
Purposes {
    AA includes BB CC, BB, CC
}
Actual purposes {}
Declared purposes {}
"""
    pm = pcompile(dm,sm,privacy_model)

@pytest.mark.safe
def test_complex_purpose_2():
    privacy_model = """
Personal data {}
Purposes {
    AA includes BB, BB includes CC, CC
}
Actual purposes {}
Declared purposes {}
"""
    pm = pcompile(dm,sm,privacy_model)


@pytest.mark.safe
def test_purpose_hierarchy_1():
    privacy_model = """
Personal data {}
Purposes {
    AA includes BB, BB includes CC, CC includes AA
}
Actual purposes {}
Declared purposes {}
"""
    with pytest.raises(Exception):
        pm = pcompile(dm,sm,privacy_model)

@pytest.mark.safe
def test_purpose_hierarchy_2():
    privacy_model = """
Personal data {}
Purposes {
    AA includes D, BB includes CC, CC 
}
Actual purposes {}
Declared purposes {}
"""
    with pytest.raises(Exception):
        pm = pcompile(dm,sm,privacy_model)

@pytest.mark.safe
def test_purpose_hierarchy_3():
    privacy_model = """
Personal data {}
Purposes {
    AA includes D, AA includes CC, CC, D
}
Actual purposes {}
Declared purposes {}
"""
    with pytest.raises(Exception):
        pm = pcompile(dm,sm,privacy_model)
        
## Actual purposes: Resources
@pytest.mark.safe
def test_actual_purpose_resource_exists():
    privacy_model = """
Personal data {}
Purposes {
    AA, BB, CC
}
Actual purposes {
    Paper.publish AA
}
Declared purposes {}
"""
    pm = pcompile(dm,sm,privacy_model)

@pytest.mark.safe
def test_actual_purpose_resource_does_not_exist():
    privacy_model = """
Personal data {}
Purposes {
    AA, BB, CC
}
Actual purposes {
    Not_Paper.publish AA
}
Declared purposes {}
"""
    with pytest.raises(Exception):
        pm = pcompile(dm,sm,privacy_model)

## Actual purposes: Subresources
@pytest.mark.safe
def test_actual_purpose_subresource_exists():
    privacy_model = """
Personal data {}
Purposes {
    AA includes BB, BB, CC
}
Actual purposes {
    Paper.assignReviewer AA
}
Declared purposes {}
"""
    pm = pcompile(dm,sm,privacy_model)

@pytest.mark.safe
def test_actual_purpose_subresource_does_not_exist():
    privacy_model = """
Personal data {}
Purposes {
    AA includes BB, BB, CC
}
Actual purposes {
    Paper.not_assignReviewer AA
}
Declared purposes {}
"""
    with pytest.raises(Exception):
        pm = pcompile(dm,sm,privacy_model)

## Actual purposes: Purposes
@pytest.mark.safe
def test_actual_purpose_exists():
    privacy_model = """
Personal data {}
Purposes {
    AA includes BB CC, BB, CC
}
Actual purposes {
    Paper.publish AA
}
Declared purposes {}
"""
    pm = pcompile(dm,sm,privacy_model)

@pytest.mark.safe
def test_actual_purpose_does_not_exist():
    privacy_model = """
Personal data {}
Purposes {
    AA, BB, CC
}
Actual purposes {
    Paper.publish D
}
Declared purposes {}
"""
    with pytest.raises(Exception):
        pm = pcompile(dm,sm,privacy_model)



## Declared purposes: Resources
@pytest.mark.safe
def test_declared_purpose_resource_exists():
    privacy_model = """
Personal data { Researcher }
Purposes {
    AA includes BB CC, BB, CC
}
Actual purposes {}
Declared purposes {
    Researcher.papers AA
}
"""
    pm = pcompile(dm,sm,privacy_model)

@pytest.mark.safe
def test_declared_purpose_resource_does_not_exist():
    privacy_model = """
Personal data { Researcher }
Purposes {
    AA includes BB CC, BB, CC
}
Actual purposes {}
Declared purposes {
    Not_Researcher.papers AA
}
"""
    with pytest.raises(Exception):
        pm = pcompile(dm,sm,privacy_model)


@pytest.mark.safe
def test_declared_purpose_resource_not_personal():
    privacy_model = """
Personal data { Researcher }
Purposes {
    AA includes BB CC, BB, CC
}
Actual purposes {}
Declared purposes {
    Paper.title AA
}
"""
    with pytest.raises(Exception):
        pm = pcompile(dm,sm,privacy_model)
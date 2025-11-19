from dtm.compiler import compile as dcompile
# from dtm.compiler import DataModelError
import pytest

### Empty datamodel
@pytest.mark.safe
def test_empty_dtm():
    data_model = """"""
    with pytest.raises(Exception):
        dm = dcompile(data_model)

### entity keyword correctly
@pytest.mark.safe
def test_invalid_entity_keyword():
    data_model = """
notentity Researcher {
    String name
}
    """
    with pytest.raises(Exception):
        dm = dcompile(data_model)

### entityname (i.e., TypeName) in right format
@pytest.mark.safe
def test_valid_entity_name():
    data_model = """
entity Researcher {
    String name
}
    """
    dm = dcompile(data_model)
    
@pytest.mark.safe
def test_invalid_entity_name():
    data_model = """
entity researcher {
    String name
}
    """
    with pytest.raises(Exception):
        dm = dcompile(data_model)
        
@pytest.mark.safe
def test_camel_entity_name():
    data_model = """
entity ResearcherPaper {
    String name
}
    """
    with pytest.raises(Exception):
        dm = dcompile(data_model)
        
@pytest.mark.safe
def test_valid_entity_name_1():
    data_model = """
entity Researcher_paper {
    String name
}
    """
    dm = dcompile(data_model)
    
### entity with empty properties
@pytest.mark.safe
def test_entity_with_empty_properties():
    data_model = """
entity Researcher {
}
    """
    dm = dcompile(data_model)

### two entities with same TypeName
@pytest.mark.safe
def test_two_entities_with_same_name():
    data_model = """
entity Researcher {
}

entity Researcher {
}
    """
    with pytest.raises(Exception):
        dm = dcompile(data_model)

### attribute with the wrong types
@pytest.mark.safe
def test_attribute_types():
    data_model = """
entity Researcher {
    string name
}
    """
    with pytest.raises(Exception):
        dm = dcompile(data_model)

### check if attribute with class type works if the class does not exist
@pytest.mark.safe
def test_attribute_valid_type_as_class():
    data_model = """
enum Role {
    ADMIN
}    
    
entity Researcher {
    Role name
}
    """
    dm = dcompile(data_model)

### check if attribute with class type works if the class does not exist
@pytest.mark.safe
def test_attribute_invalid_type_as_class():
    data_model = """
enum Role {
    ADMIN
}    
    
entity Researcher {
    SomeRole name
}
    """
    with pytest.raises(Exception):
        dm = dcompile(data_model)        

### nested collection types check
@pytest.mark.safe
def test_attribute_nested_collection_type():
    data_model = """
entity Researcher {
    Bag(Set(Sequence(OrderedSet(String)))) test
}
    """
    dm = dcompile(data_model) 
        
### same attribute names in the same entity
@pytest.mark.safe
def test_attributes_same_name():
    data_model = """
entity Researcher {
    String name
    String someotherthing
    Integer name
}
    """
    with pytest.raises(Exception):
        dm = dcompile(data_model)      

### association-ends exists in both ends in the Association!
@pytest.mark.safe
def test_both_ends_exists():
    data_model = """
entity Researcher{
    String name
    
    Set(Researcher) students in Advisorship
    Set(Researcher) advisers in Advisorship
}
    """
    dm = dcompile(data_model)  
        
        
@pytest.mark.safe
def test_both_ends_exists_1():
    data_model = """
entity Researcher{
    String name
    Set(Paper) papers in Authorship
}

entity Paper{
    Set(Researcher) author in Authorship
}
    """
    dm = dcompile(data_model)
          
        
@pytest.mark.safe
def test_both_ends_exists_invalid():
    data_model = """
entity Researcher{
    String name
    Set(Paper) papers in Authorship
}

entity Paper{
    Set(Researcher) author in NotAuthorship
}
    """
    with pytest.raises(Exception):
        dm = dcompile(data_model)  

### no same association-ends going from the same entity
@pytest.mark.safe
def test_both_ends_exists_in_same_class():
    data_model = """
entity Researcher{
    String name
    
    Set(Researcher) students in Advisorship
    Set(Researcher) students in Other_association
}
    """
    with pytest.raises(Exception):
        dm = dcompile(data_model)  
    
### can the propertyType attributes be a collectionType?
@pytest.mark.safe
def test_collection_as_collection_type():
    data_model = """
entity Researcher{
    Set(Integer) years
}
    """
    dm = dcompile(data_model)  

### function return nothing
@pytest.mark.safe
def test_function_void():
    data_model = """
entity Researcher{
    recommendPapers()
}
    """
    dm = dcompile(data_model)  

### function no duplication
@pytest.mark.safe
def test_functions_same_name():
    data_model = """
entity Researcher {
    recommendPapers()
    
    String recommendPapers()
}
    """
    with pytest.raises(Exception):
        dm = dcompile(data_model)  

### function contains 1 parameter
@pytest.mark.safe
def test_function_1_param():
    data_model = """
entity Researcher {
    recommendPapers(String researcherId)
}
    """
    dm = dcompile(data_model)  
        
### function contains 2 parameters
@pytest.mark.safe
def test_function_2_params():
    data_model = """
entity Researcher {
    recommendPapers(String researcherId, Integer paperId)
}
    """
    dm = dcompile(data_model)  
    
### function overlead works?
@pytest.mark.safe
def test_function_overload():
    data_model = """
entity Researcher {
    String recommendPapers()
    
    String recommendPapers(Integer researcherId)
}
    """
    dm = dcompile(data_model)  

### enum no duplication
@pytest.mark.safe
def test_enum_duplication():
    data_model = """
enum Role {
    NONE
}

enum Role {
    ADMIN
}
    """
    with pytest.raises(Exception):
        dm = dcompile(data_model)  

### empty enum
@pytest.mark.safe
def test_enum_empty():
    data_model = """
enum Role {
}
    """
    with pytest.raises(Exception):
        dm = dcompile(data_model)  
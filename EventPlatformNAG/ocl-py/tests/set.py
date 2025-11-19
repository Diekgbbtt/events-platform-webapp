from ocl.ocl import eval_ocl, OCLTerm
import pytest


## Basic types test

@pytest.mark.safe
def test_set_1():
    ocl_exp = "let x = Set{0, 1, 2, 3, 4} in x"
    assert (eval_ocl(ocl_exp)) == {0, 1, 2, 3, 4}
    
@pytest.mark.safe
def test_set_2():
    ocl_exp = "Set{0, 1, 2, 3, 4, 4, 3, 2, 1, 0}"
    assert (eval_ocl(ocl_exp)) == {0, 1, 2, 3, 4}
    
# An important issue here is that when the source collection is a Set the resulting collection is not a Set but a Bag.
@pytest.mark.safe
def test_set_collect():
    ocl_exp = "Set{0, 1, 2, 3, 4}->collect(e|e>3)"
    assert (eval_ocl(ocl_exp)) == [False, False, False, False, True]
    
@pytest.mark.safe
def test_set_collect_2():
    ocl_exp = "Set{0, 1, 2, 3, 4}->collect(e|e+3)"
    assert (eval_ocl(ocl_exp)) == [3, 4, 5, 6, 7]
    
@pytest.mark.safe
def test_set_excludes():
    ocl_exp = "Set{0, 1, 2, 3, 4}->excludes(3)"
    assert (eval_ocl(ocl_exp)) == False   
    
@pytest.mark.safe
def test_set_excludes_2():
    ocl_exp = "Set{0, 1, 2, 3, 4}->excludes(5)"
    assert (eval_ocl(ocl_exp)) == True 
   
@pytest.mark.safe
def test_set_exists():
    ocl_exp = "Set{0, 1, 2, 3, 4}->exists(e|e>3)"
    assert (eval_ocl(ocl_exp)) == True 

@pytest.mark.safe    
def test_set_exists_2():
    ocl_exp = "Set{0, 1, 2, 3, 4}->exists(e|e>6)"
    assert (eval_ocl(ocl_exp)) == False
    
@pytest.mark.safe
def test_set_forAll():
    ocl_exp = "Set{0, 1, 2, 3, 4}->forAll(e|e>3)"
    assert (eval_ocl(ocl_exp)) == False 
    
@pytest.mark.safe
def test_set_forAll_2():
    ocl_exp = "Set{0, 1, 2, 3, 4}->forAll(e|e<6)"
    assert (eval_ocl(ocl_exp)) == True 
    
@pytest.mark.safe
def test_set_includes():
    ocl_exp = "Set{0, 1, 2, 3, 4}->includes(3)"
    assert (eval_ocl(ocl_exp)) == True   

@pytest.mark.safe
def test_set_includes_2():
    ocl_exp = "Set{0, 1, 2, 3, 4}->includes(7)"
    assert (eval_ocl(ocl_exp)) == False   
    
@pytest.mark.safe
def test_set_isEmpty():
    ocl_exp = "Set{0, 1, 2, 3, 4}->isEmpty()"
    assert (eval_ocl(ocl_exp)) == False   
    
@pytest.mark.safe
def test_set_isEmpty_2():
    ocl_exp = "Set{}->isEmpty()"
    assert (eval_ocl(ocl_exp)) == True  
    
@pytest.mark.safe
def test_set_notEmpty():
    ocl_exp = "Set{0, 1, 2, 3, 4}->notEmpty()"
    assert (eval_ocl(ocl_exp)) == True  
    
@pytest.mark.safe
def test_set_notEmpty_2():
    ocl_exp = "Set{}->notEmpty()"
    assert (eval_ocl(ocl_exp)) == False  
    
@pytest.mark.safe
def test_set_select():
    ocl_exp = "Set{0, 1, 2, 3, 4}->select(e|e>6)"
    assert (eval_ocl(ocl_exp)) == set()
    
@pytest.mark.safe
def test_set_select_2():
    ocl_exp = "Set{0, 1, 2, 3, 4}->select(e|e>3)"
    assert (eval_ocl(ocl_exp)) == {4}
    
@pytest.mark.safe
def test_set_reject():
    ocl_exp = "Set{0, 1, 2, 3, 4}->reject(e|e>6)"
    assert (eval_ocl(ocl_exp)) == {0, 1, 2, 3, 4}
    
@pytest.mark.safe
def test_set_reject_2():
    ocl_exp = "Set{0, 1, 2, 3, 4}->reject(e|e>3)"
    assert (eval_ocl(ocl_exp)) == {0, 1, 2, 3}
    
@pytest.mark.safe
def test_set_size():
    ocl_exp = "Set{0, 1, 2, 3, 4}->size()"
    assert (eval_ocl(ocl_exp)) == 5
    
@pytest.mark.safe
def test_set_size_2():
    ocl_exp = "Set{}->size()"
    assert (eval_ocl(ocl_exp)) == 0
    
## Object types test

class A(OCLTerm):
    student = False
    
    def __init__(self, t) -> None:
        self.flag = t

    @classmethod
    def allInstances(cls) -> set:
        return set()
        
obj1 = A('t1')
obj2 = A('t2')
obj3 = A('t1')
obj4 = A('t3')

@pytest.mark.safe
def test_set_3():
    ocl_exp = "Set{a, b, c}"
    result = eval_ocl(ocl_exp, a=obj1, b=obj2, c=obj3)
    assert (result) == {obj1, obj2}

@pytest.mark.safe
def test_set_collect_3():
    ocl_exp = "Set{a, b, c}->collect(o|o.flag)"
    result = eval_ocl(ocl_exp, a=obj1, b=obj2, c=obj3)
    assert (result == ['t1','t2'] or ['t2','t1'] == result)

@pytest.mark.safe
def test_set_excludes_3():
    ocl_exp = "Set{a, b, c}->excludes(d)"
    assert (eval_ocl(ocl_exp, a=obj1, b=obj2, c=obj3, d=obj1)) == False

@pytest.mark.safe
def test_set_exists_3():
    ocl_exp = "Set{a, b, c}->exists(o|o.flag = 't1')"
    assert (eval_ocl(ocl_exp, a=obj1, b=obj2, c=obj3)) == True

@pytest.mark.safe
def test_set_forAll_3():
    ocl_exp = "Set{a, b, c}->forAll(o|o.flag = 't1')"
    assert (eval_ocl(ocl_exp, a=obj1, b=obj2, c=obj3)) == False

@pytest.mark.safe
def test_set_includes_3():
    ocl_exp = "Set{a, b, c}->includes(d)"
    assert (eval_ocl(ocl_exp, a=obj1, b=obj2, c=obj3, d=obj1)) == True    

@pytest.mark.safe
def test_set_isEmpty_3():
    ocl_exp = "Set{a, b, c}->isEmpty()"
    assert (eval_ocl(ocl_exp, a=obj1, b=obj2, c=obj3)) == False        

@pytest.mark.safe
def test_set_notEmpty_3():
    ocl_exp = "Set{a, b, c}->notEmpty()"
    assert (eval_ocl(ocl_exp, a=obj1, b=obj2, c=obj3)) == True     

@pytest.mark.safe
def test_set_reject_3():
    ocl_exp = "Set{a, b, c}->reject(o|o.flag = 't1')"
    assert (eval_ocl(ocl_exp, a=obj1, b=obj2, c=obj3)) == {obj2}    

@pytest.mark.safe
def test_set_select_3():
    ocl_exp = "Set{a, b, c}->select(o|o.flag = 't1')"
    assert (eval_ocl(ocl_exp, a=obj1, b=obj2, c=obj3)) == {obj1}        

@pytest.mark.safe
def test_set_size_3():
    ocl_exp = "Set{a, b, c}->size()"
    assert (eval_ocl(ocl_exp, a=obj1, b=obj2, c=obj3)) == 2    
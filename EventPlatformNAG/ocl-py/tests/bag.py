from ocl.ocl import eval_ocl, OCLTerm
import pytest


## Basic types test

@pytest.mark.safe
def test_set_1():
    ocl_exp = "let x = Bag{0, 1, 2, 3, 4} in x"
    assert (eval_ocl(ocl_exp)) == [0, 1, 2, 3, 4]
    
@pytest.mark.safe
def test_bag_2():
    ocl_exp = "Bag{0, 1, 2, 3, 4, 4, 3, 2, 1, 0}"
    assert (eval_ocl(ocl_exp)) == [0, 1, 2, 3, 4, 4, 3, 2, 1, 0]
    
@pytest.mark.safe
def test_bag_collect():
    ocl_exp = "Bag{0, 1, 2, 3, 4}->collect(e|e>3)"
    assert (eval_ocl(ocl_exp)) == [False, False, False, False, True]
    
@pytest.mark.safe
def test_bag_collect_2():
    ocl_exp = "Bag{0, 1, 2, 3, 4}->collect(e|e+3)"
    assert (eval_ocl(ocl_exp)) == [3, 4, 5, 6, 7]
    
@pytest.mark.safe
def test_bag_excludes():
    ocl_exp = "Bag{0, 1, 2, 3, 4}->excludes(3)"
    assert (eval_ocl(ocl_exp)) == False   
    
@pytest.mark.safe
def test_bag_excludes_2():
    ocl_exp = "Bag{0, 1, 2, 3, 4}->excludes(5)"
    assert (eval_ocl(ocl_exp)) == True 
   
@pytest.mark.safe
def test_bag_exists():
    ocl_exp = "Bag{0, 1, 2, 3, 4}->exists(e|e>3)"
    assert (eval_ocl(ocl_exp)) == True 

@pytest.mark.safe    
def test_bag_exists_2():
    ocl_exp = "Bag{0, 1, 2, 3, 4}->exists(e|e>6)"
    assert (eval_ocl(ocl_exp)) == False
    
@pytest.mark.safe
def test_bag_forAll():
    ocl_exp = "Bag{0, 1, 2, 3, 4}->forAll(e|e>3)"
    assert (eval_ocl(ocl_exp)) == False 
    
@pytest.mark.safe
def test_bag_forAll_2():
    ocl_exp = "Bag{0, 1, 2, 3, 4}->forAll(e|e<6)"
    assert (eval_ocl(ocl_exp)) == True 
    
@pytest.mark.safe
def test_bag_includes():
    ocl_exp = "Bag{0, 1, 2, 3, 4}->includes(3)"
    assert (eval_ocl(ocl_exp)) == True   

@pytest.mark.safe
def test_bag_includes_2():
    ocl_exp = "Bag{0, 1, 2, 3, 4}->includes(7)"
    assert (eval_ocl(ocl_exp)) == False   
    
@pytest.mark.safe
def test_bag_isEmpty():
    ocl_exp = "Bag{0, 1, 2, 3, 4}->isEmpty()"
    assert (eval_ocl(ocl_exp)) == False   
    
@pytest.mark.safe
def test_bag_isEmpty_2():
    ocl_exp = "Bag{}->isEmpty()"
    assert (eval_ocl(ocl_exp)) == True  
    
@pytest.mark.safe
def test_bag_notEmpty():
    ocl_exp = "Bag{0, 1, 2, 3, 4}->notEmpty()"
    assert (eval_ocl(ocl_exp)) == True  
    
@pytest.mark.safe
def test_bag_notEmpty_2():
    ocl_exp = "Bag{}->notEmpty()"
    assert (eval_ocl(ocl_exp)) == False  
    
@pytest.mark.safe
def test_bag_select():
    ocl_exp = "Bag{0, 1, 2, 3, 4}->select(e|e>6)"
    assert (eval_ocl(ocl_exp)) == []
    
@pytest.mark.safe
def test_bag_select_2():
    ocl_exp = "Bag{0, 1, 2, 3, 4}->select(e|e>3)"
    assert (eval_ocl(ocl_exp)) == [4]
    
@pytest.mark.safe
def test_bag_reject():
    ocl_exp = "Bag{0, 1, 2, 3, 4}->reject(e|e>6)"
    assert (eval_ocl(ocl_exp)) == [0, 1, 2, 3, 4]
    
@pytest.mark.safe
def test_bag_reject_2():
    ocl_exp = "Bag{0, 1, 2, 3, 4}->reject(e|e>3)"
    assert (eval_ocl(ocl_exp)) == [0, 1, 2, 3]
    
@pytest.mark.safe
def test_bag_size():
    ocl_exp = "Bag{0, 1, 2, 3, 4}->size()"
    assert (eval_ocl(ocl_exp)) == 5
    
@pytest.mark.safe
def test_bag_size_2():
    ocl_exp = "Bag{}->size()"
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
def test_bag_3():
    ocl_exp = "Bag{a, b, c}"
    assert (eval_ocl(ocl_exp, a=obj1, b=obj2, c=obj3)) == [obj1, obj2, obj3]

@pytest.mark.safe
def test_bag_collect_3():
    ocl_exp = "Bag{a, b, c}->collect(o|o.flag)"
    assert (eval_ocl(ocl_exp, a=obj1, b=obj2, c=obj3)) == ['t1','t2','t1']    

@pytest.mark.safe
def test_bag_excludes_3():
    ocl_exp = "Bag{a, b, c}->excludes(d)"
    assert (eval_ocl(ocl_exp, a=obj1, b=obj2, c=obj3, d=obj1)) == False

@pytest.mark.safe
def test_bag_exists_3():
    ocl_exp = "Bag{a, b, c}->exists(o|o.flag = 't1')"
    assert (eval_ocl(ocl_exp, a=obj1, b=obj2, c=obj3)) == True

@pytest.mark.safe
def test_bag_forAll_3():
    ocl_exp = "Bag{a, b, c}->forAll(o|o.flag = 't1')"
    assert (eval_ocl(ocl_exp, a=obj1, b=obj2, c=obj3)) == False

@pytest.mark.safe
def test_bag_includes_3():
    ocl_exp = "Bag{a, b, c}->includes(d)"
    assert (eval_ocl(ocl_exp, a=obj1, b=obj2, c=obj3, d=obj1)) == True    

@pytest.mark.safe
def test_bag_isEmpty_3():
    ocl_exp = "Bag{a, b, c}->isEmpty()"
    assert (eval_ocl(ocl_exp, a=obj1, b=obj2, c=obj3)) == False        

@pytest.mark.safe
def test_bag_notEmpty_3():
    ocl_exp = "Bag{a, b, c}->notEmpty()"
    assert (eval_ocl(ocl_exp, a=obj1, b=obj2, c=obj3)) == True     

@pytest.mark.safe
def test_bag_reject_3():
    ocl_exp = "Bag{a, b, c}->reject(o|o.flag = 't1')"
    assert (eval_ocl(ocl_exp, a=obj1, b=obj2, c=obj3)) == [obj2]    

@pytest.mark.safe
def test_bag_select_3():
    ocl_exp = "Bag{a, b, c}->select(o|o.flag = 't1')"
    assert (eval_ocl(ocl_exp, a=obj1, b=obj2, c=obj3)) == [obj1, obj3]        

@pytest.mark.safe
def test_bag_size_3():
    ocl_exp = "Bag{a, b, c}->size()"
    assert (eval_ocl(ocl_exp, a=obj1, b=obj2, c=obj3)) == 3    
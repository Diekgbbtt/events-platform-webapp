from ocl.ocl import eval_ocl, OCLTerm
import pytest

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

# True iff self and o are the same object or if self and o are instances of the same
# Type and have the same value. Invalid iff self or o are invalid

@pytest.mark.safe
def test_eq_true():
    ocl_exp = "a = b"
    assert(eval_ocl(ocl_exp,a=obj1,b=obj1)) == True
    
@pytest.mark.safe
def test_eq_true_2():
    ocl_exp = "a = b"
    assert(eval_ocl(ocl_exp,a=obj1,b=obj3)) == True
    
@pytest.mark.safe
def test_eq_false():
    ocl_exp = "a = b"
    assert(eval_ocl(ocl_exp,a=obj1,b=obj2)) == False

def test_eq_invalid():
    ocl_exp = "a = invalid"
    assert(eval_ocl(ocl_exp,a=obj1)) == None
    
# True i Invalid i ff ffself and o are not the same object and do not have the same value. 
# self or o are invalid

@pytest.mark.safe
def test_neq_false():
    ocl_exp = "a <> b"
    assert(eval_ocl(ocl_exp,a=obj1,b=obj1)) == False
    
@pytest.mark.safe
def test_eq_false_2():
    ocl_exp = "a <> b"
    assert(eval_ocl(ocl_exp,a=obj1,b=obj3)) == False
    
@pytest.mark.safe
def test_neq_true():
    ocl_exp = "a <> b"
    assert(eval_ocl(ocl_exp,a=obj1,b=obj2)) == True

def test_neq_invalid():
    ocl_exp = "a = invalid"
    assert(eval_ocl(ocl_exp,a=obj1)) == None
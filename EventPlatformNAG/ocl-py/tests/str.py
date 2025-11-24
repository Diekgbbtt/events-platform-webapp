from ocl.ocl import eval_ocl
import pytest

# Definition A.15 (Syntax Of Operations)

@pytest.mark.safe
def test_eq_true():
    ocl_exp = "'a string' = 'a string'"
    assert(eval_ocl(ocl_exp)) == True

@pytest.mark.safe
def test_eq_false():
    ocl_exp = "'a string' = 'another string'"
    assert(eval_ocl(ocl_exp)) == False
    
@pytest.mark.safe
def test_neq_false():
    ocl_exp = "'a string' <> 'a string'"
    assert(eval_ocl(ocl_exp)) == False

@pytest.mark.safe
def test_neq_true():
    ocl_exp = "'a string' = 'another string'"
    assert(eval_ocl(ocl_exp)) == True
    
@pytest.mark.safe
def test_concat():
    ocl_exp = "'a string'.concat('another string')"
    assert(eval_ocl(ocl_exp)) == 'a stringanother string'
    
@pytest.mark.safe
def test_neq_true():
    ocl_exp = "'a string'.size()"
    assert(eval_ocl(ocl_exp)) == 8
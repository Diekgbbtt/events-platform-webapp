from ocl.ocl import eval_ocl
import pytest

# Definition A.15 (Syntax Of Operations)

@pytest.mark.safe
def test_lt_false():
    ocl_exp = "1 < 1"
    assert(eval_ocl(ocl_exp)) == False

@pytest.mark.safe
def test_lt_false():
    ocl_exp = "1 < 2"
    assert(eval_ocl(ocl_exp)) == True
    
@pytest.mark.safe
def test_geq_true():
    ocl_exp = "1 >= 1"
    assert(eval_ocl(ocl_exp)) == True

@pytest.mark.safe
def test_geq_false():
    ocl_exp = "83 >= 100"
    assert(eval_ocl(ocl_exp)) == False
    
@pytest.mark.safe
def test_gt_false():
    ocl_exp = "1 > 1"
    assert(eval_ocl(ocl_exp)) == False

@pytest.mark.safe
def test_gt_false():
    ocl_exp = "1 > 0"
    assert(eval_ocl(ocl_exp)) == True

@pytest.mark.safe
def test_leq_true():
    ocl_exp = "1 <= 1"
    assert(eval_ocl(ocl_exp)) == True

@pytest.mark.safe
def test_leq_false():
    ocl_exp = "1 <= 0"
    assert(eval_ocl(ocl_exp)) == False
    
@pytest.mark.safe
def test_geq_true():
    ocl_exp = "1 >= 1"
    assert(eval_ocl(ocl_exp)) == True

@pytest.mark.safe
def test_geq_false():
    ocl_exp = "83 >= 100"
    assert(eval_ocl(ocl_exp)) == False
    
@pytest.mark.safe
def test_eq_true():
    ocl_exp = "1 = 1"
    assert(eval_ocl(ocl_exp)) == True

@pytest.mark.safe
def test_eq_false():
    ocl_exp = "1 = 2"
    assert(eval_ocl(ocl_exp)) == False
   
def test_eq_false_null():
    ocl_exp = "1 = null"
    assert(eval_ocl(ocl_exp)) == False
    
def test_eq_false_null_2():
    ocl_exp = "null = 1"
    assert(eval_ocl(ocl_exp)) == False
    
def test_eq_none():
    ocl_exp = "1 = invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_eq_none():
    ocl_exp = "invalid = 1"
    assert(eval_ocl(ocl_exp)) == None
    
@pytest.mark.safe
def test_neq_false():
    ocl_exp = "1 <> 1"
    assert(eval_ocl(ocl_exp)) == False

@pytest.mark.safe
def test_neq_true():
    ocl_exp = "1 <> 2"
    assert(eval_ocl(ocl_exp)) == True
   
def test_neq_false_null():
    ocl_exp = "1 <> null"
    assert(eval_ocl(ocl_exp)) == True
    
def test_neq_false_null_2():
    ocl_exp = "null <> 1"
    assert(eval_ocl(ocl_exp)) == True
    
def test_neq_none():
    ocl_exp = "1 <> invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_neq_none():
    ocl_exp = "invalid <> 1"
    assert(eval_ocl(ocl_exp)) == None
  
@pytest.mark.safe
def test_plus_true():
    ocl_exp = "1 + 101"
    assert(eval_ocl(ocl_exp)) == 102

@pytest.mark.safe
def test_minus_false():
    ocl_exp = "1 - 101"
    assert(eval_ocl(ocl_exp)) == -100
    
@pytest.mark.safe
def test_mult_false():
    ocl_exp = "2 * 101"
    assert(eval_ocl(ocl_exp)) == 202
    
@pytest.mark.safe
def test_div_false():
    ocl_exp = "2 / 5"
    assert(eval_ocl(ocl_exp)) == 0.4
  

from ocl.ocl import eval_ocl
import pytest

# Definition A.15 (Syntax Of Operations)

@pytest.mark.safe
def test_lt_false():
    ocl_exp = "1.3 < 0.5"
    assert(eval_ocl(ocl_exp)) == False

@pytest.mark.safe
def test_lt_false():
    ocl_exp = "1.3 < 2"
    assert(eval_ocl(ocl_exp)) == True
    
@pytest.mark.safe
def test_geq_true():
    ocl_exp = "1.3 >= 1"
    assert(eval_ocl(ocl_exp)) == True

@pytest.mark.safe
def test_geq_false():
    ocl_exp = "83.5 >= 100.3"
    assert(eval_ocl(ocl_exp)) == False
    
@pytest.mark.safe
def test_gt_false():
    ocl_exp = "1.1 > 1.3"
    assert(eval_ocl(ocl_exp)) == False

@pytest.mark.safe
def test_gt_false():
    ocl_exp = "1.5 > 0"
    assert(eval_ocl(ocl_exp)) == True

@pytest.mark.safe
def test_leq_true():
    ocl_exp = "1.0 <= 1.0"
    assert(eval_ocl(ocl_exp)) == True

@pytest.mark.safe
def test_leq_false():
    ocl_exp = "1.3 <= 0"
    assert(eval_ocl(ocl_exp)) == False
    
@pytest.mark.safe
def test_geq_true():
    ocl_exp = "1.5 >= 1"
    assert(eval_ocl(ocl_exp)) == True

@pytest.mark.safe
def test_geq_false():
    ocl_exp = "83.1 >= 100.2"
    assert(eval_ocl(ocl_exp)) == False
    
@pytest.mark.safe
def test_eq_true():
    ocl_exp = "1.3 = 1.3"
    assert(eval_ocl(ocl_exp)) == True

@pytest.mark.safe
def test_eq_false():
    ocl_exp = "1.3 = 2.3"
    assert(eval_ocl(ocl_exp)) == False
   
def test_eq_false_null():
    ocl_exp = "1.2 = null"
    assert(eval_ocl(ocl_exp)) == False
    
def test_eq_false_null_2():
    ocl_exp = "null = 1.3"
    assert(eval_ocl(ocl_exp)) == False
    
def test_eq_none():
    ocl_exp = "1.3 = invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_eq_none():
    ocl_exp = "invalid = 1.2"
    assert(eval_ocl(ocl_exp)) == None
    
@pytest.mark.safe
def test_neq_false():
    ocl_exp = "1.2 <> 1.2"
    assert(eval_ocl(ocl_exp)) == False

@pytest.mark.safe
def test_neq_true():
    ocl_exp = "1.2 <> 2"
    assert(eval_ocl(ocl_exp)) == True
   
def test_neq_false_null():
    ocl_exp = "1.2 <> null"
    assert(eval_ocl(ocl_exp)) == True
    
def test_neq_false_null_2():
    ocl_exp = "null <> 1.2"
    assert(eval_ocl(ocl_exp)) == True
    
def test_neq_none():
    ocl_exp = "1.2 <> invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_neq_none():
    ocl_exp = "invalid <> 1.2"
    assert(eval_ocl(ocl_exp)) == None
  
@pytest.mark.safe
def test_plus_true():
    ocl_exp = "1.2 + 101.2"
    assert(eval_ocl(ocl_exp)) == 102.4

@pytest.mark.safe
def test_minus_false():
    ocl_exp = "1.3 - 101.2"
    assert(eval_ocl(ocl_exp)) == -99.9
    
@pytest.mark.safe
def test_mult_false():
    ocl_exp = "2 * 101.2"
    assert(eval_ocl(ocl_exp)) == 202.4
    
@pytest.mark.safe
def test_div_false():
    ocl_exp = "2.5 / 5"
    assert(eval_ocl(ocl_exp)) == 0.5
  

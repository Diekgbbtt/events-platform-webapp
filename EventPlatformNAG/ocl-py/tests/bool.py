from ocl.ocl import eval_ocl
import pytest

# 11.5.4 Boolean
# or (b : Boolean) : Boolean
# True if either self or b is true.
# Otherwise invalid if either self or b is invalid.
# Otherwise null if either self or b is null.
# Otherwise false.


@pytest.mark.safe
def test_true_or_true():
    ocl_exp = "true or true"
    assert(eval_ocl(ocl_exp)) == True

@pytest.mark.safe
def test_true_or_false():
    ocl_exp = "true or false"
    assert(eval_ocl(ocl_exp)) == True
    
@pytest.mark.safe
def test_false_or_true():
    ocl_exp = "false or true"
    assert(eval_ocl(ocl_exp)) == True
    
@pytest.mark.safe
def test_false_or_false():
    ocl_exp = "false or false"
    assert(eval_ocl(ocl_exp)) == False

def test_null_or_true():
    ocl_exp = "null or true"
    assert(eval_ocl(ocl_exp)) == True
    
def test_true_or_null():
    ocl_exp = "true or null"
    assert(eval_ocl(ocl_exp)) == True
    
def test_null_or_null():
    ocl_exp = "null or null"
    assert(eval_ocl(ocl_exp)) == None
    
def test_null_or_false():
    ocl_exp = "null or false"
    assert(eval_ocl(ocl_exp)) == None
    
def test_false_or_null():
    ocl_exp = "false or null"
    assert(eval_ocl(ocl_exp)) == None
    
def test_invalid_or_true():
    ocl_exp = "invalid or true"
    assert(eval_ocl(ocl_exp)) == True
    
def test_true_or_invalid():
    ocl_exp = "true or invalid"
    assert(eval_ocl(ocl_exp)) == True
    
def test_invalid_or_invalid():
    ocl_exp = "invalid or invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_invalid_or_false():
    ocl_exp = "invalid or false"
    assert(eval_ocl(ocl_exp)) == None
    
def test_false_or_invalid():
    ocl_exp = "false or invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_null_or_invalid():
    ocl_exp = "null or invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_invalid_or_null():
    ocl_exp = "invalid or null"
    assert(eval_ocl(ocl_exp)) == None
    
# 11.5.4 Boolean
# not : Boolean
# True if self is false.
# False if self is true.
# null if self is null.
# Otherwise invalid. 

@pytest.mark.safe
def test_not_true():
    ocl_exp = "not true"
    assert(eval_ocl(ocl_exp)) == False

@pytest.mark.safe
def test_not_false():
    ocl_exp = "not false"
    assert(eval_ocl(ocl_exp)) == True

def test_not_null():
    ocl_exp = "not null"
    assert(eval_ocl(ocl_exp)) == None

def test_not_invalid():
    ocl_exp = "not invalid"
    assert(eval_ocl(ocl_exp)) == None 
    
# A.2.2 Common Operations On All Types

@pytest.mark.safe
def test_true_neq_true():
    ocl_exp = "true <> true"
    assert(eval_ocl(ocl_exp)) == False

@pytest.mark.safe
def test_true_neq_false():
    ocl_exp = "true <> false"
    assert(eval_ocl(ocl_exp)) == True
    
@pytest.mark.safe
def test_false_neq_true():
    ocl_exp = "false <> true"
    assert(eval_ocl(ocl_exp)) == True
    
@pytest.mark.safe
def test_false_neq_false():
    ocl_exp = "false <> false"
    assert(eval_ocl(ocl_exp)) == False

def test_null_neq_true():
    ocl_exp = "null <> true"
    assert(eval_ocl(ocl_exp)) == True
    
def test_true_neq_null():
    ocl_exp = "true <> null"
    assert(eval_ocl(ocl_exp)) == True
    
def test_null_neq_null():
    ocl_exp = "null <> null"
    assert(eval_ocl(ocl_exp)) == False
    
def test_null_neq_false():
    ocl_exp = "null <> false"
    assert(eval_ocl(ocl_exp)) == True
    
def test_false_neq_null():
    ocl_exp = "false <> null"
    assert(eval_ocl(ocl_exp)) == True
    
def test_invalid_neq_true():
    ocl_exp = "invalid <> true"
    assert(eval_ocl(ocl_exp)) == None
    
def test_true_neq_invalid():
    ocl_exp = "true <> invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_invalid_neq_invalid():
    ocl_exp = "invalid <> invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_invalid_neq_false():
    ocl_exp = "invalid <> false"
    assert(eval_ocl(ocl_exp)) == None
    
def test_false_neq_invalid():
    ocl_exp = "false <> invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_null_neq_invalid():
    ocl_exp = "null <> invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_invalid_neq_null():
    ocl_exp = "invalid <> null"
    assert(eval_ocl(ocl_exp)) == None
    
# 11.5.4 Boolean
# implies (b : Boolean) : Boolean
# True if self is false, or if b is true.
# Otherwise invalid if either self or b is invalid.
# Otherwise null if either self or b is null.
# Otherwise false.

@pytest.mark.safe
def test_true_implies_true():
    ocl_exp = "true implies true"
    assert(eval_ocl(ocl_exp)) == True

@pytest.mark.safe
def test_true_implies_false():
    ocl_exp = "true implies false"
    assert(eval_ocl(ocl_exp)) == False
    
@pytest.mark.safe
def test_false_implies_true():
    ocl_exp = "false implies true"
    assert(eval_ocl(ocl_exp)) == True
    
@pytest.mark.safe
def test_false_implies_false():
    ocl_exp = "false implies false"
    assert(eval_ocl(ocl_exp)) == True

def test_null_implies_true():
    ocl_exp = "null implies true"
    assert(eval_ocl(ocl_exp)) == True
    
def test_true_implies_null():
    ocl_exp = "true implies null"
    assert(eval_ocl(ocl_exp)) == None
    
def test_null_implies_null():
    ocl_exp = "null implies null"
    assert(eval_ocl(ocl_exp)) == None
    
def test_null_implies_false():
    ocl_exp = "null implies false"
    assert(eval_ocl(ocl_exp)) == None
    
def test_false_implies_null():
    ocl_exp = "false implies null"
    assert(eval_ocl(ocl_exp)) == True
    
def test_invalid_implies_true():
    ocl_exp = "invalid implies true"
    assert(eval_ocl(ocl_exp)) == True
    
def test_true_implies_invalid():
    ocl_exp = "true implies invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_invalid_implies_invalid():
    ocl_exp = "invalid implies invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_invalid_implies_false():
    ocl_exp = "invalid implies false"
    assert(eval_ocl(ocl_exp)) == None
    
def test_false_implies_invalid():
    ocl_exp = "false implies invalid"
    assert(eval_ocl(ocl_exp)) == True
    
def test_null_implies_invalid():
    ocl_exp = "null implies invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_invalid_implies_null():
    ocl_exp = "invalid implies null"
    assert(eval_ocl(ocl_exp)) == None
    

# A.2.2 Common Operations On All Types

@pytest.mark.safe
def test_true_eq_true():
    ocl_exp = "true = true"
    assert(eval_ocl(ocl_exp)) == True

@pytest.mark.safe
def test_true_eq_false():
    ocl_exp = "true = false"
    assert(eval_ocl(ocl_exp)) == False
    
@pytest.mark.safe
def test_false_eq_true():
    ocl_exp = "false = true"
    assert(eval_ocl(ocl_exp)) == False
    
@pytest.mark.safe
def test_false_eq_false():
    ocl_exp = "false = false"
    assert(eval_ocl(ocl_exp)) == True

def test_null_eq_true():
    ocl_exp = "null = true"
    assert(eval_ocl(ocl_exp)) == False
    
def test_true_eq_null():
    ocl_exp = "true = null"
    assert(eval_ocl(ocl_exp)) == False
    
def test_null_eq_null():
    ocl_exp = "null = null"
    assert(eval_ocl(ocl_exp)) == True
    
def test_null_eq_false():
    ocl_exp = "null = false"
    assert(eval_ocl(ocl_exp)) == False
    
def test_false_eq_null():
    ocl_exp = "false = null"
    assert(eval_ocl(ocl_exp)) == False
    
def test_invalid_eq_true():
    ocl_exp = "invalid = true"
    assert(eval_ocl(ocl_exp)) == None
    
def test_true_eq_invalid():
    ocl_exp = "true = invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_invalid_eq_invalid():
    ocl_exp = "invalid = invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_invalid_eq_false():
    ocl_exp = "invalid = false"
    assert(eval_ocl(ocl_exp)) == None
    
def test_false_eq_invalid():
    ocl_exp = "false = invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_null_eq_invalid():
    ocl_exp = "null = invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_invalid_eq_null():
    ocl_exp = "invalid = null"
    assert(eval_ocl(ocl_exp)) == None
    
# 11.5.4 Boolean
# and (b : Boolean) : Boolean
# False if either self or b is false.
# Otherwise invalid if either self or b is invalid .
# Otherwise null if either self or b is null.
# Otherwise true

@pytest.mark.safe
def test_true_and_true():
    ocl_exp = "true and true"
    assert(eval_ocl(ocl_exp)) == True

@pytest.mark.safe
def test_true_and_false():
    ocl_exp = "true and false"
    assert(eval_ocl(ocl_exp)) == False
    
@pytest.mark.safe
def test_false_and_true():
    ocl_exp = "false and true"
    assert(eval_ocl(ocl_exp)) == False
    
@pytest.mark.safe
def test_false_and_false():
    ocl_exp = "false and false"
    assert(eval_ocl(ocl_exp)) == False

def test_null_and_true():
    ocl_exp = "null and true"
    assert(eval_ocl(ocl_exp)) == None
    
def test_true_and_null():
    ocl_exp = "true and null"
    assert(eval_ocl(ocl_exp)) == None
    
def test_null_and_null():
    ocl_exp = "null and null"
    assert(eval_ocl(ocl_exp)) == None
    
def test_null_and_false():
    ocl_exp = "null and false"
    assert(eval_ocl(ocl_exp)) == False
    
def test_false_and_null():
    ocl_exp = "false and null"
    assert(eval_ocl(ocl_exp)) == False
    
def test_invalid_and_true():
    ocl_exp = "invalid and true"
    assert(eval_ocl(ocl_exp)) == None
    
def test_true_and_invalid():
    ocl_exp = "true and invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_invalid_and_invalid():
    ocl_exp = "invalid and invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_invalid_and_false():
    ocl_exp = "invalid and false"
    assert(eval_ocl(ocl_exp)) == False
    
def test_false_and_invalid():
    ocl_exp = "false and invalid"
    assert(eval_ocl(ocl_exp)) == False
    
def test_null_and_invalid():
    ocl_exp = "null and invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_invalid_and_null():
    ocl_exp = "invalid and null"
    assert(eval_ocl(ocl_exp)) == None
    
# 11.5.4 Boolean
# xor (b : Boolean) : Boolean
# True if self is true and b is false, or if self is false and b is true.
# False if self is true and b is true, or if self is false and b is false.
# Otherwise invalid if either self or b is invalid.
# Otherwise null.

@pytest.mark.safe
def test_true_xor_true():
    ocl_exp = "true xor true"
    assert(eval_ocl(ocl_exp)) == False

@pytest.mark.safe
def test_true_xor_false():
    ocl_exp = "true xor false"
    assert(eval_ocl(ocl_exp)) == True
    
@pytest.mark.safe
def test_false_xor_true():
    ocl_exp = "false xor true"
    assert(eval_ocl(ocl_exp)) == True
    
@pytest.mark.safe
def test_false_xor_false():
    ocl_exp = "false xor false"
    assert(eval_ocl(ocl_exp)) == False

def test_null_xor_true():
    ocl_exp = "null xor true"
    assert(eval_ocl(ocl_exp)) == None
    
def test_true_xor_null():
    ocl_exp = "true xor null"
    assert(eval_ocl(ocl_exp)) == None
    
def test_null_xor_null():
    ocl_exp = "null xor null"
    assert(eval_ocl(ocl_exp)) == None
    
def test_null_xor_false():
    ocl_exp = "null xor false"
    assert(eval_ocl(ocl_exp)) == None
    
def test_false_xor_null():
    ocl_exp = "false xor null"
    assert(eval_ocl(ocl_exp)) == None
    
def test_invalid_xor_true():
    ocl_exp = "invalid xor true"
    assert(eval_ocl(ocl_exp)) == None
    
def test_true_xor_invalid():
    ocl_exp = "true xor invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_invalid_xor_invalid():
    ocl_exp = "invalid xor invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_invalid_xor_false():
    ocl_exp = "invalid xor false"
    assert(eval_ocl(ocl_exp)) == None
    
def test_false_xor_invalid():
    ocl_exp = "false xor invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_null_xor_invalid():
    ocl_exp = "null xor invalid"
    assert(eval_ocl(ocl_exp)) == None
    
def test_invalid_xor_null():
    ocl_exp = "invalid xor null"
    assert(eval_ocl(ocl_exp)) == None
 
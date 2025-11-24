from ocl.ocl import eval_ocl, OCLTerm
import pytest


# 9007199254740993 is the smallest integer that can't be represented accurately
# in a IEE754 double (it's rounded down to 9007199254740992)
def test14():
    ocl_exp = "let x = 9007199254740993.0 in (x = 9007199254740993)"
    assert (eval_ocl(ocl_exp))

def test15():
    ocl_exp = "let x = 9007199254740993.0 in (x <> 9007199254740992)"
    assert (eval_ocl(ocl_exp))

# @pytest.mark.safe
# def test16():
#     ocl_exp = "OrderedSet{ 1, 2 } <> OrderedSet{ 2, 1 }"
#     assert eval_ocl(ocl_exp)

@pytest.mark.safe
def test17():
    ocl_exp = "OrderedSet{ 1, 2 }.append(3) = OrderedSet{ 1, 2, 3 }"
    assert eval_ocl(ocl_exp)

@pytest.mark.safe
def test18():
    ocl_exp = "OrderedSet{ 1, 2 }.at(0) = 1"
    assert eval_ocl(ocl_exp)

@pytest.mark.safe
def test19():
    ocl_exp = "OrderedSet{ 1, 2 }.at(1) = 2"
    assert eval_ocl(ocl_exp)

@pytest.mark.safe
def test20():
    ocl_exp = "OrderedSet{ 2, 1 }.first() = 2"
    assert eval_ocl(ocl_exp)

@pytest.mark.safe
def test21():
    ocl_exp = "OrderedSet{ 2, 1 }.first() = 2"
    assert eval_ocl(ocl_exp)

@pytest.mark.safe
def test22():
    ocl_exp = "OrderedSet{ 2, 1 }.last() = 1"
    assert eval_ocl(ocl_exp)

@pytest.mark.safe
def test23():
    ocl_exp = "OrderedSet{ 1, 2, 4, 3 }.indexOf(3) = 3"
    assert eval_ocl(ocl_exp)

@pytest.mark.safe
def test24():
    ocl_exp = "OrderedSet{ 1, 2 }.insertAt(0, 7)"
    assert eval_ocl(ocl_exp) == {7: None, 1: None, 2: None}

@pytest.mark.safe
def test26():
    ocl_exp = "OrderedSet{ 1, 2 }.insertAt(1, 7) = OrderedSet{ 1, 7, 2 }"
    assert eval_ocl(ocl_exp)

@pytest.mark.safe
def test27():
    ocl_exp = "OrderedSet{ 1, 2 }.insertAt(99, 7) = OrderedSet{ 1, 2, 7 }"
    assert eval_ocl(ocl_exp)

@pytest.mark.safe
def test28():
    ocl_exp = "OrderedSet{ 1, 2 }.prepend(3) = OrderedSet{ 3, 1, 2 }"
    assert eval_ocl(ocl_exp)

# This test fails because insert is an existing method that returns None.
# Ideally it should instead be an error message or exception pointing out that
# insert isn't valid OCL.
# Could possibly handle this by translating all method calls to add a prefix,
# so there's no confusion with existing Python methods.
@pytest.mark.safe
def test29():
    ocl_exp = "Sequence{ 1, 2 }.insertAt(0, 7)"
    assert eval_ocl(ocl_exp) == [ 7, 1, 2 ]

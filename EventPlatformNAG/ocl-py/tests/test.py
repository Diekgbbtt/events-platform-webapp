from ocl.ocl import eval_ocl, OCLTerm
import pytest

@pytest.mark.safe
def test1():
    ocl_exp = "let x = Set{0, 1..5} in x->select(e | e > 0)->collect(e | e + 4)"
    result = eval_ocl(ocl_exp)
    assert (result) == [5, 6, 7, 8, 9]

@pytest.mark.safe
def test2():
    ocl_exp = "Sequence{0, 1..5}->select(e | e > 0)->collect(e | e + 4)"
    assert (eval_ocl(ocl_exp)) == [5, 6, 7, 8, 9]

@pytest.mark.safe
def test3():
    ocl_exp = "Set{}->isEmpty()"
    assert (eval_ocl(ocl_exp)) == True

@pytest.mark.safe
def test4():
    ocl_exp = "x->size() < (y+4) * 3"
    assert (eval_ocl(ocl_exp,x=[3,4,5],y=5)) == True

class Paper(OCLTerm):
    def __init__(self, t) -> None:
        self.title = t
    

class B(OCLTerm):
    def c(self,a):
        return a==45
    papers = [Paper("P1"),Paper("P2"),Paper("P3")]


class A(OCLTerm):
    b = B()
    flag = True
    student = False
    

a = A()
b = B()

@pytest.mark.safe
def test5():
    ocl_exp = "a.b.c(45)"
    assert (eval_ocl(ocl_exp,a=a)) == True


@pytest.mark.safe
def test6():
    ocl_exp = "let x = Tuple{foo='abc'} in (x.foo = 'abc' and y.flag)"
    assert (eval_ocl(ocl_exp,y=a)) == True

# TODO: Qualified names
# ocl_exp = "ParameterDirectionKind::inout"
# ocl_exp = compile(ocl_exp)
# print("OCL:    " + ocl_exp)
# print("Python: " + ocl_exp)
# assert (eval_ocl(ocl_exp))

@pytest.mark.safe
def test7():
    ocl_exp = "self.student"
    assert (eval_ocl(ocl_exp,self=a)) == False

@pytest.mark.safe
def test8():
    ocl_exp = "Sequence{1, 2..5}->forAll(e | e > 0)"
    assert (eval_ocl(ocl_exp)) == True

@pytest.mark.safe
def test9():
    ocl_exp = "self.papers->forAll(b | a.concat(b.title).size() < c)"
    assert (eval_ocl(ocl_exp,self=b,a="blabla",c=10)) == True


class Researcher(OCLTerm):
    def __init__(self, n):
        self.name = n
        self.advisers = []
        self.papers = []
    
    def __repr__(self) -> str:
        return self.name

class Paper(OCLTerm):
    def __init__(self, t, y, p):
        self.title = t
        self.year = y
        self.published = p
        self.authors = []
    
    def __repr__(self) -> str:
        return self.title


p1 = Paper("P1", 2020, True)
p2 = Paper("P2", 2021, True)
p3 = Paper("P3", 2022, True)
p4 = Paper("P4", 2020, False)
p5 = Paper("P5", 2021, False)
p6 = Paper("P6", 2022, False)

r1 = Researcher("R1")
r2 = Researcher("R2")
r3 = Researcher("R3")
r4 = Researcher("R4")

r2.advisers.append(r1)
r3.advisers.append(r2)

r1.papers = [p1,p2]
p1.authors.append(r1)
p2.authors.append(r1)

r4.papers = [p2,p3,p4,p5]
p2.authors.append(r4)
p3.authors.append(r4)
p4.authors.append(r4)
p5.authors.append(r4)

r3.papers = [p3,p5]
p3.authors.append(r3)
p5.authors.append(r3)


@pytest.mark.safe
def test10():
    ocl_exp = "self.published or self.authors->forAll(a | caller.advisers->excludes(a) and a.papers->forAll(p | (p <> self and 2023 - p.year < 2) implies p.authors->excludes(caller)))"
    assert (eval_ocl(ocl_exp,self=p1,caller=r1)) == True

@pytest.mark.safe
def test11():
    ocl_exp = "self.published or self.authors->forAll(a | caller.advisers->excludes(a) and a.papers->forAll(p | (p <> self and 2023 - p.year < 2) implies p.authors->excludes(caller)))"
    assert (eval_ocl(ocl_exp,self=p6,caller=r1)) == True


@pytest.mark.safe
def test11():
    ocl_exp = "self.published or self.authors->forAll(a | caller.advisers->excludes(a) and a.papers->forAll(p | (p <> self and 2023 - p.year < 2) implies p.authors->excludes(caller)))"
    assert (eval_ocl(ocl_exp,self=p4,caller=r1)) == True

@pytest.mark.safe
def test12():
    ocl_exp = "self.authors->forAll(a | caller.advisers->excludes(a) and a.papers->forAll(p | (p <> self and 2023 - p.year < 2) implies p.authors->excludes(caller)))"
    assert (eval_ocl(ocl_exp,self=p5,caller=r1)) == True

@pytest.mark.safe
def test13():
    ocl_exp = "self.authors->forAll(a | caller.advisers->excludes(a) and a.papers->forAll(p | (p <> self and 2023 - p.year <= 2) implies p.authors->excludes(caller)))"
    assert (eval_ocl(ocl_exp,self=p5,caller=r1)) == False

@pytest.mark.safe
def test14():
    ocl_exp = "b.papers->forAll(p | p.title <> '')"
    assert (eval_ocl(ocl_exp,b=b)) == True

@pytest.mark.safe
def test15():
    ocl_exp = "b.papers->asSet().title->forAll(p | p <> '')"
    assert (eval_ocl(ocl_exp,b=b)) == True

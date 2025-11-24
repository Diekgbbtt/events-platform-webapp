from ocl.ocl import eval_ocl, OCLTerm, eval_python
from ocl.compiler import compile
import pytest

class User(OCLTerm):
    def __init__(self, name, surname, username, password, role):
        self.name = name
        self.surname = surname
        self.username = username
        self.password = password
        self.role = role
        self.affiliated = None
        self.teaches = []
        self.attends = []
        self.applied = []
    
    def __repr__(self) -> str:
        return f"User: {self.name} {self.surname} ({self.username})"

class Department(OCLTerm):
    def __init__(self, name):
        self.name = name
        self.has = []
        self.offers = []
    
    def __repr__(self) -> str:
        return f"Department: {self.name}"

class Course(OCLTerm):
    def __init__(self, name, limit):
        self.name = name
        self.limit = limit
        self.belongsTo = None
        self.staffs = []
        self.applicants = []
        self.attendants = []

    def __repr__(self) -> str:
        return f"Course: {self.name} (Limit: {self.limit})"

class Enrolment(OCLTerm):
    def __init__(self, grade, final=False):
        self.grade = grade
        self.final = final
        self.student = None
        self.course = None
    
    def __repr__(self) -> str:
        return f"Enrolment: {self.student.username} in {self.course.name} (Grade: {self.grade}, Final: {self.final})"

# Create test data
r1 = User("Alice", "Smith", "alice.smith", "password123", "Admin")
r2 = User("Bob", "Johnson", "bob.johnson", "password456", "Professor")
r3 = User("Charlie", "Brown", "charlie.brown", "password789", "TA")
r4 = User("David", "Williams", "david.williams", "password101", "Student")
r5 = User("Eve", "Davis", "eve.davis", "password102", "Student")
r6 = User("Frank", "Garcia", "frank.garcia", "password103", "Student")
r7 = User("Grace", "Martinez", "grace.martinez", "password104", "Professor")
d1 = Department("Computer Science")
d2 = Department("Mathematics")
c1 = Course("Data Structures", 30)
c2 = Course("Algorithms", 25)
c3 = Course("Calculus", 40)
# Associate users with departments and courses
r1.affiliated = d1
d1.has.append(r1)
r2.affiliated = d1
d1.has.append(r2)
r3.affiliated = d1
d1.has.append(r3)
r4.affiliated = d2
d2.has.append(r4)
r5.affiliated = d2
d2.has.append(r5)
r6.affiliated = d1
d1.has.append(r6)
r7.affiliated = d2
d2.has.append(r7)
c1.belongsTo = d1
d1.offers.append(c1)
c2.belongsTo = d1
d1.offers.append(c2)
c3.belongsTo = d2
d2.offers.append(c3)
# Associate course with departments
c1.belongsTo = d1
d1.offers.append(c1)
c2.belongsTo = d1
d1.offers.append(c2)
c3.belongsTo = d2
d2.offers.append(c3)
# Associate courses with staff 
r2.teaches.append(c1)
c1.staffs.append(r2)
r2.teaches.append(c2)
c2.staffs.append(r2)
r3.teaches.append(c1)
c1.staffs.append(r3)
r3.teaches.append(c2)
c2.staffs.append(r3)
r7.teaches.append(c3)
c3.staffs.append(r7)
# Associate enrolments with students and courses
e1 = Enrolment(grade=85, final=True)
e1.student = r4
r4.attends.append(e1)
e1.course = c1
c1.attendants.append(e1)
e2 = Enrolment(grade=None, final=False)
e2.student = r5
r5.attends.append(e2)
e2.course = c3
c3.attendants.append(e2)
e3 = Enrolment(grade=90, final=True)
e3.student = r6
r6.attends.append(e3)
e3.course = c1
c1.attendants.append(e3)
e4 = Enrolment(grade=75, final=False)
e4.student = r6
r6.attends.append(e4)
e4.course = c2
c2.attendants.append(e4)
# Associate TAs with courses
r3.applied.append(c1)
c1.applicants.append(r3)
r3.applied.append(c2)
c2.applicants.append(r3)


# Invariant: A name, surname of a user cannot be empty
@pytest.mark.safe
def test_inv0():
    ocl_exp = "test_uniorg::User.allInstances()->forAll(u | not (u.name = null or u.surname = null))"
    assert eval_ocl(ocl_exp) == True

# Invariant: The username and password attributes of the User class cannot be empty.
@pytest.mark.safe
def test_inv1():
    ocl_exp = "test_uniorg::User.allInstances()->forAll(u | not (u.username = null or u.password = null))"
    assert eval_ocl(ocl_exp) == True

# Invariant: Every user has a unique username.
@pytest.mark.safe
def test_inv2():
    ocl_exp = "test_uniorg::User.allInstances()->forAll(u1 | test_uniorg::User.allInstances()->forAll(u2 | u1 <> u2 implies u1.username <> u2.username))"
    # ocl_exp = "test_uniorg::User.allInstances()->forAll(u1 | test_uniorg::User.allInstances()->forAll(u2 | u1 <> u2 implies (u1.username <> u2.username)))"
    assert eval_ocl(ocl_exp) == True

# Invariant: For every course, the number of enrolled students cannot be larger than the
# value of the limit attribute of the course
@pytest.mark.safe
def test_inv3():
    ocl_exp = "test_uniorg::Course.allInstances()->forAll(c | c.attendants->size() <= c.limit)"
    assert eval_ocl(ocl_exp) == True

# Invariant: Students cannot enroll in the same course multiple times
@pytest.mark.safe
def test_inv4():
    # Same problem with inv2
    ocl_exp = "test_uniorg::User.allInstances()->select(u | u.role = 'Student')->forAll(s | s.attends->forAll(e1 | s.attends->forAll(e2 | e1 <> e2 implies (e1.course <> e2.course))))"
    assert eval_ocl(ocl_exp) == True

# Invariant: Each course is taught by exactly one professor
@pytest.mark.safe
def test_inv5():
    ocl_exp = "test_uniorg::Course.allInstances()->forAll(c | c.staffs->select(s | s.role = 'Professor')->size() = 1)"
    assert eval_ocl(ocl_exp) == True

# A course can be taught by at most a number of TAs equal to the student limit
# divided by 20 (rounded down).
@pytest.mark.safe
def test_inv6():
    ocl_exp = "test_uniorg::Course.allInstances()->forAll(c | c.staffs->select(s | s.role = 'TA')->size() <= c.limit / 20)"
    assert eval_ocl(ocl_exp) == True

# Constraint: A user can read its own username
@pytest.mark.safe
def test_con0():
    ocl_exp = "self = caller"
    assert eval_ocl(ocl_exp, self=r4, caller=r4) == True

# Constraint: A user can only update his own name and surname to a non empty value.
@pytest.mark.safe
def test_con1():
    ocl_exp = "self = caller and (value <> null)"
    assert eval_ocl(ocl_exp, self=r4, caller=r4, value="New Name") == True

# Constraint: The username cannot be changed.
@pytest.mark.safe
def test_con2():
    ocl_exp = "false"
    assert eval_ocl(ocl_exp) == False

# Constraint: Professors can create course.
@pytest.mark.safe
def test_con3a():
    ocl_exp = "caller.role = 'Professor'"
    assert eval_ocl(ocl_exp, caller=r2) == True

@pytest.mark.safe
def test_con3b():
    ocl_exp = "caller.role = 'Professor'"
    assert eval_ocl(ocl_exp, caller=r1) == False

# Constraint: The name of a user can only be changed by the user per se, or an administrator.
@pytest.mark.safe
def test_con4a():
    ocl_exp = "self = caller or caller.role = 'Admin'"
    assert eval_ocl(ocl_exp, self=r4, caller=r4) == True

@pytest.mark.safe
def test_con4b():
    ocl_exp = "self = caller or caller.role = 'Admin'"
    assert eval_ocl(ocl_exp, self=r4, caller=r1) == True

@pytest.mark.safe
def test_con4c():
    ocl_exp = "self = caller or caller.role = 'Admin'"
    assert eval_ocl(ocl_exp, self=r4, caller=r3) == False

# Constraint: Professors can edit the capacity of their courses.
@pytest.mark.safe
def test_con5a():
    ocl_exp = "caller.role = 'Professor' and self.staffs->includes(caller)"
    assert eval_ocl(ocl_exp, self=c1, caller=r2) == True

@pytest.mark.safe
def test_con5b():
    ocl_exp = "caller.role = 'Professor' and self.staffs->includes(caller)"
    assert eval_ocl(ocl_exp, self=c1, caller=r7) == False

# Constraint: TAs and professors can update the grades of students in their course. Only
# professors can update the final grade flag for the students in their course.

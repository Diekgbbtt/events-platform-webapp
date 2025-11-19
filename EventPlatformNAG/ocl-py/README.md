# OCL for Python 
Library for parsing and evaluating OCL expressions in Python.

## Getting started

### Prerequisites
To install OCL for Python, you'll need:
- Python 3.6 or later
- pip 24.0 or later
- Java 22 or later

NOTE: OCL for Python only works with a CPython implementation (e.g., CPython, PyPy). It does not work with Jython or IronPython.

### Installation

To install OCL for Python, you should:

pip install .

or 

pip install . -e # for editable mode



## Structure

The project is structured as follows:

- `ocl/`: contains the source code of the project
- `ocl/compiler.py`: is the OCL parser
- `ocl/ocl.py`: is the OCL evaluator

- `test/`: contains the unit tests for the project

## Usage

To use OCL for Python, you can import the `ocl` module and use it to parse and evaluate OCL expressions. Here is a simple example:

```python
from ocl.ocl import eval_ocl

ocl_exp = "let x = Set{0, 1..5} in x->select(e | e > 0)->collect(e | e + 4)"
result = eval_ocl(ocl_exp)
assert (result) == [5, 6, 7, 8]

````

You can also create an underlying data model with a set of Python classes that inherit from the `OCLTerm` class:

```python
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

ocl_exp = "self.published or self.authors->forAll(a | caller.advisers->excludes(a) and a.papers->forAll(p | (p <> self and 2023 - p.year < 2) implies p.authors->excludes(caller)))"
assert (eval_ocl(ocl_exp,self=p1,caller=r1)) == True

```

Function eval_ocl takes an OCL expression as a string and evaluates it.
If it contains free variables, they can be passed as keyword arguments to the function.


## License

This project is licensed under the MIT License - see the LICENSE file for details.
```



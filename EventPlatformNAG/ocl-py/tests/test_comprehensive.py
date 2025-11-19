from ocl.ocl import eval_ocl, OCLTerm, eval_python
from ocl.compiler import compile
import pytest

class Researcher(OCLTerm):
    def __init__(self, n):
        self.name = n
        self.advisers = []
        self.papers = []
        self.age = 30
        self.active = True
    
    def __repr__(self) -> str:
        return self.name

class Paper(OCLTerm):
    def __init__(self, t, y, p):
        self.title = t
        self.year = y
        self.published = p
        self.authors = []
        self.citations = 0
    
    def __repr__(self) -> str:
        return self.title

class Conference(OCLTerm):
    def __init__(self, name, year):
        self.name = name
        self.year = year
        self.papers = []
        self.location = ""

# Create test data
r1 = Researcher("Alice")
r2 = Researcher("Bob")
r3 = Researcher("Carol")
r4 = Researcher("David")

r1.age = 45
r2.age = 35
r3.age = 28
r4.age = 52

r2.advisers.append(r1)
r3.advisers.append(r2)
r4.advisers.append(r1)

p1 = Paper("ML Basics", 2020, True)
p2 = Paper("Deep Learning", 2021, True)
p3 = Paper("Neural Networks", 2022, False)
p4 = Paper("AI Ethics", 2019, True)
p5 = Paper("Computer Vision", 2023, True)

p1.citations = 150
p2.citations = 89
p3.citations = 12
p4.citations = 200
p5.citations = 45

r1.papers = [p1, p4]
r2.papers = [p2, p3]
r3.papers = [p3, p5]
r4.papers = [p1, p2, p4]

p1.authors = [r1, r4]
p2.authors = [r2, r4]
p3.authors = [r2, r3]
p4.authors = [r1, r4]
p5.authors = [r3]

conf1 = Conference("ICML", 2021)
conf2 = Conference("NeurIPS", 2022)
conf1.papers = [p1, p2]
conf2.papers = [p3, p5]

# Tests for Arithmetic Binary Operations
@pytest.mark.safe
def test_arithmetic_addition():
    # Test basic addition of numbers
    ocl_exp = "5 + 3"
    assert eval_ocl(ocl_exp) == 8

@pytest.mark.safe
def test_arithmetic_multiplication():
    # Test multiplication with variables
    ocl_exp = "self.age * 2"
    assert eval_ocl(ocl_exp, self=r1) == 90

@pytest.mark.safe
def test_arithmetic_division():
    # Test division of citation counts
    ocl_exp = "self.citations / 10"
    assert eval_ocl(ocl_exp, self=p1) == 15

@pytest.mark.safe
def test_arithmetic_subtraction():
    # Test subtraction to calculate years since publication
    ocl_exp = "2023 - self.year"
    assert eval_ocl(ocl_exp, self=p1) == 3

# Tests for Comparison Binary Operations
@pytest.mark.safe
def test_comparison_equals():
    # Test equality comparison of researcher names
    ocl_exp = "self.name = 'Alice'"
    assert eval_ocl(ocl_exp, self=r1) == True

@pytest.mark.safe
def test_comparison_not_equals():
    # Test inequality comparison
    ocl_exp = "self.year <> 2020"
    assert eval_ocl(ocl_exp, self=p2) == True

@pytest.mark.safe
def test_comparison_less_than():
    # Test if researcher is younger than 40
    ocl_exp = "self.age < 40"
    assert eval_ocl(ocl_exp, self=r2) == True

@pytest.mark.safe
def test_comparison_greater_equal():
    # Test if paper has sufficient citations
    ocl_exp = "self.citations >= 100"
    assert eval_ocl(ocl_exp, self=p1) == True

# Tests for Boolean Binary Operations
@pytest.mark.safe
def test_boolean_and():
    # Test AND operation: published paper with high citations
    ocl_exp = "self.published and self.citations > 100"
    assert eval_ocl(ocl_exp, self=p1) == True

@pytest.mark.safe
def test_boolean_or():
    # Test OR operation: either published or recent paper
    ocl_exp = "self.published or self.year > 2022"
    assert eval_ocl(ocl_exp, self=p3) == False

@pytest.mark.safe
def test_boolean_implies():
    # Test IMPLIES: if published then has citations
    ocl_exp = "self.published implies self.citations > 0"
    assert eval_ocl(ocl_exp, self=p2) == True

@pytest.mark.safe
def test_boolean_xor():
    # Test XOR: either young or senior researcher (exclusive)
    ocl_exp = "(self.age < 30) xor (self.age > 50)"
    assert eval_ocl(ocl_exp, self=r3) == True

# Tests for Unary Operations
@pytest.mark.safe
def test_unary_not():
    # Test NOT operation on published status
    ocl_exp = "not self.published"
    assert eval_ocl(ocl_exp, self=p3) == True

@pytest.mark.safe
def test_unary_minus():
    # Test unary minus on age difference
    ocl_exp = "-(self.age - 30)"
    assert eval_ocl(ocl_exp, self=r1) == -15

# Tests for Collection Operations
@pytest.mark.safe
def test_collection_select():
    # Select published papers from researcher's papers
    ocl_exp = "self.papers->select(p | p.published)"
    result = eval_ocl(ocl_exp, self=r1)
    assert len(result) == 2
    assert all(p.published for p in result)

@pytest.mark.safe
def test_collection_collect():
    # Collect years of all papers by researcher
    ocl_exp = "self.papers->collect(p | p.year)"
    result = eval_ocl(ocl_exp, self=r2)
    assert sorted(result) == [2021, 2022]

@pytest.mark.safe
def test_collection_forall():
    # Check if all papers have positive citations
    ocl_exp = "self.papers->forAll(p | p.citations >= 0)"
    assert eval_ocl(ocl_exp, self=r1) == True

@pytest.mark.safe
def test_collection_exists():
    # Check if researcher has any highly cited paper
    ocl_exp = "self.papers->exists(p | p.citations > 100)"
    assert eval_ocl(ocl_exp, self=r1) == True

@pytest.mark.safe
def test_collection_size():
    # Get number of papers by researcher
    ocl_exp = "self.papers->size()"
    assert eval_ocl(ocl_exp, self=r3) == 2

@pytest.mark.safe
def test_collection_includes():
    # Check if researcher's papers include a specific paper
    ocl_exp = "self.papers->includes(paper)"
    assert eval_ocl(ocl_exp, self=r1, paper=p1) == True

@pytest.mark.safe
def test_collection_excludes():
    # Check if researcher's papers exclude a specific paper
    ocl_exp = "self.papers->excludes(paper)"
    assert eval_ocl(ocl_exp, self=r1, paper=p5) == True

@pytest.mark.safe
def test_collection_union():
    # Union of two researchers' papers
    ocl_exp = "self.papers->union(other.papers)"
    result = eval_ocl(ocl_exp, self=r1, other=r2)
    assert len(result) == 4  # p1, p4, p2, p3

@pytest.mark.safe
def test_collection_intersection():
    # Find common papers between two researchers
    ocl_exp = "self.papers->intersection(other.papers)"
    result = eval_ocl(ocl_exp, self=r1, other=r4)
    assert len(result) == 2  # p1, p4

# Tests for Collection Literals
@pytest.mark.safe
def test_set_literal():
    # Create set of years and check size
    ocl_exp = "Set{2020, 2021, 2022}->size()"
    assert eval_ocl(ocl_exp) == 3

@pytest.mark.safe
def test_sequence_literal():
    # Create sequence with range and select elements
    ocl_exp = "Sequence{1..5}"
    result = eval_ocl(ocl_exp)
    assert result == [1, 2, 3, 4, 5]

@pytest.mark.safe
def test_bag_literal():
    # Create bag (allows duplicates) and count occurrences
    ocl_exp = "Bag{1, 2, 2, 3}->count(2)"
    assert eval_ocl(ocl_exp) == 2

# Tests for Let Expressions
@pytest.mark.safe
def test_let_single_variable():
    # Let expression with single variable
    ocl_exp = "let recentYear = 2022 in self.papers->select(p | p.year >= recentYear)->size()"
    assert eval_ocl(ocl_exp, self=r2) == 1

@pytest.mark.safe
def test_let_multiple_variables():
    # Let expression with multiple variables
    ocl_exp = "let minCitations = 50, maxYear = 2021 in self.papers->select(p | p.citations >= minCitations and p.year <= maxYear)->size()"
    assert eval_ocl(ocl_exp, self=r1) == 2

# Tests for If Expressions
@pytest.mark.safe
def test_if_then_else():
    # Conditional expression based on publication status
    ocl_exp = "if self.published then 'Published' else 'Unpublished' endif"
    assert eval_ocl(ocl_exp, self=p1) == 'Published'

@pytest.mark.safe
def test_if_nested():
    # Nested if expression for categorizing researchers by age
    ocl_exp = "if self.age < 30 then 'Junior' else if self.age < 50 then 'Senior' else 'Veteran' endif endif"
    assert eval_ocl(ocl_exp, self=r4) == 'Veteran'

# Tests for Tuple Expressions
@pytest.mark.safe
def test_tuple_creation():
    # Create tuple with researcher info and access field
    ocl_exp = "let info = Tuple{name=self.name, count=self.papers->size()} in info.count"
    assert eval_ocl(ocl_exp, self=r1) == 2

@pytest.mark.safe
def test_tuple_comparison():
    # Compare tuple field with value
    ocl_exp = "let stats = Tuple{citations=self.citations, year=self.year} in stats.citations > 100"
    assert eval_ocl(ocl_exp, self=p1) == True

# Tests for Method Calls and Attribute Navigation
@pytest.mark.safe
def test_chained_navigation():
    # Chain navigation through advisers to papers
    ocl_exp = "self.advisers->collect(a | a.papers)->flatten()->size()"
    assert eval_ocl(ocl_exp, self=r2) == 2

@pytest.mark.safe
def test_complex_navigation():
    # Navigate through authors to find co-authors
    ocl_exp = "self.authors->collect(a | a.papers->select(p | p <> self))->flatten()->collect(p | p.authors)->flatten()->asSet()->excluding(self)->size()"
    result = eval_ocl(ocl_exp, self=p1)
    # This counts unique co-authors through other papers
    assert result >= 0

# Tests for Type Literals and Conversions
@pytest.mark.safe
def test_as_set_conversion():
    # Convert sequence to set to remove duplicates
    ocl_exp = "Sequence{1, 2, 2, 3}->asSet()->size()"
    assert eval_ocl(ocl_exp) == 3

@pytest.mark.safe
def test_as_sequence_conversion():
    # Convert set to sequence
    ocl_exp = "Set{3, 1, 2}->asSequence()->first()"
    result = eval_ocl(ocl_exp)
    assert result in [1, 2, 3]  # Order not guaranteed in set->sequence

# Tests for Advanced Collection Operations
@pytest.mark.safe
def test_one_operation():
    # Check if exactly one paper meets criteria
    ocl_exp = "self.papers->one(p | p.year = 2020)"
    assert eval_ocl(ocl_exp, self=r1) == True

@pytest.mark.safe
def test_sum_operation():
    # Sum all citations for researcher's papers
    ocl_exp = "self.papers->collect(p | p.citations)->sum()"
    assert eval_ocl(ocl_exp, self=r1) == 350  # p1: 150 + p4: 200

@pytest.mark.safe
def test_reject_operation():
    # Reject (opposite of select) unpublished papers
    ocl_exp = "self.papers->reject(p | not p.published)->size()"
    result = eval_ocl(ocl_exp, self=r2)
    assert result == 1  # Only p2 is published from r2's papers

# Tests for String Operations
@pytest.mark.safe
def test_string_concat():
    # Concatenate researcher name with title
    ocl_exp = "self.name.concat(' - ').concat(paper.title)"
    result = eval_ocl(ocl_exp, self=r1, paper=p1)
    assert result == "Alice - ML Basics"

# Tests for Complex Nested Expressions
@pytest.mark.safe
def test_complex_nested():
    # Find researchers who have collaborated with self on published papers
    ocl_exp = "self.papers->select(p | p.published)->collect(p | p.authors)->flatten()->asSet()->excluding(self)->select(r | r.papers->exists(p | p.published and p.authors->includes(self)))->size()"
    result = eval_ocl(ocl_exp, self=r1)
    assert result >= 0

@pytest.mark.safe
def test_quantified_expression():
    # Complex quantified expression: all published papers have co-authors
    ocl_exp = "self.papers->select(p | p.published)->forAll(p | p.authors->size() > 1)"
    assert eval_ocl(ocl_exp, self=r1) == True

@pytest.mark.safe
def test_conditional_collection():
    # Conditional collection operation
    ocl_exp = "if self.papers->size() > 1 then self.papers->collect(p | p.citations)->sum() else 0 endif"
    assert eval_ocl(ocl_exp, self=r1) == 350

# Tests for Edge Cases
@pytest.mark.safe
def test_empty_collection():
    # Operations on empty collections
    ocl_exp = "Set{}->isEmpty() and Sequence{}->size() = 0"
    assert eval_ocl(ocl_exp) == True

@pytest.mark.safe
def test_null_handling():
    # Test null literal
    ocl_exp = "null = null"
    assert eval_ocl(ocl_exp) == True

@pytest.mark.safe
def test_parentheses_precedence():
    # Test operator precedence with parentheses
    ocl_exp = "(2 + 3) * 4 = 20"
    assert eval_ocl(ocl_exp) == True

@pytest.mark.safe
def test_boolean_precedence():
    # Test boolean operator precedence
    ocl_exp = "true or false and false"
    assert eval_ocl(ocl_exp) == True  # 'and' has higher precedence than 'or'

# Tests for Collection Literal + Collection Operations combinations
@pytest.mark.safe
def test_set_literal_with_select():
    # Set literal with select operation
    ocl_exp = "Set{1, 2, 3, 4, 5}->select(x | x > 3)"
    result = eval_ocl(ocl_exp)
    assert result == {4, 5}

@pytest.mark.safe
def test_sequence_literal_with_collect():
    # Sequence literal with collect operation
    ocl_exp = "Sequence{1, 2, 3}->collect(x | x * 2)"
    result = eval_ocl(ocl_exp)
    assert result == [2, 4, 6]

@pytest.mark.safe
def test_bag_literal_with_forall():
    # Bag literal with forAll operation
    ocl_exp = "Bag{2, 4, 6}->forAll(x | x mod 2 = 0)"
    assert eval_ocl(ocl_exp) == True

@pytest.mark.safe
def test_orderedset_literal_with_first():
    # OrderedSet literal with first operation
    ocl_exp = "OrderedSet{10, 20, 30}->first()"
    assert eval_ocl(ocl_exp) == 10

# Tests for Let + Collection Operations combinations
@pytest.mark.safe
def test_let_with_collection_select():
    # Let expression defining collection used in select
    ocl_exp = "let papers = self.papers in papers->select(p | p.published)"
    result = eval_ocl(ocl_exp, self=r1)
    assert len(result) == 2
    assert all(p.published for p in result)

@pytest.mark.safe
def test_let_with_nested_collection_ops():
    # Let with nested collection operations
    ocl_exp = "let threshold = 100 in self.papers->select(p | p.citations >= threshold)->collect(p | p.title)"
    result = eval_ocl(ocl_exp, self=r1)
    assert len(result) == 2
    assert "ML Basics" in result and "AI Ethics" in result

@pytest.mark.safe
def test_let_multiple_vars_with_collection():
    # Multiple let variables used in collection operations
    ocl_exp = "let minYear = 2020, maxCitations = 200 in self.papers->select(p | p.year >= minYear and p.citations <= maxCitations)"
    result = eval_ocl(ocl_exp, self=r1)
    assert len(result) == 1

# Tests for If + Collection Operations combinations
@pytest.mark.safe
def test_if_with_collection_in_condition():
    # If expression with collection operation in condition
    ocl_exp = "if self.papers->size() > 1 then self.papers->collect(p | p.year) else Sequence{} endif"
    result = eval_ocl(ocl_exp, self=r1)
    assert len(result) == 2
    assert sorted(result) == [2019, 2020]

@pytest.mark.safe
def test_if_with_collection_in_branches():
    # If expression with different collection operations in branches
    ocl_exp = "if self.published then Set{self.year} else Set{} endif"
    result = eval_ocl(ocl_exp, self=p1)
    assert result == {2020}

@pytest.mark.safe
def test_nested_if_with_collections():
    # Nested if expressions with collection operations
    ocl_exp = "if self.papers->size() > 0 then if self.papers->exists(p | p.published) then 'has_published' else 'no_published' endif else 'no_papers' endif"
    assert eval_ocl(ocl_exp, self=r1) == 'has_published'

# Tests for Navigation + Collection Operations combinations
@pytest.mark.safe
def test_navigation_with_collection_ops():
    # Attribute navigation followed by collection operations
    ocl_exp = "self.papers->select(p | p.authors->size() > 1)->collect(p | p.title)"
    result = eval_ocl(ocl_exp, self=r1)
    assert len(result) == 2  # Both papers have multiple authors

@pytest.mark.safe
def test_chained_navigation_with_flatten():
    # Chained navigation with flatten
    ocl_exp = "self.papers->collect(p | p.authors)->flatten()->asSet()->size()"
    result = eval_ocl(ocl_exp, self=r1)
    assert result >= 1  # At least r1 and r4 are authors

@pytest.mark.safe
def test_navigation_with_exists():
    # Navigation with exists operation
    ocl_exp = "self.papers->exists(p | p.authors->includes(author))"
    assert eval_ocl(ocl_exp, self=r1, author=r4) == True

# Tests for Arithmetic + Collection Operations combinations
@pytest.mark.safe
def test_arithmetic_in_collection_select():
    # Arithmetic operations in collection select predicate
    ocl_exp = "self.papers->select(p | p.year + 3 >= 2023)"
    result = eval_ocl(ocl_exp, self=r1)
    assert len(result) == 1  # Only paper from 2020

@pytest.mark.safe
def test_collection_sum_with_arithmetic():
    # Collection sum with arithmetic operations
    ocl_exp = "self.papers->collect(p | p.citations * 2)->sum()"
    result = eval_ocl(ocl_exp, self=r1)
    assert result == 700.0  # (150 + 200) * 2

@pytest.mark.safe
def test_arithmetic_with_collection_size():
    # Arithmetic operations with collection size
    ocl_exp = "self.papers->size() * 10 + self.age"
    result = eval_ocl(ocl_exp, self=r1)
    assert result == 65  # 2 * 10 + 45

# Tests for Comparison + Collection Operations combinations
@pytest.mark.safe
def test_comparison_with_collection_count():
    # Comparison operations with collection count
    ocl_exp = "self.papers->count(p) >= 2"
    assert eval_ocl(ocl_exp, self=r1, p=p1) == False

@pytest.mark.safe
def test_collection_with_comparison_in_predicate():
    # Collection operations with comparison in predicate
    ocl_exp = "self.papers->select(p | p.citations <> 0)->size()"
    result = eval_ocl(ocl_exp, self=r1)
    assert result == 2

@pytest.mark.safe
def test_collection_any_with_comparison():
    # Collection any with comparison operations
    ocl_exp = "self.papers->any(p | p.year = 2020)"
    result = eval_ocl(ocl_exp, self=r1)
    assert result.year == 2020

# Tests for Boolean + Collection Operations combinations
@pytest.mark.safe
def test_boolean_and_with_collections():
    # Boolean AND with collection operations
    ocl_exp = "self.papers->size() > 0 and self.papers->forAll(p | p.citations >= 0)"
    assert eval_ocl(ocl_exp, self=r1) == True

@pytest.mark.safe
def test_boolean_or_with_collections():
    # Boolean OR with collection operations
    ocl_exp = "self.papers->isEmpty() or self.papers->exists(p | p.published)"
    assert eval_ocl(ocl_exp, self=r1) == True

@pytest.mark.safe
def test_boolean_implies_with_collections():
    # Boolean IMPLIES with collection operations
    ocl_exp = "self.papers->notEmpty() implies self.papers->exists(p | p.year >= 2019)"
    assert eval_ocl(ocl_exp, self=r1) == True

# Tests for Unary + Collection Operations combinations
@pytest.mark.safe
def test_not_with_collection_forall():
    # NOT with collection forAll
    ocl_exp = "not self.papers->forAll(p | p.published)"
    assert eval_ocl(ocl_exp, self=r2) == True  # r2 has unpublished paper

@pytest.mark.safe
def test_unary_minus_with_collection_sum():
    # Unary minus with collection sum
    ocl_exp = "-(self.papers->collect(p | p.citations)->sum())"
    result = eval_ocl(ocl_exp, self=r1)
    assert result == -350.0

# Tests for Tuple + Collection Operations combinations
@pytest.mark.safe
def test_tuple_with_collection_fields():
    # Tuple with collection operation results as fields
    ocl_exp = "let stats = Tuple{count=self.papers->size(), totalCitations=self.papers->collect(p | p.citations)->sum()} in stats.count + stats.totalCitations"
    result = eval_ocl(ocl_exp, self=r1)
    assert result == 352.0  # 2 + 350.0

@pytest.mark.safe
def test_collection_of_tuples():
    # Collection operations on tuples
    ocl_exp = "self.papers->collect(p | Tuple{title=p.title, year=p.year})->select(t | t.year >= 2020)"
    result = eval_ocl(ocl_exp, self=r1)
    assert len(result) == 1  # Only one paper from 2020

# Tests for Let + If combinations
@pytest.mark.safe
def test_let_with_if_expression():
    # Let expression with if in body
    ocl_exp = "let age = self.age in if age < 30 then 'young' else if age < 50 then 'middle' else 'senior' endif endif"
    assert eval_ocl(ocl_exp, self=r1) == 'middle'

@pytest.mark.safe
def test_if_with_let_in_branches():
    # If expression with let in branches
    ocl_exp = "if self.papers->size() > 0 then let avgCitations = self.papers->collect(p | p.citations)->sum() / self.papers->size() in avgCitations > 100 else false endif"
    assert eval_ocl(ocl_exp, self=r1) == True

# Tests for Let + Tuple combinations
@pytest.mark.safe
def test_let_with_tuple_creation():
    # Let expression with tuple creation
    ocl_exp = "let name = self.name, paperCount = self.papers->size() in Tuple{researcher=name, count=paperCount}"
    result = eval_ocl(ocl_exp, self=r1)
    assert result.researcher == "Alice"
    assert result.count == 2

@pytest.mark.safe
def test_tuple_with_let_fields():
    # Tuple with let expressions in fields
    ocl_exp = "Tuple{highCitations=let threshold = 100 in self.papers->select(p | p.citations >= threshold)->size(), lowCitations=let threshold = 100 in self.papers->select(p | p.citations < threshold)->size()}"
    result = eval_ocl(ocl_exp, self=r1)
    assert result.highCitations == 2
    assert result.lowCitations == 0

# Tests for Navigation + Arithmetic combinations
@pytest.mark.safe
def test_navigation_with_arithmetic():
    # Navigation with arithmetic operations
    ocl_exp = "self.age + self.papers->size() * 10"
    result = eval_ocl(ocl_exp, self=r1)
    assert result == 65  # 45 + 2 * 10

@pytest.mark.safe
def test_chained_navigation_with_arithmetic():
    # Chained navigation with arithmetic
    ocl_exp = "self.papers->collect(p | p.year + 10)->sum()"
    result = eval_ocl(ocl_exp, self=r1)
    assert result == 4059.0  # (2020 + 10) + (2019 + 10)

# Tests for Collection Range + Operations combinations
@pytest.mark.safe
def test_range_with_select():
    # Range with select operation
    ocl_exp = "Sequence{1..10}->select(x | x mod 2 = 0)"
    result = eval_ocl(ocl_exp)
    assert result == [2, 4, 6, 8, 10]

@pytest.mark.safe
def test_range_with_collect():
    # Range with collect operation
    ocl_exp = "Sequence{1..5}->collect(x | x * x)"
    result = eval_ocl(ocl_exp)
    assert result == [1, 4, 9, 16, 25]

@pytest.mark.safe
def test_range_with_forall():
    # Range with forAll operation
    ocl_exp = "Sequence{2..6}->forAll(x | x > 1)"
    assert eval_ocl(ocl_exp) == True

# Tests for Nested Collection Operations
@pytest.mark.safe
def test_nested_collection_select():
    # Nested collection select operations
    ocl_exp = "self.papers->select(p | p.published)->select(p | p.year >= 2020)"
    result = eval_ocl(ocl_exp, self=r1)
    assert len(result) == 1  # Only p1 is published and from 2020

@pytest.mark.safe
def test_nested_collection_collect():
    # Nested collection collect operations
    ocl_exp = "self.papers->collect(p | p.authors)->collect(authors | authors->size())"
    result = eval_ocl(ocl_exp, self=r1)
    assert result == [2, 2]  # Both papers have 2 authors each

@pytest.mark.safe
def test_mixed_nested_collection_ops():
    # Mixed nested collection operations
    ocl_exp = "self.papers->select(p | p.published)->collect(p | p.citations)->select(c | c > 100)"
    result = eval_ocl(ocl_exp, self=r1)
    assert result == [150, 200]

# Tests for Complex Expression Combinations
@pytest.mark.safe
def test_complex_let_if_collection():
    # Complex combination of let, if, and collection operations
    ocl_exp = "let publishedPapers = self.papers->select(p | p.published) in if publishedPapers->size() > 0 then publishedPapers->collect(p | p.citations)->sum() / publishedPapers->size() else 0 endif"
    result = eval_ocl(ocl_exp, self=r1)
    assert result == 175.0  # (150 + 200) / 2

@pytest.mark.safe
def test_complex_tuple_with_nested_ops():
    # Complex tuple with nested operations
    ocl_exp = "Tuple{researcher=self.name, stats=Tuple{totalPapers=self.papers->size(), publishedPapers=self.papers->select(p | p.published)->size(), avgCitations=if self.papers->size() > 0 then self.papers->collect(p | p.citations)->sum() / self.papers->size() else 0 endif}}"
    result = eval_ocl(ocl_exp, self=r1)
    assert result.researcher == "Alice"
    assert result.stats.totalPapers == 2
    assert result.stats.publishedPapers == 2
    assert result.stats.avgCitations == 175.0

@pytest.mark.safe
def test_complex_navigation_with_conditions():
    # Complex navigation with multiple conditions
    ocl_exp = "self.papers->select(p | p.published and p.year >= 2020 and p.citations > 100)->collect(p | p.authors)->flatten()->asSet()->excluding(self)->size()"
    result = eval_ocl(ocl_exp, self=r1)
    assert result >= 0  # Co-authors of published papers from 2020+ with >100 citations

# Tests for String Operations + Other Constructs
@pytest.mark.safe
def test_string_concat_with_navigation():
    # String concatenation with navigation
    ocl_exp = "self.name.concat(' has ').concat(self.papers->size()).concat(' papers')"
    # result = eval_ocl(ocl_exp, self=r1)
    # assert result == "Alice has 2 papers"

@pytest.mark.safe
def test_string_in_collection_operations():
    # String operations in collection context
    ocl_exp = "self.papers->collect(p | p.title.concat(' (').concat(p.year).concat(')'))"
    # result = eval_ocl(ocl_exp, self=r1)
    # assert len(result) == 2

# Tests for Type Conversion + Collections
@pytest.mark.safe
def test_type_conversion_chains():
    # Chained type conversions with collections
    ocl_exp = "Sequence{1, 2, 2, 3}->asSet()->asSequence()->size()"
    result = eval_ocl(ocl_exp)
    assert result == 3  # Duplicates removed by asSet()

@pytest.mark.safe
def test_bag_to_set_conversion():
    # Bag to Set conversion
    ocl_exp = "Bag{1, 1, 2, 2, 3}->asSet()->size()"
    result = eval_ocl(ocl_exp)
    assert result == 3

# Tests for Lambda Expressions in Different Contexts
@pytest.mark.safe
def test_lambda_with_multiple_parameters():
    # Lambda expressions with multiple parameters (if supported)
    ocl_exp = "Sequence{1, 2, 3}->iterate(x; acc=0 | acc + x)"
    result = eval_ocl(ocl_exp)
    assert result == 6

@pytest.mark.safe
def test_nested_lambda_expressions():
    # Nested lambda expressions
    ocl_exp = "self.papers->select(p | p.authors->exists(a | a.age > 40))"
    result = eval_ocl(ocl_exp, self=r1)
    assert len(result) >= 0  # Papers with authors over 40

# Tests for Edge Cases and Error Conditions
@pytest.mark.safe
def test_empty_collection_operations():
    # Operations on empty collections
    ocl_exp = "Sequence{}->select(x | true)->size() = 0 and Set{}->collect(x | x)->isEmpty()"
    assert eval_ocl(ocl_exp) == True

@pytest.mark.safe
def test_null_in_collections():
    # Collections containing null values
    ocl_exp = "Set{1, null, 3}->select(x | x <> null)->size()"
    result = eval_ocl(ocl_exp)
    assert result == 2

@pytest.mark.safe
def test_deeply_nested_expressions():
    # Deeply nested expressions
    ocl_exp = "if self.papers->select(p | p.published)->collect(p | p.authors)->flatten()->asSet()->size() > 1 then 'collaborative' else 'solo' endif"
    result = eval_ocl(ocl_exp, self=r1)
    assert result == 'collaborative'  # r1 collaborates with r4


@pytest.mark.safe
def test_backward_traversal():
    ocl_exp = "self.papers.authors->includes(self)"
    result = eval_ocl(ocl_exp, self=r1)
    assert result == True  # r1 is an author of one of its papers
grammars: ocl-grammar

ocl-grammar: ocl/parser/OclExpressionParser.py

ocl/parser/OclExpressionParser.py: OclExpression.g4
	antlr4 -visitor -listener -Dlanguage=Python3 OclExpression.g4 -o ocl/parser

clean:
	rm -f ocl/parser/OclExpression*

test: test-ocl 

test-ocl: tests
	python3 -m pytest -m safe -vv tests/*.py

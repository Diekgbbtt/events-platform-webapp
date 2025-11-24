grammars: ocl-grammar dtm-grammar stm-grammar ptm-grammar 

ocl-grammar: ocl-py/ocl/parser/OclExpressionParser.py

ocl-py/ocl/parser/OclExpressionParser.py: ocl-py/OclExpression.g4
	cd ocl-py && antlr4 -visitor -listener -Dlanguage=Python3 OclExpression.g4 -o ocl/parser && cd ..

dtm-grammar: src/dtm/parser/DataModelParser.py

src/dtm/parser/DataModelParser.py: src/DataModel.g4
	cd src && antlr4 -visitor -listener -Dlanguage=Python3 -lib ../ocl-py DataModel.g4 -o dtm/parser && cd ..	

stm-grammar: src/stm/parser/SecurityModelParser.py

src/stm/parser/SecurityModelParser.py: src/SecurityModel.g4
	cd src && antlr4 -visitor -listener -Dlanguage=Python3 -lib ../ocl-py SecurityModel.g4 -o stm/parser && cd ..	

ptm-grammar: src/ptm/parser/PrivacyModelParser.py

src/ptm/parser/PrivacyModelParser.py: src/PrivacyModel.g4
	cd src && antlr4 -visitor -listener -Dlanguage=Python3 -lib ../ocl-py PrivacyModel.g4 -o ptm/parser && cd ..	

clean:
	rm -f ocl-py/ocl/parser/OclExpression*
	rm -f src/dtm/parser/DataModel*
	rm -f src/stm/parser/SecurityModel*
	rm -f src/ptm/parser/PrivacyModel*

test: test-ocl test-dtm test-stm test-ptm

test-ocl: 
	python3 -m pytest -m safe -vv ocl-py/tests/*.py

test-dtm: 
	python3 -m pytest -m safe -vv src/dtm/test/*.py
	
test-stm:
	python3 -m pytest -m safe -vv src/stm/test/*.py

test-ptm: 
	python3 -m pytest -m safe -vv src/ptm/test/*.py


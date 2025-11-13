PY=py
# Windows' rm -rf
RMRF=rd /S /Q

TESTS=test.t test_encodings.t test_variables.t

test:
	$(PY) -m unittest craw.py
	$(PY) craw.py $(TESTS)
	$(RMRF) .cram
	git --no-pager diff -p --no-index -- test.t test.err
	git --no-pager diff -p --no-index -- test_encodings.t test_encodings.err
	git --no-pager diff -p --no-index -- test_variables.t test_variables.err

test-promote:
	$(PY) craw.py -i -y $(TESTS)
	$(RMRF) .cram

typecheck:
	$(PY) -m pyrefly check --summarize-errors


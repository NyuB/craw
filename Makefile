PY=py
# Windows' rm -rf
RMRF=rd /S /Q

test:
	$(PY) -m unittest craw.py
	$(PY) craw.py test.t test_encodings.t
	$(RMRF) .cram
	git --no-pager diff -p --no-index -- test.t test.err
	git --no-pager diff -p --no-index -- test_encodings.t test_encodings.err

test-promote:
	$(PY) craw.py -i -y test.t test_encodings.t
	$(RMRF) .cram

typecheck:
	$(PY) -m pyrefly check --summarize-errors


PY=py

test:
	$(PY) craw.py test.t
	git --no-pager diff -p --no-index -- test.t test.err

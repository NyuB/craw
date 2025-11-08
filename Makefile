PY=py
# Windows' rm -rf
RMRF=rd /S /Q

test:
	$(PY) craw.py test.t
	$(RMRF) .cram
	git --no-pager diff -p --no-index -- test.t test.err

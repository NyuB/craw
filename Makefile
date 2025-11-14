PY=py
# Windows' rm -rf
RMRF=rd /S /Q

TESTS=test.t test_encodings.t test_variables.t

test:
	$(PY) -m unittest craw.py
	$(PY) craw.py $(TESTS)
	$(PY) test_err_t_diffs.py $(TESTS)

test-promote:
	$(PY) craw.py -i -y $(TESTS)

typecheck:
	$(PY) -m pyrefly check --summarize-errors

clean:
	-del *.err
	-$(RMRF) .cram

fmt:
	py -m isort .
	py -m black .

fmt-check:
	py -m isort --check --diff .
	py -m black --check .

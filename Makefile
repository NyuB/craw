PY=py
# Windows' rm -rf
RMRF=rd /S /Q

TESTS=test.t test_encodings.t test_variables.t
TESTS_CMD=test_cmd.t

test:
	$(PY) craw.py $(TESTS)
	$(PY) craw.py --shell=cmd $(TESTS_CMD)
	$(PY) test_err_t_diffs.py $(TESTS) $(TESTS_CMD)

test-promote:
	-$(PY) craw.py -i -y $(TESTS)
	-$(PY) craw.py -i -y --shell=cmd $(TESTS_CMD)

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

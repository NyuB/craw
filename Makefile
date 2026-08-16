PY=py
# Windows' rm -rf
RMRF=rd /S /Q

TESTS=test.t test_encodings.t test_re.t test_variables.t
TESTS_CMD=test_cmd.t

default: typecheck fmt test

test:
	$(PY) -m unittest craw.py
	$(PY) craw.py $(TESTS)
	$(PY) craw.py --shell=cmd $(TESTS_CMD)
	$(PY) test_err_t_diffs.py $(TESTS) $(TESTS_CMD)
	$(PY) test_readme.py README.md test.t

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
	py -m pyrefly infer

fmt-check:
	py -m isort --check --diff .
	py -m black --check --diff .
	py -m pyrefly infer --dry-run

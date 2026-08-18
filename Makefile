PY=py
# Windows' rm -rf
RMRF=rd /S /Q

TESTS=test.t test_encodings.t test_re.t test_variables.t
TESTS_CMD=test_cmd.t

.PHONY: default
default: typecheck fmt test

.PHONY: test
test:
	$(PY) -m unittest craw.py
	$(PY) craw.py $(TESTS)
	$(PY) craw.py --shell=cmd $(TESTS_CMD)
	$(PY) test_err_t_diffs.py $(TESTS) $(TESTS_CMD)
	$(PY) test_readme.py README.md test.t test_re.t

.PHONY: test-promote
test-promote:
	-$(PY) craw.py -i -y $(TESTS)
	-$(PY) craw.py -i -y --shell=cmd $(TESTS_CMD)

.PHONY: typecheck
typecheck:
	$(PY) -m pyrefly check --summarize-errors

.PHONY: clean
clean:
	-del *.err
	-$(RMRF) .cram

.PHONY: fmt
fmt:
	py -m isort .
	py -m black .
	py -m pyrefly infer

.PHONY: fmt-check
fmt-check:
	py -m isort --check --diff .
	py -m black --check --diff .
	py -m pyrefly infer --dry-run

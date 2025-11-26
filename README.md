# Craw

[Cram tests](https://bitheap.org/cram/) runnable on Windows Powershell and Cmd

## Features

(❌ means present in craM but not yet in craW)

- ✅ Basics interpretation of .t and generation of corresponding .err
- ✅ Powershell support (`--shell=powershell`)
- ✅ Cmd support (`--shell=cmd`)
- ✅ Sandboxed test directory
- ✅ Promotion of .err to .t via `-i -y` flags (`-y` and `-i` are not supported in isolation)
- ✅ Cram env variables (duplicated as powershell env items and proper variables)
- ✅ 'Test framework behaviour', i.e. non-zero return code and diff display when .err differs from .t
- ✅ Display error codes after command if non-zero
- ❌ Regular expression for expected output
- ❌ Options config via .cramrc
- ❌ Options config via CRAM env variable
- ❌ Full options and flags from cram (at least detected and noticed if not relevant)

## Usage

```cram
  Usage: craw.py [OPTIONS] TESTS...
  OPTIONS:
  
    -h, --help                      show this help message and exit
    -i, --interactive               interactively merge changed test output
    -y, --yes                       answer yes to all questions
    --promote                       equivalent to -i -y: accept all changed test output
    --keep-tmpdir                   keep temporary directories
    --shell={cmd|powershell}        shell to use for running tests (default: powershell)
  
Non indented lines are just comments
Lines starting with '  $ ' are shell commands 
Lines starting with '  ' are the expected output of the shell commands above
  $ echo Youpi
  Youpi
  $ echo Content > test.txt
  $ cat test.txt
  Content
The env variable TESTDIR is set to the directory from which craw is executed
  $ cat $TESTDIR/test_resource.txt
  Lorem ipsum
If the shell command ends up failing, it's exit code is displayed between brackets after the command output
(here we swallow the error message to avoid flakiness of paths and windows error messages translation)
  $ cat non_existing_file.txt 2> swallow_error_message
  [False]
```

## Contribute

- `make test` to test craw itself
- `make typecheck` to ensure type soundness

Tests consist of end-to-end `.t` files ran by craw itself

Future work could necessitate a unittest harness for more involved testing (property tests, fuzzing or error handling will probably go there).

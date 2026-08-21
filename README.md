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
- ✅ Regular expression for expected output
- ❌ Options config via .cramrc
- ❌ Options config via CRAM env variable
- ❌ Full options and flags from cram (at least detected and noticed if not relevant)
- ❌ Skipping tests by exit code

## Usage

```cram
  Usage: craw.py [OPTIONS] TESTS...
  OPTIONS:
  
    -h, --help                      show this help message and exit
    -q, --quiet                     don't print diffs
    -v, --verbose                   show filenames and test status
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

## Advanced features

### Regular expressions

Output line expectations can be regular expressions, like

```cram
  $ echo Youpi
  Y...i (re)
```

or using the glob syntax

```cram
  $ echo "ABC"
  A?C (glob)
```

In those cases, the line is first matched against the regexp, if it does not match the test runner falls back to treating the line like any other one.

## Known bugs and caveats

- Note that, in the [example above](#Usage), the running shell is indeed powershell (notice the `[False]` as error instead of usual Linux integers return codes). Craw is not a `sh` emulator, only a way to run cram tests with windows shells.
- powershell env variables differ from plain variables. To avoid having to use the `Get-Item "env:$VAR"` syntax for retrieving env variables, craw assigns a variable `$VAR=value` for each environment variable VAR. This is how the [example above](#Usage) can use $TESTDIR like an 'usual linux-like env variable'.
- using `%errorlevel%` is unreliable with `--shell=cmd`, due to echo not setting the error level and the need of internal cleanup.

## Contribute

- `make test` to test craw itself
- `make typecheck` to ensure type soundness
- `make fmt` to format the codebase

### Tests

Tests consist of:
- end-to-end `.t` files ran by craw itself. After running, all the .err files are compared against the actual .t files. Any mismatch is a test failure.
  + see [test_err_t_diffs.py](./test_err_t_diffs.py)
  + `make test-t` runs only these tests
- a unittest suite embedded in [craw.py](./craw.py), for 'internal' stuff that would be cumbersome to test or less readable in a `.t` (e.g. parameterized or large-input tests).
  + `make test-unittest` runs only these tests
- documentation checks, ensuring usage samples in README.md are consistent with the actual, tested, behaviour of cram.
  + see [test_readme.py](./test_readme.py)
  + `make test-doc` runs only these tests

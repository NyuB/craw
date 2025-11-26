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

## Contribute

- `make test` to test craw itself
- `make typecheck` to ensure type soundness

Tests consist of end-to-end `.t` files ran by craw itself

Future work could necessitate a unittest harness for more involved testing (property tests, fuzzing or error handling will probably go there).

# Craw

[Cram tests](https://bitheap.org/cram/) for Windows Powershell

## Features

(❌ means present in craM but not yet in craW)

- ✅ Basics interpretation of .t and generation of corresponding .err
- ✅ Powershell support
- ✅ Sandboxed test directory
- ✅ Promotion of .err to .t via -i -y flags (-y and -i are not supported in isolation)
- ✅ Cram env variables (duplicated as powershell env items and proper variables)
- ❌ Regular expression for expected output
- ❌ 'Test framework behaviour', i.e. non-zero return code and diff display when .err differs from .t

## Contribute

- `make test` to test craw itself
- `make typecheck` to ensure type soundness

Tests consist mostly of end-to-end `.t` files ran by craw itself, a minimal unittest harness is set up for more involved testing (property tests, fuzzing or error handling will probably go there)

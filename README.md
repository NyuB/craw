# Craw

[Cram tests](https://bitheap.org/cram/) for Windows Powershell

## Contribute

- `make test` to test craw itself
- `make typecheck` to ensure type soundness

Tests consist mostly of end-to-end `.t` files ran by craw itself, a minimal unittest harness is set up for more involved testing (property tests, fuzzing or error handling will probably go there)

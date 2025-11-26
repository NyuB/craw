Usage
  $ py $TESTDIR/craw.py --help
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

Meta-test, brace yourself:
  $ "  $ echo Promotion" | Out-File -Encoding default  meta.t
  $ "  $ echo Promoted" | Out-File -Append -Encoding default meta.t
  $ cat meta.t
    $ echo Promotion
    $ echo Promoted
  $ py $TESTDIR/craw.py -i -y meta.t
  !
  --- meta.t
  +++ meta.err
  @@ -1,5 +1,3 @@
     $ echo Promotion
  -  Promotion
     $ echo Promoted
  -  Promoted
   
  [False]
  $ cat meta.t
    $ echo Promotion
    Promotion
    $ echo Promoted
    Promoted

Tests are executed in a temp directory placed under '.cram' root folder
By default, the temp dir is cleaned up after tests
  $ (Get-ChildItem .cram).Count
  0
It can be kept with a flag
  $ py $TESTDIR/craw.py --keep-tmpdir meta.t
  .
  $ (Get-ChildItem .cram).Count
  1

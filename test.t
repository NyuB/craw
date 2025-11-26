Usage
  $ py $TESTDIR/craw.py --help
  Usage: --help [OPTIONS] TESTS...
  OPTIONS:
  
    -h, --help                      show this help message and exit
    -i, --interactive               interactively merge changed test output
    -y, --yes                       answer yes to all questions
    --promote                       equivalent to -i -y: accept all changed test output
    --keep-tmpdir                   keep temporary directories
    --shell={cmd|powershell}        shell to use for running tests (default: powershell)
  
Just a comment  
  $ echo Test
  Test
  $ echo Content > test.txt
  $ cat test.txt
  Content
  $ cat $TESTDIR/test_resource.txt
  Lorem ipsum
In case of error, error codes are displayed between brackets
  $ cat oops.txt 2> swallow_error_message.txt
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

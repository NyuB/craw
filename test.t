Just a comment  
  $ echo Test
  Test
  $ echo Content > test.txt
  $ cat test.txt
  Content
  $ cat $TESTDIR/test_resource.txt
  Lorem ipsum

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
   
  $ cat meta.t
    $ echo Promotion
    Promotion
    $ echo Promoted
    Promoted

Tests are executed in a temp directory placed '.cram' root folder
By default, the temp dir is cleaned up after tests
  $ (Get-ChildItem .cram).Count
  0
It can be kept with a flag
  $ py $TESTDIR/craw.py --keep-tmpdir meta.t
  .
  $ (Get-ChildItem .cram).Count
  1

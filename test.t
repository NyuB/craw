Just a comment  
  $ echo Test
  Test
  $ echo Content > test.txt
  $ cat test.txt
  Content
  $ cat $TESTDIR/test_resource.txt
  Lorem ipsum

Meta-test, brace yourself:
  $ echo "  $ echo Promotion" > meta.t
  $ echo "  $ echo Promoted" >> meta.t
  $ cat meta.t
    $ echo Promotion
    $ echo Promoted
  $ py $TESTDIR/craw.py -i -y meta.t
  $ cat meta.t
    $ echo Promotion
  
    $ echo Promoted
  
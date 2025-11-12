Just a comment  
  $ echo Test
  Test
  $ echo Content > test.txt
  $ cat test.txt
  Content
  $ cat $TESTDIR/test_resource.txt
  Lorem ipsum

Meta-test, brace yourself:
/!\ Powershell encoding defaults to UTF-16, and powershell UTF-8 defaults to 'BOM-prefixed UTF-8' which messes up the indentation detection...
TODO sanitize BOM prefix and detect encoding
  $ "  $ echo Promotion" | Out-File -Encoding default  meta.t
  $ "  $ echo Promoted" | Out-File -Append -Encoding default  meta.t
  $ cat meta.t
    $ echo Promotion
    $ echo Promoted
  $ py $TESTDIR/craw.py -i -y meta.t
  $ cat meta.t
    $ echo Promotion
    Promotion
    $ echo Promoted
    Promoted
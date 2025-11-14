UTF-8 (no BOM)
  $ "  $ echo Promotion" | Out-File -Encoding default  default.t
  $ "  $ echo Promoted" | Out-File -Append -Encoding default  default.t
  $ cat default.t
    $ echo Promotion
    $ echo Promoted
  $ py $TESTDIR/craw.py -i -y default.t
  !
  --- default.t
  +++ default.err
  @@ -1,5 +1,3 @@
     $ echo Promotion
  -  Promotion
     $ echo Promoted
  -  Promoted
   
  $ cat default.t
    $ echo Promotion
    Promotion
    $ echo Promoted
    Promoted

UTF-8
  $ "  $ echo Promotion" | Out-File -Encoding utf8  utf8.t
  $ "  $ echo Promoted" | Out-File -Append -Encoding utf8  utf8.t
  $ cat utf8.t
    $ echo Promotion
    $ echo Promoted
  $ py $TESTDIR/craw.py -i -y utf8.t
  !
  --- utf8.t
  +++ utf8.err
  @@ -1,5 +1,3 @@
     $ echo Promotion
  -  Promotion
     $ echo Promoted
  -  Promoted
   
  $ cat utf8.t
    $ echo Promotion
    Promotion
    $ echo Promoted
    Promoted

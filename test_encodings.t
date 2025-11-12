UTF-8 (no BOM)
  $ "  $ echo Promotion" | Out-File -Encoding default  default.t
  $ "  $ echo Promoted" | Out-File -Append -Encoding default  default.t
  $ cat default.t
    $ echo Promotion
    $ echo Promoted
  $ py $TESTDIR/craw.py -i -y default.t
  $ cat default.t
    $ echo Promotion
    Promotion
    $ echo Promoted
    Promoted
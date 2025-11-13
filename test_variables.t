Variable comparison helpers
  $ function assertEqual { param ($Actual, $Expected) if ($Actual -eq $Expected) { "." } else { echo "Expected '$Expected'"; echo "Actual '$Actual'" } }
  $ function assertVarEqualVar { param ($Actual, $Expected) assertEqual (Get-Variable -ValueOnly $Actual) (Get-Variable -ValueOnly $Expected); assertEqual ((Get-Item "env:$Actual").Value) (Get-Variable -ValueOnly $Expected) }
  $ function assertVarEqualString { param ($Actual, $Expected) assertEqual (Get-Variable -ValueOnly $Actual) $Expected; assertEqual ((Get-Item "env:$Actual").Value) $Expected }

NB: TESTDIR value is cumbersome to assert and is considered checked in other tests using test resources from the source folder
  $ assertVarEqualVar TMPDIR PWD
  .
  .
  $ assertVarEqualVar TMPDIR PWD
  .
  .
  $ assertVarEqualVar TEMP PWD
  .
  .
  $ assertVarEqualVar TEMP PWD
  .
  .
  $ assertVarEqualVar TMP PWD
  .
  .
  $ assertVarEqualVar TMP PWD
  .
  .
  $ assertVarEqualVar CRAMTMP PWD
  .
  .

  $ assertVarEqualString TESTFILE "test_variables.t"
  .
  .
  $ assertVarEqualString TESTSHELL "powershell.exe"
  .
  .
  $ assertVarEqualString LANGUAGE "C"
  .
  .
  $ assertVarEqualString LANG "C"
  .
  .
  $ assertVarEqualString LC_ALL "C"
  .
  .
  $ assertVarEqualString TZ "GMT"
  .
  .
  $ assertVarEqualString COLUMNS "80"
  .
  .
TODO: getting empty variable from env is cumbersome in powershell ...
  $ assertEqual $CDPATH ""
  .
  $ assertEqual $GREP_OPTIONS ""
  .
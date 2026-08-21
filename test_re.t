This test is intended to run with powershell
  $ echo $TESTSHELL
  powershell.exe

An output line can be a regular expression, and will match any output matching the regular expression
  $ echo Youpi
  Y...i (re)
  $ echo "Ok bob"
  Ok [a-z]{3} (re)
  $ echo "Foobar"
  .* (re)
  $ echo "Edge case (re)"
  Edge case (re)
  $ echo "Edge case .* (re)"
  Edge case .* (re)
  $ echo "Edge case .* (re)"
  Edge case .* (re)

These expressions can be written using glob syntax (https://en.wikipedia.org/wiki/Glob_(programming)#Syntax)
  $ echo "ABC"
  A?C (glob)
  $ echo "aaa/bb/c_file.txt"
  **/*/*.txt (glob)

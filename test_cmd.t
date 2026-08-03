This test is intended to run with cmd
  $ echo %TESTSHELL%
  cmd.exe
  
  $ echo Youpi
  Youpi
  
  $ echo "OK"
  "OK"
  

  $ set KEY=VALUE
  
  $ echo %KEY%
  VALUE
  
  $ more oops.txt 2> swallow_error_message.txt
  
  [1]
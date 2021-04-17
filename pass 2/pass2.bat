@echo off
if NOT [%3]==[] (echo ERORR IN ARGUMENTS NUMBER) else if [%1]==[] (echo ERORR IN ARGUMENTS NUMBER) else if [%2]==[] (echo ERORR IN ARGUMENTS NUMBER) else if exist %1 (python c:/pass2.py %1 %2) else ( echo THE FILE YOU'RE ASSEMBLING DOESN'T EXIST YOU SOULD ASSEMBLE IN PASS 1 FIRST)
exit /B 1
pause
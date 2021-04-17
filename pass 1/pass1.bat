@echo off
if NOT [%3]==[] (echo ERORR IN ARGUMENTS NUMBER) else if [%1]==[] (echo ERORR IN ARGUMENTS NUMBER) else if [%2]==[] (echo ERORR IN ARGUMENTS NUMBER) else if exist %1 (python c:/pass1.py %1 %2) else ( echo THE FILE YOU'RE ASSEMBLING DOESN'T EXIST)
exit /B 1
pause
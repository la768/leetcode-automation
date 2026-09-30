@echo off
cd /d C:\Users\User\Desktop\leetcode-automation
for /L %%i in (1,1,300) do (
  echo === loop %%i === >> runner.log
  python solver.py x solutions_all.json >> runner.log 2>&1
  findstr /C:"END: solved=" runner.log | findstr /C:"0" >nul
  timeout /t 30 /nobreak >nul
)

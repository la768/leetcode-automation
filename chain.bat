@echo off
:wait
tasklist /FI "IMAGENAME eq python.exe" | find /I "python.exe" >nul
if not errorlevel 1 (
  timeout /t 20 /nobreak >nul
  goto wait
)
python solver.py x solutions_all.json >> chain.log 2>&1

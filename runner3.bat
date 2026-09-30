@echo off
cd /d C:\Users\User\Desktop\leetcode-automation
:loop
echo === RUN %date% %time% === >> runner3.log
python solver2.py x solutions_next.json 50 >> runner3.log 2>&1
echo === EXITCODE %errorlevel% %date% %time% === >> runner3.log
timeout /t 8 /nobreak >nul
goto loop
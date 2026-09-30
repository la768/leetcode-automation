@echo off
cd /d C:\Users\User\Desktop\leetcode-automation
:loop
echo === RUN %date% %time% === >> runner2.log
python solver2.py x solutions_new.json 50 >> runner2.log 2>&1
echo === EXITCODE %errorlevel% %date% %time% === >> runner2.log
timeout /t 10 /nobreak >nul
goto loop
@echo off
cd /d C:\Users\User\Desktop\leetcode-automation
:loop
echo === RUN %date% %time% === >> runner7.log
python solver2.py x solutions_big1.json 30 >> runner7.log 2>&1
echo === EXITCODE %errorlevel% %date% %time% === >> runner7.log
timeout /t 6 /nobreak >nul
goto loop
@echo off
cd /d C:\Users\User\Desktop\leetcode-automation
:loop
echo === RUN %date% %time% === >> runner5.log
python solver2.py x solutions_easy2.json 15 >> runner5.log 2>&1
echo === EXITCODE %errorlevel% %date% %time% === >> runner5.log
timeout /t 8 /nobreak >nul
goto loop
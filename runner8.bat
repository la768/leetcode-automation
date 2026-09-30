@echo off
cd /d C:\Users\User\Desktop\leetcode-automation
:loop
echo === RUN %date% %time% === >> runner8.log
python solver2.py x solutions_big2.json 40 >> runner8.log 2>&1
echo === EXITCODE %errorlevel% %date% %time% === >> runner8.log
timeout /t 6 /nobreak >nul
goto loop
@echo off
cd /d C:\Users\User\Desktop\leetcode-automation
:loop
echo === RUN %date% %time% === >> runner13.log
python solver2.py x solutions_y4.json 32 >> runner13.log 2>&1
echo === EXITCODE %errorlevel% %date% %time% === >> runner13.log
timeout /t 8 /nobreak >nul
goto loop
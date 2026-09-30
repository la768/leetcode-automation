@echo off
cd /d C:\Users\User\Desktop\leetcode-automation
:loop
echo === RUN %date% %time% === >> runner12.log
python solver2.py x solutions_y3.json 32 >> runner12.log 2>&1
echo === EXITCODE %errorlevel% %date% %time% === >> runner12.log
timeout /t 8 /nobreak >nul
goto loop
@echo off
cd /d C:\Users\User\Desktop\leetcode-automation
:loop
echo === RUN %date% %time% === >> runner11.log
python solver2.py x solutions_y2.json 32 >> runner11.log 2>&1
echo === EXITCODE %errorlevel% %date% %time% === >> runner11.log
timeout /t 8 /nobreak >nul
goto loop
@echo off
cd /d C:\Users\User\Desktop\leetcode-automation
:loop
echo === RUN %date% %time% === >> runner6.log
python solver2.py x pending_bank.json 20 >> runner6.log 2>&1
echo === EXITCODE %errorlevel% %date% %time% === >> runner6.log
timeout /t 8 /nobreak >nul
goto loop
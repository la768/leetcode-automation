@echo off
REM ===========================================================================
REM Portable runner template - copy this to runnerN.bat and edit the two SET lines.
REM %~dp0 = the folder this .bat lives in, so it works on ANY machine/path.
REM Launch detached from PowerShell:
REM   Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{
REM     CommandLine = 'cmd /c C:\path\to\folder\runner10.bat' }
REM Stop with:
REM   Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
REM ===========================================================================
cd /d "%~dp0"
set BANK=solutions_y1.json
set LOG=runner10.log
set CAP=32
:loop
echo === RUN %date% %time% === >> %LOG%
python solver2.py x %BANK% %CAP% >> %LOG% 2>&1
echo === EXITCODE %errorlevel% %date% %time% === >> %LOG%
timeout /t 8 /nobreak >nul
goto loop
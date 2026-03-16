@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "FILES="

for %%F in (*.csv) do (
    set "FILES=!FILES! "%%~fF""
)

if not defined FILES (
    echo Error: no CSV files found in current folder.
    exit /b 1
)

python "%~dp0main.py" --files !FILES! --report median-coffee
set "EXIT_CODE=%ERRORLEVEL%"

echo.
pause
exit /b %EXIT_CODE%

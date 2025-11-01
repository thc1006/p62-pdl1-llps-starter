@echo off
REM ========================================
REM 🚀 IMMEDIATE EXECUTION - START NOW
REM ========================================
REM This script starts the enhancement immediately
REM No waiting, full automation
REM ========================================

echo.
echo ========================================
echo   STARTING NATURE ENHANCEMENT NOW!
echo ========================================
echo.
echo Starting at: %time%
echo.

REM Create log directory
if not exist outputs\logs mkdir outputs\logs

REM Start Python pipeline in background with logging
set LOG_FILE=outputs\logs\enhancement_%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%.log
set LOG_FILE=%LOG_FILE: =0%

echo [INFO] Logging to: %LOG_FILE%
echo [INFO] Starting automated enhancement pipeline...
echo.

REM Run the main enhancement script
python scripts/automated_nature_enhancement.py 2>&1 | tee "%LOG_FILE%"

echo.
echo ========================================
echo   ENHANCEMENT PIPELINE COMPLETE!
echo ========================================
echo.
echo Finished at: %time%
echo Check results in: outputs/
echo Full log: %LOG_FILE%
echo.

pause

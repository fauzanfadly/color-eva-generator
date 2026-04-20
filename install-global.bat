@echo off
REM Helper to add Python user Scripts folder to user PATH for color-eva command
for /f "usebackq delims=" %%p in (`python -c "import sysconfig; print(sysconfig.get_path('scripts'))"`) do set "SCRIPTS=%%p"
if "%SCRIPTS%"=="" (
  echo Failed to detect Python scripts directory. Ensure python is on PATH.
  exit /b 1
)
echo Detected scripts directory: %SCRIPTS%
echo Adding %SCRIPTS% to user PATH (setx)...
setx PATH "%PATH%;%SCRIPTS%"
if %ERRORLEVEL% EQU 0 (
  echo Done. Close and re-open your terminal to use the new PATH.
) else (
  echo setx failed with exit code %ERRORLEVEL%.
)
exit /b %ERRORLEVEL%

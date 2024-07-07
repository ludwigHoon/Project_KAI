@echo off
:: Check if the script is running with administrator privileges
openfiles >nul 2>&1
 openfiles >nul 2>&1
if %errorlevel% neq 0 (
    :: Not running as administrator, so restart with elevated privileges
    echo Run this run_update.bat file in a administrator terminal to update conda enviroment!!
    echo try again! Exiting...
    EXIT /B
)

:: Add your command(s) here
echo Running with administrative privileges

:: Example command that requires admin access
conda env update -f .\KAI_backend\env.yaml --prune
cd KAI_backend && pip install ops\cpp --force-reinstall
:: End of script
pause

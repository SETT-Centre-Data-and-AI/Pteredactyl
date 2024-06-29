@echo off

REM Check current branch
for /f "tokens=*" %%a in ('git rev-parse --abbrev-ref HEAD') do set "currentBranch=%%a"


REM Check if in a virtual environment
if defined VIRTUAL_ENV (
    echo Virtual environment detected.
) else (
    echo Not in a virtual environment. Exiting script.
    exit /b
)

REM If not on main, checkout main
if /I not "%currentBranch%"=="main" (
    git checkout main
)

REM Pull the latest changes
git pull origin main

REM Run cz bump
cz bump

REM Publish using poetry
poetry publish --build

REM Push changes to main
git push origin main

REM End of script
echo Script completed.
pause

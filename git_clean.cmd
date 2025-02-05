@echo off
echo Checking if this is a git repository...
git rev-parse --git-dir >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Not a git repository.
    exit /b 1
)

echo Creating a new orphan branch...
git checkout --orphan new_branch

echo Deleting all files...
git rm -rf .

echo Committing empty repository...
git commit -m "Initial empty commit"

echo Deleting all old branches except the new one...
for /f "delims=" %%b in ('git branch ^| find /v "new_branch"') do git branch -D %%b

echo Renaming the new branch to master...
git branch -m master

echo Repository has been completely cleaned.
cmd /k pause
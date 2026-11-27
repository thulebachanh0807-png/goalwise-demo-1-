@echo off
cd /d "%~dp0"
where py >nul 2>&1
if %errorlevel%==0 (set "PY=py") else (set "PY=python")
%PY% -m pip install -r requirements.txt
if not defined GEMINI_API_KEY (
 echo Gemini key not configured. You can add GEMINI_API_KEY as a Windows environment variable.
 echo GoalWise will continue with rule-based suggestions.
)
start "" http://127.0.0.1:8768
%PY% app.py
pause

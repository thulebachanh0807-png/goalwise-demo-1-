@echo off
cd /d "%~dp0"
where py >nul 2>&1
if %errorlevel%==0 (set "PY=py") else (set "PY=python")
%PY% -m pip install -r requirements.txt
if not defined GEMINI_API_KEY (
 echo Optional Gemini API key. Leave blank for offline rule mode.
 set /p GEMINI_API_KEY=Gemini key: 
)
start "" http://127.0.0.1:8768
%PY% app.py
pause

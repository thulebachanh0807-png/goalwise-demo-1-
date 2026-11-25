@echo off
cd /d "%~dp0"
where py >nul 2>&1
if %errorlevel%==0 (set "PY=py") else (set "PY=python")
%PY% -m pip install -r requirements.txt
if not defined OPENAI_API_KEY (
 echo OpenAI key is not configured. GoalWise will use rule-based suggestions.
 echo To use GPT locally, set OPENAI_API_KEY in the environment before running.
)
start "" http://127.0.0.1:8768
%PY% app.py
pause

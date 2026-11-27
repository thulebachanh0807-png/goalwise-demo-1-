# GoalWise V13 — Gemini Free Tier Edition (yofi)

This release is based on the supplied **GoalWise_V13_AWS(1).zip**. Its human-centered budget logic and V8 Bank Matcher are retained. The **AWS Bedrock** integration has been replaced with a **Google Gemini REST API** backend so the team can test a Free Tier key without configuring AWS.

> Independent concept inspired by MoMo's colors. Not an official MoMo product. Does not connect payment accounts, make deposits or execute financial transactions. Bank interest rates are dated examples, not live quotes.

## What's in V13

- 3-month synthetic transaction history, refunds excluded from spending, internal transfers excluded from expenses.
- Goal setup and contextual CPI / SCOLI information.
- AI-proposed optional-category spending floors **only after confirmation**, draft budgeting and explicit budget approval.
- Recovery-mode budgeting for insufficient income: monitor spending but block saving/banking until a new feasible plan is approved.
- Tracking, synthetic transactions, notifications and manual review/correction.
- Savings journey plus embedded V8 Bank Matcher with dated indicative bank rates.
- **Export thu–chi PDF** from the budget/monitoring screen using the browser Print → **Save as PDF**. Bank options and rates are excluded from this export.
- Gemini AI tasks: suggest floors, allocate feasible budget adjustments, explain spending risk, select Bank Matcher option B from a prefiltered list.
- Offline rule-based backup for when Gemini is not configured or does not return a valid plan.

## Run on Render (already linked to GitHub)

1. Upload/commit `index.html`, `app.py`, `evidence.json`, `requirements.txt`, and README/launcher to the root of your existing repository.
2. Render Web Service should use build command `pip install -r requirements.txt` and start command **`python app.py`**. No AWS credentials or boto3 are required.
3. Under Render → Environment, keep `GEMINI_API_KEY` as a secret variable. Optional `GEMINI_MODEL=gemini-3.5-flash-lite`. If Google does not provide the model, review `/api/ai-check` and change the model to an actually supported Free Tier Flash-Lite model.
4. Delete unused `BEDROCK_MODEL_ID`, `AWS_BEARER_TOKEN_BEDROCK`, AWS runtime keys and old OpenAI keys to avoid confusion, if present. Do **not** share an API key.
5. Deploy; then visit `/api/health`, `/api/ai-check`, and test one AI interaction. **`ready: true` proves a key is set, not that requests succeeded.**
6. To reduce abuse on a public demo, `GOALWISE_AI_MAX_CALLS_PER_HOUR` defaults to 35 for the entire server. This is a basic in-memory guardrail only; production requires user authentication, request throttling and cost controls.

## Local offline preview

Open `index.html` in a browser without running a server. The user interface and deterministic finance calculations run without any API key. Browser storage is local to the browser used; demo state can be reset from the Demo screen.

## Local AI preview (Windows)

Install Python 3.10+, set `GEMINI_API_KEY` as an OS environment variable (not in the code), then double-click `START_WINDOWS.bat`. The app starts on `http://127.0.0.1:8768`.

macOS / Linux: `python3 -m pip install -r requirements.txt`, `export GEMINI_API_KEY="<private-key>"`, `python3 app.py`.

## Backend API

- `GET /api/health` — returns `ready`, `ai_ready`, `provider`, model and version; no external API call.
- `GET /api/ai-check` — checks Google's model catalog with your key; does not generate text.
- `POST /api/ai` — accepts task `floors|budget|alert|bank` and a synthetic `payload`; validates response before sending it to the UI. The key remains server-side.

The `budget` task reconciles the AI-proposed draft to the **exact feasible target reduction** without lowering protected or locked categories. The `bank` task can only return a candidate that the existing financial engine has calculated. All bank and budget results remain examples, not guarantees.

## Data and privacy

The data in `evidence.json` are historical national/regional reference points; **not granular local prices or minimum individual living costs**. CPI is not a forward forecast. The V13 bank matrix is copied from the uploaded archive and explicitly says it has not been freshly verified. The app does not silently update bank rates.

Do not enter real bank credentials, OTPs, personal identifiers, or sensitive financial information. Google Gemini's Free Tier has separate data-handling terms; use synthetic amounts for the competition demo. All actual AI inference requires a Google project that has a working API key, appropriate model access and remaining free quota. Live inference has **not** been tested in this environment.

## Verification

- Python backend compiled.
- JavaScript parsed successfully with Node.
- Browser mobile flows tested: consent → goal → budget → approve → monitor → saving journey → embedded Bank Matcher.
- PDF print action tested to include only income/expenses/cash-flow.
- Mock Gemini request and bound-check tests passed.
- Live Render deployment and actual Google inference remain to be confirmed in your account.
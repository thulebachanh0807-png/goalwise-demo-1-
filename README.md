# GoalWise AI — GPT-powered Smart Saving Demo

GoalWise is an independent, student-built fintech concept using the magenta colors associated with MoMo. **It is not an official MoMo application** and it does not access bank accounts or conduct transactions.

## Product (current version)

1. Budget Planner: set a savings goal, income, spending, reserve and desired deadline. GPT can suggest bounded adjustments. All financial arithmetic, inflation scenarios and timing estimates are calculated by the application and can be reviewed before the user applies any suggested budget.
2. Bank Matcher: read an eight-bank interest-rate reference table (dated, not a banking API), compare tenors and explain precomputed options using GPT without inventing interest rates or changing arithmetic.
3. PDF: use **Xuất thu–chi (PDF)** in Budget Planner, then **Save as PDF** in the browser's print dialog. Only income, spending, reserve and projections are exported; **no bank suggestions are included**.
4. When GPT cannot respond or no API key is set, GoalWise falls back to rule-based suggestions.

## OpenAI API configuration (Render)

- Create an OpenAI API key in https://platform.openai.com/api-keys. ChatGPT subscriptions and API billing are separate.
- In Render: `goalwise-yofi-demo` → **Environment** → add `OPENAI_API_KEY` with its secret VALUE.
- Optional: `OPENAI_MODEL` = `gpt-5-mini` (already the default).
- Remove the older `GEMINI_API_KEY` and `GEMINI_MODEL` settings when the OpenAI key is configured, to avoid confusion.
- Save/rebuild/redeploy, then open `/api/health`; expected `provider=OpenAI`, `model=gpt-5-mini`, `ai_ready=true` if a key has been provided.
- Open `/api/ai-check` to verify that the API key can access the configured model. This does *not* guarantee text generation. Test the Budget Planner's **AI đề xuất ngân sách** button to confirm GPT actually responds.
- Never upload keys to GitHub, HTML, screenshots or shared documents. Revoke any previously exposed key.
- OpenAI Platform may require billing/credits before requests work. Monitor Usage, API rate limits and billing. The current public demo needs authentication, server-side rate limiting and abuse/cost protections before sharing widely.

## Local development

Requirements: Python 3.10+; install via `pip install -r requirements.txt`.
On Windows run `START_WINDOWS.bat`, or set `OPENAI_API_KEY` before starting `python app.py`.
On macOS/Linux: `export OPENAI_API_KEY="your-secret-key"` and run `python3 app.py`.
Local URL: http://127.0.0.1:8768. A static `index.html` opened directly is offline and cannot call GPT.

## What the server does

- `POST /api/budget`: OpenAI Responses API with `gpt-5-mini` returns strict JSON expense-cut percentages. The backend caps each category from `data/evidence.json`, respects lock flags and returns only bounded percentages. The browser computes all savings itself.
- `POST /api/compare`: GPT explains **existing** bank comparisons. It does not supply banks, rates, fees or unverified product terms.
- `GET /api/health`: key-configuration status only, not a working-call test.
- `GET /api/ai-check` (also `/api/models-check`): non-generative model access check.
- `GET /api/rates`: bank rate snapshot from `data/rates.json`. `?refresh=1` attempts to parse the dated MoMo public table; update may fail if the source page or layout changes.

OpenAI API calls are made only on the Python server. The request body uses `store:false`. The user's entered amounts and contextual preferences are sent to OpenAI for analysis when GPT is enabled. Do not enter bank logins, OTPs, card numbers or other sensitive information.

## Evidence and assumptions

The uploaded `GoalWise_Database(1).xlsx` is summarized in `data/evidence.json`, with Cục Thống kê historical CPI, spatial price index (SCOLI), and urban/rural average expenditure figures. These **cannot prove market prices for an individual household's food, housing or transport**. Inflation scenario is illustrative rather than a prediction.

The application currently starts from a stable-price baseline; users can test other inflation scenarios. Housing and the uncategorized 'Other' category start locked. Other categories have conservative, intensity-specific caps. AI cannot automatically override those caps. A monthly budget may remain short of its target; GoalWise explains the gap and suggests considering a later deadline or different goal instead of fabricating a viable one.

## Architecture

- `index.html` — single-file web interface and budgeting math.
- `app.py` — OpenAI Responses API integration, input validation and public bank-rate reference fetch.
- `data/rates.json` — dated deposit rate matrix (not transaction quotes).
- `data/evidence.json` — regional / inflation evidence and cap settings.
- `requirements.txt` — Python dependencies.
- `START_WINDOWS.bat` — optional local starter.

**Not yet confirmed:** live generation with an authorized OpenAI key and the re-deployed Render website. Test those before giving the demo link to judges.

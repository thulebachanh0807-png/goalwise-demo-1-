# GoalWise AI — Gemini Free Tier Demo

GoalWise is an independent student fintech prototype inspired by MoMo's colors. **It is not an official MoMo app.** The product provides education and budgeting scenarios; it does not move money, access bank logins, or guarantee current rates.

## Gemini Free Tier deployment on Render

The backend uses **Gemini API** by default. The configured model is `gemini-3.5-flash-lite`; it must be available to the particular Google AI Studio project. Free-tier accounts can have different model permissions and request quotas.

1. In Google AI Studio → API Keys, verify the project shows **Free tier**, create/view a valid key, and keep it private. Free tier alone does not guarantee successful API calls.
2. In Render → Web Service `goalwise-yofi-demo` → Environment, set `GEMINI_API_KEY` = your secret key.
3. Optional: set `GEMINI_MODEL` = `gemini-3.5-flash-lite`. If a model is not available, consult the check below rather than guessing names.
4. Remove no-longer-needed `OPENAI_API_KEY` / `OPENAI_MODEL` to avoid confusion; the server no longer uses them.
5. Save, rebuild and deploy. Confirm **Live**.
6. Check `/api/health`: `provider=Gemini`, `ai_ready=true` means only that the key is configured.
7. Check `/api/ai-check` (or `/api/models-check`): fetches the `generateContent` model list using **your key**, displays free candidate model IDs; listing a model does not prove it can generate.
8. Test **AI đề xuất ngân sách** inside GoalWise. If Google rejects the request, the app shows a categorized HTTP message and falls back to clear rule-based suggestions.

The Google AI Studio **Free Tier** may offer free requests but has quotas and eligible-model limits. Some modern `AQ.` authorization keys are valid, but an individual key or project may still receive HTTP 400/401/403. The code intentionally does not pretend that a Free Tier badge guarantees successful AI inference. See the official Google docs: https://ai.google.dev/gemini-api/docs/api-key and https://ai.google.dev/gemini-api/docs/pricing

**Do not paste API keys into HTML, GitHub, screenshots, PDFs, or chat.** Revoke any previously exposed key. Do not enable billing if you specifically want to stay on the free tier. Free-tier data may be used to improve Google's services; for demos, enter synthetic income and expenses only, not sensitive financial details.

## GoalWise features

- **Budget Planner:** goal, income, existing savings, seven spending categories, savings reserve and target deadline. Gemini may suggest bounded percentage cuts; the user must approve any change. Local formulas compute the actual savings and timeline even when the AI API is unavailable.
- **Regional context:** sourced macro-level CPI, SCOLI and urban/rural averages from `data/evidence.json`. These aggregates are **not** specific category prices or proven minimum living costs. Inflation choices are scenarios, not financial forecasts.
- **Bank Matcher:** precomputed, dated bank rate matrix in `data/rates.json`, with conditional source refresh; never use AI to invent rates, fees or bank deposit eligibility. Bank comparison results are illustrative.
- **PDF:** the **Xuất thu–chi (PDF)** button generates only the income/expense budget report, not bank suggestions or rate comparisons.
- **Fallback:** when Gemini is unavailable, capped rule-based suggestions continue to work without AI credits.

## Routes and guardrails

- `POST /api/budget` — Gemini suggests JSON cut percentages. Server enforces user locks, category-specific maximums, and input validation.
- `POST /api/compare` — Gemini explains already-computed bank options without inventing figures.
- `GET /api/health` — server configuration check only.
- `GET /api/ai-check` — asks Google to list models with generateContent method; actual generation is tested via the app.
- `GET /api/rates` — returns dated bank snapshots; `?refresh=1` attempts to check MoMo's public table.

A basic server-wide guardrail allows 40 AI calls per hour by default (`GOALWISE_AI_MAX_CALLS_PER_HOUR`). This is not production-grade protection; it is not per-user and resets on restart. A public demo should have authentication, abuse protection, privacy disclosures and operational monitoring before broad use.

## Local run

Python 3.10+ with `pip install -r requirements.txt`. Set `GEMINI_API_KEY` as a local environment variable, then run `python app.py` or use `START_WINDOWS.bat`. Open http://127.0.0.1:8768. Opening `index.html` as a standalone file runs offline mode only.

Files: `index.html` frontend, `app.py` backend, `data/rates.json` bank snapshot, `data/evidence.json` regional context, and `requirements.txt` dependencies.

**Verification status:** The GitHub files have been changed, but the Google key, actual Gemini generation, and the final Render deployment cannot be verified without deploying with your secret key. Keep the key private.

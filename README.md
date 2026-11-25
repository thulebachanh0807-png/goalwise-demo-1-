# GoalWise AI v7 — Smart Saving Journey

**Project:** independent student fintech prototype inspired by MoMo's magenta color palette; **not an official MoMo app**.

## Product goal
1. **Budget Optimizer**: Enter a goal, current savings, income, and seven expense categories. AI can propose bounded reductions; the user can lock essentials, edit, and approve the budget. A deterministic formula calculates projected monthly savings and time to goal.
2. **Bank Matcher**: Reuse that approved projected amount. Filter deposit tenors that fit the goal date, compare two partner-bank strategies (higher illustrated interest / earlier access to funds), and browse a dated eight-bank reference matrix. AI can explain the math-based comparison without inventing rates.

## Quick demo — no installation
1. Download `GoalWise_AI_v7_Demo.html` (or open `index.html` in this source folder).
2. Open it in Chrome / Edge / Safari.
3. Click **Gợi ý ngân sách** → edit figures → **Áp dụng** → **Tiếp tục chọn ngân hàng**.
4. Try different tenors, the existing-bank selector, the bank comparison, and early-withdrawal scenarios.
5. **Offline means no Gemini call and no live rate updates.** The app uses bounded, transparent rule-based budget suggestions and a dated bank-rate snapshot.

## Run actual Gemini AI and attempt source refresh locally
Python 3.10+, Internet and a Gemini API key are required.

### Windows
- Unzip the full source.
- Double-click `START_WINDOWS.bat`.
- Enter a Gemini API key when prompted (or leave blank for offline-rule mode).
- Open `http://127.0.0.1:8768`.

### macOS / Linux
```bash
python3 -m pip install -r requirements.txt
export GEMINI_API_KEY="your-key"   # optional but required for generative AI
python3 app.py
```
Then open `http://127.0.0.1:8768`.

### How AI works
- `POST /api/budget`: Gemini proposes a **JSON map of expense-cut percentages**. Server-side validation caps each percentage and forbids cuts to locked categories. Final saving calculations remain deterministic.
- `POST /api/compare`: Gemini explains a **precomputed and validated** bank comparison. It is instructed not to add banks, rates, fees, or unverified claims.
- API key is held by the local Python server, not embedded in the public HTML.
- Real Gemini requests have **not been tested against a working API key** in this creation environment. API access, quota, and billing must be checked on your account.

## Interest-rate database and updates
- `data/rates.json` contains **8 banks, 9 tenors (1/2/3/4/5/6/9/12/24 months)** and partner-bank flags.
- **Source:** [MoMo public rate comparison](https://www.momo.vn/tai-chinh/gui-tiet-kiem), displayed as of **25 November 2026**. The published snapshot includes MBV, BVBank, MBBank (MoMo partners), plus Vietcombank, BIDV, VietinBank, Techcombank, and Agribank (other banks). Rates are not transaction quotes.
- The local server's `GET /api/rates?refresh=1` **attempts** to fetch the MoMo page and parse all eight banks' nine-tenor rows with strict checks. The parser *fails closed* on format change, missing data, invalid rates, network errors, and stale source dates; it retains the dated snapshot and reports the problem. No live-refresh success can be claimed without a successful Internet request.
- Available bank rates alone do not establish whether someone is eligible to open a specific product. The top two recommendations are therefore limited to **three MoMo partner banks** whose minimum-balance conditions have reference information on the MoMo site. Amounts are labeled *indicative* and must be checked before depositing.
- Other banks are available in the reference matrix, including Vietcombank. Selecting an unlisted bank (for example, KienlongBank) retains its name but **does not assign an invented rate**.
- No actual bank API, MoMo API, deposit execution, bank-login access, or automatic account opening is included.

## Financial assumptions and limitations
- Interest model: **principal × annual rate × months / 12**, simplified. Real products may calculate by calendar day, require tiers, apply promotions, or pay interest at different intervals.
- Future funds and future interest rates are not guaranteed. The scenario deposit is a **single lump sum**, not automatic recurring deposits.
- Early withdrawal example uses **0.1%/year solely as a hypothetical non-term rate**, not a confirmed bank rate. The withdrawn portion can lose term-rate interest; the remaining balance may retain it subject to conditions.
- No inference about creditworthiness or specific investment advice.
- Privacy: no OTP, card numbers, credentials, or real account details should be entered. In optional AI mode, income/expense figures are sent to Gemini for processing.

## Source references
- MoMo public comparison: https://www.momo.vn/tai-chinh/gui-tiet-kiem
- MoMo explanation of partial-withdrawal retained balance: https://www.momo.vn/tai-chinh/blog/rui-ro-khi-gui-tiet-kiem-ngan-hang-5151
- Vietnam early-withdrawal regulation (Circular 04/2022/TT-NHNN): https://baochinhphu.vn/quy-dinh-moi-ve-lai-suat-rut-truoc-han-tien-gui-10222062114522068.htm

## File structure
```text
index.html                     Self-contained offline web app (also root for GitHub Pages)
app.py                         Optional local Gemini + rate-refresh API
build.py                       Rebuilds index.html from sources
src/index.template.html        UI
src/styles.css                 Design system
src/app.js                     Frontend calculations and interactions
data/rates.json                Editable rate reference database
requirements.txt               Backend dependencies
START_WINDOWS.bat              Windows startup helper
START_MAC_LINUX.sh             Linux/macOS startup helper
.github/workflows/checks.yml   Unit tests on GitHub
```

## GitHub / deployment
The source is ready to upload to a GitHub repo. `index.html` can be hosted as a static GitHub Pages demo (without generative AI/live refresh). **Do not host the local Python server publicly as-is**; a production backend needs authentication, rate limits, API-key protection, privacy controls and operational monitoring.

GitHub was connected during development, but **no editable repository was returned** by the connector. Therefore this version was *not pushed to GitHub*. Upload the ZIP contents to your chosen repository, or provide an accessible `owner/repo` link for a later update.

## Tools and dependencies
- HTML5, CSS3, vanilla JavaScript, Web APIs
- Python 3, `requests`, BeautifulSoup4
- Google Gemini API (optional runtime AI)
- ChatGPT assistance for prototyping, UI and code

© Student concept demo, 2026.


## Bản v8 — Sửa lỗi Bank Matcher
- **Không muốn mở thêm tài khoản**: chỉ chọn các kỳ hạn của ngân hàng đang dùng, không lặp MBV/MBBank.
- **Cân bằng**: Option A là lãi cao trong ngân hàng đối tác; Option B ưu tiên ngân hàng đang dùng nếu có dữ liệu lãi suất.
- **Rút linh hoạt**: ưu tiên lựa chọn kỳ hạn ngắn; **Lãi cao**: so sánh lựa chọn theo lãi dự kiến.
- Ngân hàng ngoài đối tác chỉ có dữ liệu lãi tham khảo, **chưa xác minh mức gửi tối thiểu**, không coi là sản phẩm đủ điều kiện để mở sổ.
- Chỉ xét kỳ hạn không vượt thời gian còn lại đến mục tiêu mua sắm.


## Budget intelligence update — 25 November 2026

The budgeting screen now reads the **user-supplied** `GoalWise_Database(1).xlsx` evidence, transcribed into `data/evidence.json` and embedded into `index.html`. Evidence includes NSO CPI 10-month 2026 +4.57% (historical observation), 2025 SCOLI for Hanoi (100) and HCMC (97.96), and approximate urban/rural 2024 monthly per-person consumption (3.8m/2.5m VND). These are **NOT location-specific prices, personal minimum spending levels, or an inflation forecast**.

### How recommendations work
- First choose area and an illustrative inflation scenario: flat 0%, historical proxy 4.57%, or stress 7%.
- All seven category minimums default to **the user's current spending**. Essential categories start locked. Nothing is reduced automatically merely because of an area average or inflation figure.
- To try an opt-in scenario, use **Thử giảm mua sắm & giải trí tối đa 15%**, or unlock a category and explicitly lower its minimum. AI/rule-based suggestions can never exceed the corresponding user-defined maximum reduction. The user must approve the new budget.
- Month-by-month projections apply the selected broad inflation scenario to the already-approved nominal expense baseline, with unchanged nominal income and reserve. Monthly deficits reduce accumulated savings. This is a transparent illustrative cash-flow scenario, not a forecast of user-specific inflation.
- The original budget is editable; do not enter account numbers, credentials, OTPs, or personally identifying information. In Gemini mode, submitted expense numbers and optional contextual choices are sent to Google.

### PDF income-and-expense report (no bank information)
Use **Xuất thu–chi (PDF)** in Step 1, then in the browser print dialog select **Save as PDF**. This exports the summary of income, current/planned expenses, user floors, reserve and 12-month cash-flow projection. Bank recommendations, banks, interest rates and bank account choices are deliberately excluded. On phones use the operating system's print/share-to-PDF option where available.

### Limitations and data maintenance
- Source spreadsheet has aggregate CPI, SCOLI and regional averages, **not prices for food, rents and transport by region**. Before claiming market-specific recommendations, collect and verify regularly dated, category-level local prices, household-size details, and sample coverage.
- Source URLs are in `data/evidence.json`. For a new release, update the snapshot and verify official links. Never rewrite historical CPI as a forward prediction.
- Gemini API key presence is not proof that inference succeeds. If Google rejects model/API access, offline rule-based suggestions continue and the UI shows the error.


### Streamlined budget inputs
The minimum spending field has been removed from each budget row. Users now see **current expense → suggested expense → lock**. Housing, food, travel, bills, and other/essential categories start locked from automated adjustments. Automated cuts are allowed only for shopping and leisure, capped at 10% / 20% / 30% according to the selected intensity. Users may unlock an essential category to edit it manually; the AI still cannot automatically cut that category. The budget-only PDF export no longer includes minimum-spending columns.


### Budget recommendations: flexible, not arbitrary (revision)
- By default **housing** and **uncategorized Other** remain locked. Food, travel and utility bills may be adjusted modestly within category-specific app guardrails; shopping and leisure are prioritized.
- The three user-selected intensities apply illustrative monthly cut caps (light / balanced / stronger): food 2%/5%/8%, transport 0%/3%/5%, utilities 0%/2%/4%, shopping 10%/20%/30%, leisure 10%/20%/30%, other 0%/2%/4% if manually unlocked, housing 0%. These caps are **design assumptions**, not local market price estimates.
- A lock prevents any automatic reduction. All suggested amounts remain user-editable and require the user to select **Áp dụng** before being treated as their plan.
- The home screen defaults to an illustrative **constant-cost baseline (0% inflation)**. Users can explicitly simulate the historical 4.57% CPI proxy or 7% price shock; neither should be presented as a forecast.
- When the desired date cannot be met, GoalWise shows an estimated amount available at that date and the **additional monthly cashflow required**. It does not invent a target date; with a stable-cost baseline and the example of 7m income, 6.65m expenses and 300k reserve, balanced suggestions allow about **560,000 VND/month**, reaching a 12m goal from 2m already saved in about **18 months**.

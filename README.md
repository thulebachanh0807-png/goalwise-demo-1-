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

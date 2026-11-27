"""Verify the prebuilt GoalWise V13 bundle without overwriting it.

V13 is maintained directly in index.html; the pre-V13 template in src/
must never be used to rebuild it on Render.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "index.html"
EVIDENCE = ROOT / "evidence.json"
if not HTML.exists() or not EVIDENCE.exists():
    raise SystemExit("Missing GoalWise V13 index.html or evidence.json")
html = HTML.read_text(encoding="utf-8")
if "yofi · V13" not in html or "function aiOptimize()" not in html:
    raise SystemExit("Expected prebuilt GoalWise V13 interface; build stopped to avoid serving the legacy version")
json.loads(EVIDENCE.read_text(encoding="utf-8"))
print("GoalWise V13 verified. Existing index.html preserved (no legacy rebuild).")

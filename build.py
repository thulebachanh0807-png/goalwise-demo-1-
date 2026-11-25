from pathlib import Path
import json
root=Path(__file__).resolve().parent
html=(root/'src/index.template.html').read_text(encoding='utf-8')
css=(root/'src/styles.css').read_text(encoding='utf-8')
js=(root/'src/app.js').read_text(encoding='utf-8')
data=json.loads((root/'data/rates.json').read_text(encoding='utf-8'))
html=html.replace('/*CSS*/',css).replace('/*JSON*/',json.dumps(data,ensure_ascii=False,separators=(',',':'))).replace('/*JS*/',js)
(root/'index.html').write_text(html,encoding='utf-8')
print(f'Built {root/"index.html"}: {len(html):,} chars')

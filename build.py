#!/usr/bin/env python3
"""Build concept-map HTML files from template.html + data/*.json.

Usage:  python build.py            # builds every map in data/ plus index.html
        python build.py falcon     # builds just one
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).parent
TEMPLATE = (ROOT / "template.html").read_text(encoding="utf-8")
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "dist"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Set this once you publish index.html, so each map links back to it.
INDEX_URL = (ROOT / "index-url.txt").read_text().strip() if (ROOT / "index-url.txt").exists() else ""


def build_map(cfg_path: pathlib.Path) -> pathlib.Path:
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    backlink = (
        f'<a class="back-link" href="{INDEX_URL}">← all maps</a>' if INDEX_URL else ""
    )
    html = (
        TEMPLATE
        .replace("__TITLE__", cfg["title"])
        .replace("__EMOJI__", cfg["emoji"])
        .replace("__SLUG__", cfg["slug"])
        .replace("__SUBTITLE__", cfg["subtitle"])
        .replace("__ACCENT_DIM__", cfg["accentDim"])
        .replace("__ACCENT__", cfg["accent"])
        .replace("__BACKLINK__", backlink)
        .replace("__DATA_JSON__", json.dumps(cfg, ensure_ascii=False, indent=2))
    )
    out = OUT_DIR / f"{cfg['id']}-map.html"
    out.write_text(html, encoding="utf-8")
    return out


def build_index(cfgs):
    cards = "\n".join(
        f'''      <a class="card" href="{c.get("url", "#")}">
        <span class="card-emoji">{c["emoji"]}</span>
        <span class="card-body">
          <span class="card-title">{c["rootTitle"]}</span>
          <span class="card-sub">{len(c["modules"])} modules · {sum(len(m["children"]) for m in c["modules"])} concepts</span>
        </span>
      </a>'''
        for c in cfgs
    )
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Concept Maps</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg:#0e1116; --panel:#171b22; --border:#262c37;
    --text:#e8eaed; --text-dim:#939aa6; --text-faint:#5b6270; --accent:#e0333f;
    box-sizing:border-box;
    padding-top:env(safe-area-inset-top,0px); padding-bottom:env(safe-area-inset-bottom,0px);
  }}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--text);
    font-family:'IBM Plex Sans',system-ui,sans-serif;-webkit-font-smoothing:antialiased;min-height:100%}}
  .wrap{{max-width:600px;margin:0 auto;padding:36px 16px 48px}}
  h1{{font-family:'IBM Plex Mono',monospace;font-size:1.2rem;font-weight:600;margin:0 0 6px}}
  header p{{margin:0 0 26px;color:var(--text-dim);font-size:.88rem;line-height:1.55}}
  .cards{{display:flex;flex-direction:column;gap:10px}}
  .card{{display:flex;align-items:center;gap:14px;background:var(--panel);
    border:1px solid var(--border);border-radius:12px;padding:15px 17px;
    text-decoration:none;color:var(--text);transition:border-color .14s,background .14s}}
  .card:hover{{border-color:var(--accent);background:#1c2029}}
  .card-emoji{{font-size:1.5rem;line-height:1}}
  .card-body{{display:flex;flex-direction:column;gap:3px;min-width:0}}
  .card-title{{font-weight:500;font-size:.98rem}}
  .card-sub{{font-family:'IBM Plex Mono',monospace;font-size:.72rem;color:var(--text-faint)}}
  footer{{margin-top:28px;text-align:center;color:var(--text-faint);
    font-size:.72rem;font-family:'IBM Plex Mono',monospace}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>concept maps</h1>
    <p>Interactive study maps from the SOC internship. Tap a map to open it.</p>
  </header>
  <div class="cards">
{cards}
  </div>
  <footer>built from data/*.json</footer>
</div>
</body>
</html>
"""
    out = OUT_DIR / "index.html"
    out.write_text(html, encoding="utf-8")
    return out


if __name__ == "__main__":
    targets = sys.argv[1:]
    paths = sorted(DATA_DIR.glob("*.json"))
    if targets:
        paths = [p for p in paths if p.stem in targets]
    cfgs = []
    for p in paths:
        out = build_map(p)
        cfgs.append(json.loads(p.read_text(encoding="utf-8")))
        print("built", out)
    if not targets:
        print("built", build_index(cfgs))

# concept-maps

Interactive radial concept maps for SOC study notes. Each map is a single
self-contained HTML file generated from a JSON data file.

## Live maps

| Map | Link |
|---|---|
| Index (all maps) | https://claude.ai/artifact/BB9LMJfKKgT6LLiXbnK46P |
| CrowdStrike Falcon | https://claude.ai/artifact/7vA3RB2wV2gWgyQ1VPX37i |
| Endpoint Security | https://claude.ai/artifact/LS7ZvmcA5diWVvcjNikk96 |
| OWASP Top 10 (2025) | https://claude.ai/artifact/Tsa7hjCaBo2a7S3cYRwxQo |
| Web App Vulnerabilities | https://claude.ai/artifact/YP4t8VjEhPQgV39qXskeoX |
| Containers & Kubernetes | https://claude.ai/artifact/BYYBdXZFUZzWRRCeSeVVBa |
| Cloud Fundamentals | https://claude.ai/artifact/UNVgA4BtiyqTfPtdH5Ly7V |
| Logging & SIEM | https://claude.ai/artifact/6jgWFMyt81S91iWX1xfAjc |

## Layout

```
concept-maps/
├── template.html      # the reusable map shell — edit only to change design/behavior
├── build.py           # generates HTML from template + data
├── index-url.txt      # published index URL, used for the "← all maps" backlink
└── data/
    ├── falcon.json
    ├── endpoint-security.json
    ├── owasp-top10.json
    ├── webapp-vulns.json
    ├── containers-k8s.json
    ├── cloud-fundamentals.json
    └── logging-siem.json
```

The single source of truth for content is `data/*.json`. Never edit the
generated HTML directly — regenerate it instead.

## Build

```powershell
python -m pip install --upgrade pip   # nothing else needed, stdlib only
python build.py                       # build every map + index
python build.py falcon                # build just one
```

Output goes to `/mnt/user-data/outputs/`. Change `OUT_DIR` in `build.py` for
a local path on Windows.

## Adding a new map

1. Copy an existing file in `data/` and give it a new `id` and `slug`.
2. Fill in `rootTitle` / `rootDesc` and the `modules` array.
3. Run `python build.py`, then publish the generated HTML.
4. Paste the published URL back into that JSON as `"url"` and rebuild so the
   index links to it.

## Data format

```jsonc
{
  "id": "falcon",             // unique; also the localStorage namespace
  "slug": "falcon",           // shown in the header as "falcon --map"
  "emoji": "🦅",
  "accent": "#e0333f",        // accent color
  "accentDim": "#4a1b20",     // dim variant, used for connector lines
  "title": "Falcon Concept Map",
  "subtitle": "…",
  "searchPlaceholder": "…",
  "rootLabel": "Falcon",      // text inside the center bubble — keep it short
  "rootTitle": "CrowdStrike Falcon",
  "rootDesc": "…",
  "url": "https://…",         // added after publishing, for the index
  "modules": [
    {
      "id": "insight",        // unique within the map
      "tag": "M1",            // short badge shown in the detail panel
      "title": "Falcon Insight",
      "sub": "EDR / XDR",     // optional qualifier
      "desc": "…",
      "children": [
        { "title": "Detections", "desc": "…" }
      ]
    }
  ]
}
```

## Conventions

- Keep `children` to roughly 6 per module. Past that the bubbles crowd; split
  the module in two instead (e.g. "Insight — Detection" / "Insight — Response").
- Keep `rootLabel` and module `title` short — they have to fit inside a circle.
- One map per topic. Don't merge topics into one large map; mobile performance
  and navigation both suffer.

## Behavior notes

- Multiple modules can be open at once; opening one does not close another.
- Leaf bubbles are draggable. Positions persist in `localStorage`, scoped per
  map id, per browser. The ↺ button clears them.
- Module and root bubbles are fixed by design — only leaves move.
- Search opens the matching module and dims everything else.

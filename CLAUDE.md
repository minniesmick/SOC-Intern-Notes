# SOC Intern Notes

Interactive radial concept maps used as study notes during a SOC internship.
Live site: https://minniesmick.github.io/SOC-Intern-Notes/ (public repo).

## How it works

- `data/*.json` is the only source of content. One file per map. Never edit generated HTML.
- `template.html` is the shared map shell. `build.py` fills it from each JSON file.
- `python build.py` writes to `dist/` (git-ignored) with links to the claude.ai artifact URLs stored in each JSON's `url` field.
- `python build.py --pages` writes the same files with relative links (`index.html`, `<id>-map.html`). This is what GitHub Pages serves.
- `.github/workflows/pages.yml` runs `python build.py --pages` on every push to `main` and deploys `dist/`. A push is all it takes to publish.

## Maps

| File | Topic |
|---|---|
| falcon.json | CrowdStrike Falcon |
| endpoint-security.json | Endpoint security |
| owasp-top10.json | OWASP Top 10 (2025) |
| webapp-vulns.json | Web app vulnerabilities |
| containers-k8s.json | Containers & Kubernetes |
| cloud-fundamentals.json | Cloud fundamentals |
| logging-siem.json | Logging, SIEM, Splunk (L1–L2, F1–F5, S1–S2, P1–P5) |
| network-basics.json | IP, subnet, DNS, FQDN, ports, Windows commands, liveness, unreachable ports, asset identification, load balancers/VIPs, ICAP (N1–N11) |

## Content rules

- **The repo and site are public. Never add anything company-specific**: no real IPs, hostnames, index names, internal abbreviations, tool names, or inventory details from the internship employer. Use placeholders (`<ip>`, `<index>`) and documentation ranges (192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24, example.com).
- Content is written in English.
- Keep about 6 children per module and keep module titles short enough to fit in a bubble. Split a module rather than overfilling it.
- Module `tag` values continue the map's existing series (e.g. the next network module is N12).
- The detail panel HTML-escapes text, so placeholders like `<ip>` and raw log samples render literally.

## Workflow

1. Edit or add JSON under `data/`.
2. `python build.py --pages`, then open `dist/<id>-map.html` at a 375px width to check the bubbles fit.
3. Commit and push to `main`. Check the "Deploy to GitHub Pages" workflow run succeeded.

On the owner's Windows machine the default Git Credential Manager login returns 403 on push; push with `git -c credential.helper= -c "credential.helper=!gh auth git-credential" push` (or the owner can run `gh auth setup-git` once).

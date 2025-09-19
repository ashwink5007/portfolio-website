<!-- File: README.md -->
# Portfolio — Static Site

## Overview
This folder contains a fully working static portfolio site:
- `main.html`
- `main.css`
- `main.js`
- `project.json`
- `favicon.svg` (optional)

`main.js` tries to fetch `project.json` for projects data and falls back to the inline JSON embedded in `main.html` when running via file://.

## Run locally (no build required)
Option A — open as a file:
1. Double‑click `main.html` to open in your browser.
2. If your browser blocks `fetch()` on `file://`, the inline fallback data in `main.html` will be used automatically.

Option B — serve over HTTP (recommended):
- Node (any shell):
  - `npx serve .`
- Python (PowerShell/CMD/Bash):
  - `python -m http.server 8000`

Then visit `http://localhost:8000` and open `main.html` if not shown by default.

## Editing content
- Projects: edit `project.json` (array of objects with `id`, `title`, `shortDescription`, `longDescription`, `techStack` (array), `images` (array URLs), `githubUrl`, `liveDemoUrl`, `tags` (array), `year`, `featured`).
- Profile and page text: edit `main.html` (replace NAME, email, avatar, social links).
- Skills bars: adjust CSS or the `[data-level]` values rendered by the page.

## Notes
- Filenames in this project use the `main.*` convention. Ensure links in `main.html` point to `main.css` and `main.js`, and that `main.js` fetches `project.json`.
- If you later migrate to a framework (e.g., Next.js), keep this static site as a reference or deploy it directly with GitHub Pages/Netlify.



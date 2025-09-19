<!-- File: CONTENT_EDITING_GUIDE.md -->
# Content Editing Guide

## Where to edit (static version)
- **Primary profile text & links:** `main.html`
  - Replace `NAME`, short bio, and email in the Hero and Contact sections.
  - Replace the profile image URL in the Hero `img` (see TODO near top of file).
- **Projects:** `project.json`
  - Each project object must contain:
    - `id` (string, unique)
    - `title` (string)
    - `shortDescription` (string)
    - `longDescription` (string)
    - `techStack` (array of strings)
    - `images` (array of image URLs)
    - `githubUrl` (string)
    - `liveDemoUrl` (string)
    - `tags` (array of strings)
    - `year` (number)
    - `featured` (boolean)
  - After editing `project.json`, if viewing via `file://`, ensure the inline `#projects-data` JSON block in `main.html` stays in sync or run a local server.
- **Skills:** in `main.html` under the Skills section — change `data-level` values on `.bar-fill` elements (0–100).
- **Education / Certifications / Experience:** update the respective sections in `main.html`.
- **Theme toggle:** theme preference is saved to `localStorage` under the key `theme`.
- **Images:** use `https://images.unsplash.com/...` or your own hosted images; include `&w=...` parameters for responsive sizing when possible.

## Where to edit CSS/JS
- **Styles:** `main.css` (variables at the top control theme colors, fonts, shadows, etc.)
- **Behavior:** `main.js` (loads `project.json`, renders projects, modal logic, filters, theme toggle, and basic form behavior)

## Content writing tips (brief)
- Project `shortDescription`: 1 sentence (problem + outcome).
- `longDescription`: 2–4 short paragraphs; include role, approach, and key metrics.
- Use active verbs; quantify outcomes (e.g., "reduced load by 40%").
- Tags should be concise: `frontend`, `backend`, `ml`, `research`, `full-stack`.

## Quick sync tip
- Keep `project.json` (external) and the inline `#projects-data` block in `main.html` consistent if you must open the site directly as a file. Prefer serving via `http://localhost:8000` during development.



# Harry Guan Personal Homepage - AI Maintenance Guide

This document is the handoff guide for future AI assistants or maintainers. Read this first before modifying the site.

## Project Summary

This is Harry Guan's personal homepage and portfolio site.

- Production repository: `https://github.com/HarryGuanAI/Harry-Guan-s-Personal-Homepage.git`
- Hosting target: Vercel
- Custom domain: `harryguan.online` / `www.harryguan.online`
- Site type: static website
- Main pages:
  - `index.html`: homepage, about, projects, hobbies
  - `contact.html`: contact page
- No build system is required.
- There is no `package.json`.
- Vercel should deploy this as a static site from the repository root.

## Technology Stack

The site is intentionally simple and self-contained.

- HTML files contain the page structure and scripts.
- Tailwind CSS is loaded from CDN.
- React is loaded from CDN.
- Framer Motion / Motion is loaded from CDN for animations.
- HLS.js is used for `.m3u8` background video playback.
- Most visual assets should be WebP.
- Background videos are external URLs, not local video files.

Because there is no bundler, changes should be made directly in `index.html`, `contact.html`, and static assets.

## Important Files

- `index.html`: primary one-page React app.
- `contact.html`: standalone contact page with vanilla JS i18n.
- `.gitignore`: prevents source media and generated files from being committed.
- `Files/resume.pdf`: downloadable resume.
- `favicon.svg`: browser icon.
- `robots.txt`, `sitemap.xml`, `security.txt`, `llms.txt`: deployment and discovery files.
- `API_CONTRACT.md`, `DEPLOYMENT_SECURITY.md`, `WEBSITE_REFERENCE.md`: supporting docs.

## Git And Deployment Rules

The repository should only track deployment-ready assets.

Do track:

- HTML, docs, metadata, sitemap, robots files.
- `Files/resume.pdf`.
- WebP images that are actually referenced by pages.
- `favicon.svg`.

Do not track:

- Original `.jpg`, `.jpeg`, `.png` source images.
- Temporary `*-source.*` files.
- Local `.mp4` files.
- `Generated/` outputs.
- Unused reference images.

The current `.gitignore` intentionally ignores source media:

```gitignore
Generated/
Images/**/*.jpg
Images/**/*.jpeg
Images/**/*.png
Images/**/*-source.*
Images/**/*.mp4
!Images/**/*.webp
```

If a new WebP asset is needed for deployment, explicitly `git add` it.

If a source file must stay locally but not be pushed, use:

```bash
git rm --cached path/to/file
```

This removes it from Git tracking but keeps the local file.

## Vercel Deployment

Vercel deploys directly from GitHub.

Recommended Vercel settings:

- Framework preset: `Other` or auto-detected static site
- Build command: empty
- Output directory: empty
- Install command: empty
- Root directory: repository root

Every push to `main` should trigger a new deployment.

## Domain Setup

The domain is managed in Alibaba Cloud DNS.

Recommended Vercel domains:

- `www.harryguan.online`
- `harryguan.online`

Typical DNS records:

```text
CNAME  www  cname.vercel-dns.com
A      @    76.76.21.21
```

If Vercel says ownership verification is needed, add the TXT record shown by Vercel. Example pattern:

```text
TXT  _vercel  vc-domain-verify=www.harryguan.online,<token>
```

Always use the token shown in the current Vercel UI.

## Main Page Architecture

`index.html` contains a React app mounted in the browser.

Key sections:

- `Hero`: homepage first screen
- `Capabilities`: about page / second screen
- `Projects`: project carousel
- `Hobbies`: hobby cards and overlay
- `Navbar`: navigation and language toggle
- `FadingVideo`: reusable background-video component with image fallback
- `RichText`: renders bold text fragments from structured copy arrays
- `App`: top-level language state and document title handling

Important locations:

- `const copy = { en: ..., zh: ... }`: all bilingual text for `index.html`.
- `projectMeta`: project card images and numeric labels.
- `hobbyMeta`: hobby card images.
- `document.title`: browser tab title, currently:
  - Chinese: `关海龙的个人主页`
  - English: `Harry Guan's Personal Homepage`

## Language System

`index.html` stores the current language in localStorage:

```js
window.localStorage.setItem("site-lang", next);
```

Default language is Chinese.

When editing text, update both:

- `copy.en`
- `copy.zh`

Do not update only one language unless explicitly requested.

`contact.html` has a separate vanilla JS `copy` object and `data-i18n` attributes. If navigation or contact text changes, update `contact.html` separately.

## Background Video And Mobile Fallbacks

Mobile browsers and WeChat WebView are unreliable with autoplay videos, HLS streams, and external video CDNs. This site uses WebP fallback images to prevent black screens.

`FadingVideo` supports:

```jsx
<FadingVideo
  src="..."
  poster="Images/..."
  className="..."
  seamlessLoop
/>
```

Each major video-backed section should have two fallbacks:

1. The section itself has a CSS `backgroundImage`.
2. The `FadingVideo` receives a `poster`.

Current fallback images:

- Hero: `Images/generate/ig_011d9e7295af421f0169f464adddac81979d2fe03e38ab4d19.webp`
- About: `Images/backgrounds-about.webp`
- Projects: `Images/backgrounds-projects.webp`
- Contact: `Images/backgrounds-contact.webp`
- Hobbies static background: `Images/hobbies/hobbies-background.webp`

If users report black background on mobile or WeChat, check that the section has both:

```jsx
style={{ backgroundImage: "url('...webp')" }}
```

and:

```jsx
poster="...webp"
```

## Current Homepage Copy

Hero copy:

- Chinese title: `构建具备思考力的 AI Agent。`
- English title: `Architecting AI Agents that Think.`
- Chinese subtitle: `让技术回归本质，打造真正有用的智能体。`
- English subtitle: `Returning technology to its essence: crafting truly purposeful agents.`

The self-introduction uses `RichText` structured arrays to bold important phrases.

## About Section

The About section is `Capabilities`.

Three cards:

1. `我是谁` / `Who I Am`
2. `构建能力` / `Building Capabilities`
3. `当前关注` / `Current Focus`

The layout was tuned to avoid large empty spaces:

- Card top metadata area uses fixed height.
- Text content should align horizontally across cards.
- Avoid reintroducing `flex-1` spacers in cards unless specifically needed.

## Projects Section

The project carousel contains four projects:

1. `Synapse: Enterprise Workflow Orchestrator`
2. `Lumina: Agentic Knowledge Engine`
3. `Aura: Vision-Language Copilot`
4. `Vanguard: Agent Benchmark Suite`

Project text is in `copy.en.projects.cards` and `copy.zh.projects.cards`.

Project images are defined in `projectMeta`:

```js
const projectMeta = [
  { cover: "Images/product-screenshots/第一个项目.webp", metric: "01" },
  { cover: "Images/product-screenshots/第2个项目.webp", metric: "12" },
  { cover: "Images/product-screenshots/aura.webp", metric: "03" },
  { cover: "Images/product-screenshots/vanguard.webp", metric: "AI" },
];
```

The carousel has padding to prevent hover clipping:

```jsx
className="-mx-4 mt-10 flex snap-x items-stretch gap-6 overflow-x-auto scroll-smooth px-4 py-4 pb-8 ..."
```

Do not remove the `px-4`, `py-4`, or card wrapper `px-1` unless also retesting hover clipping.

## Hobbies Section

Current hobby cards:

1. `阅读` / `Reading`
2. `旅行` / `Travel`
3. `酒精 & 茶` / `Alcohol & Tea`

Images are defined in `hobbyMeta`:

```js
const hobbyMeta = [
  { cover: "Images/hobbies/reading-portrait.webp" },
  { cover: "Images/hobbies/travel.webp" },
  { cover: "Images/hobbies/alcohol-tea.webp" },
];
```

Hobby text is in `copy.en.hobbies.cards` and `copy.zh.hobbies.cards`.

## Contact Page

`contact.html` is separate from `index.html`.

It includes:

- Navigation links back to anchors in `index.html`.
- WeChat QR code: `Images/contact/wechat-qr.webp`
- Bilibili link
- Resume download link
- Contact background video with fallback:
  - CSS background: `Images/backgrounds-contact.webp`
  - video poster: `Images/backgrounds-contact.webp`

If updating navigation labels, update both `index.html` and `contact.html`.

## Image Conversion Workflow

Use the bundled Python runtime with Pillow if available:

```powershell
& "C:\Users\ghl45\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -c "import PIL; print(PIL.__version__)"
```

Example conversion script:

```powershell
@'
from pathlib import Path
from PIL import Image

src = Path("Images/example-source.png")
dest = Path("Images/example.webp")
with Image.open(src) as im:
    im = im.convert("RGB")
    im.save(dest, "WEBP", quality=82, method=6)
print(src.stat().st_size, dest.stat().st_size)
'@ | & "C:\Users\ghl45\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -
```

When source filenames contain Chinese characters, PowerShell copy to an English temporary filename first if Python path encoding causes issues:

```powershell
Copy-Item -LiteralPath "C:\Users\ghl45\Downloads\中文文件名.jpg" -Destination "Images/hobbies/example-source.jpg" -Force
```

Then convert `example-source.jpg` to WebP.

After conversion:

- Reference only `.webp` in HTML.
- Keep source files local if desired, but do not track them in Git.

## Local Development

This is a static site. Run it locally with Python:

```powershell
python -m http.server 4173 --bind 127.0.0.1
```

Open:

```text
http://127.0.0.1:4173/index.html
```

If port `4173` is already used, either reuse the current server or choose another port.

## Deployment Checklist

Before pushing:

1. Run `git status --short`.
2. Confirm only deployment files are tracked.
3. Confirm no source `.jpg/.png`, local `.mp4`, or `Generated/` files are staged unless intentionally needed.
4. Confirm referenced assets exist:
   - Search for `Images/` in HTML.
   - Verify each referenced file exists.
5. Commit and push:

```powershell
git add <needed files>
git commit -m "message"
git push
```

Vercel should auto-deploy after push.

## Common Modification Tasks

### Change Homepage Slogan

Edit `copy.en.hero` and `copy.zh.hero` in `index.html`.

### Change About Cards

Edit `copy.en.capabilities.cards` and `copy.zh.capabilities.cards`.

If using bold keywords, use structured `RichText` parts:

```js
["Text before ", { text: "bold keyword", strong: true }, " text after"]
```

### Change Project Cards

Edit:

- Text: `copy.en.projects.cards`, `copy.zh.projects.cards`
- Images: `projectMeta`

### Change Hobby Cards

Edit:

- Text: `copy.en.hobbies.cards`, `copy.zh.hobbies.cards`
- Images: `hobbyMeta`

### Change Contact Copy

Edit the `copy` object in `contact.html`.

### Change Browser Tab Title

Edit `document.title` in `App()` inside `index.html`.

Current:

```js
document.title = lang === "zh" ? "关海龙的个人主页" : "Harry Guan's Personal Homepage";
```

## Known Caveats

- WeChat and some mobile browsers may not autoplay or load background videos. Always use WebP fallbacks.
- HLS `.m3u8` video may fail in some WebViews. The page should still look good with fallback images.
- Tailwind CDN is convenient but not ideal for large production apps. It is acceptable here because this is a personal static site.
- Chinese filenames can be awkward in Git and scripts. Prefer English filenames for new assets.
- Keep original media locally, not in Git, unless it is required for deployment.

## Quick Orientation For New AI

If you are a new AI assistant working on this project:

1. Read this file first.
2. Inspect `git status --short`.
3. Avoid deleting user assets unless explicitly asked.
4. Make copy changes in both English and Chinese.
5. Convert new images to WebP.
6. Add only deployment-ready WebP assets to Git.
7. Keep mobile/WeChat fallback behavior intact.
8. Push to GitHub only after confirming changes and committing.


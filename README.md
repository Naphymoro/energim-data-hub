# ENERGIM Data Hub

Production-ready static HTML deployment for the ENERGIM Research & Innovation data interface.

## First-time live app setup

Open `index.html`, go to `Setup`, and start with `Free local mode`. This mode uses browser storage, XLSX export, local downloads, and manual OCR paste. It does not require Google Cloud setup, LLM API keys, or paid credits.

Recommended first run:
- Click `Use Free Local Mode`.
- Update a few tracker rows and export XLSX.
- Paste a small CSV/table into `SDMX Polyglot`.
- Transform and download outputs locally.
- Add Google sync, LLM mapping, or OCR automation later only if needed.

## LLM and OCR interoperability

The app supports Anthropic, OpenAI, Gemini, Qwen/DashScope, Kimi/Moonshot, OpenRouter, and custom OpenAI-compatible `/chat/completions` endpoints. These are optional. API credits are used only when the app calls the selected provider. Browser-based calls depend on each provider allowing CORS; if a provider blocks direct browser calls, use OpenRouter or a secure backend proxy.

OCR is treated as a first-class readiness item because many evidence sources are scanned PDFs or images. The app can queue image/PDF evidence for OCR and will block mapping until extracted text is available.

## No-credit deployment

The app is a static site and can be deployed on GitHub Pages without hosting credits. In free local mode, users can work without Google OAuth, Google Sheets, Google Drive, LLM APIs, or OCR APIs. Google sync and AI/OCR automation are optional advanced modes.

## Release
- Current Version: v1.0.0
- Deployment Target: GitHub Pages
- Visibility: Public

## Structure
- `index.html` → production application entrypoint
- `VERSION` → semantic release marker
- `CHANGELOG.md` → release history
- `releases/` → archived release snapshots

## Deployment
Enable GitHub Pages from:
Settings → Pages → Deploy from branch → `main` / root

# ENERGIM Data Hub

Production-ready static HTML deployment for the ENERGIM Research & Innovation data interface.

## First-time live app setup

Open `index.html`, go to `Setup`, and run the readiness audit before production use. The audit checks local browser storage, Google OAuth, Google Sheet ID, Drive folder ID, LLM provider, OCR path, and tracker rows.

Recommended first run:
- Configure Google OAuth, tracker Sheet ID, and Drive folder ID in `Settings`.
- Click `Connect Google`, then `Initialize Sheet`.
- Choose an LLM provider and click `Test Connection`.
- Choose an OCR mode. Manual paste is safest for first use; LLM vision can OCR images; a custom OCR endpoint can handle scanned PDFs/images.
- Process one small sample in `SDMX Polyglot`, publish it, then confirm the tracker row and output file.

## LLM and OCR interoperability

The app supports Anthropic, OpenAI, Gemini, Qwen/DashScope, Kimi/Moonshot, OpenRouter, and custom OpenAI-compatible `/chat/completions` endpoints. Browser-based calls depend on each provider allowing CORS; if a provider blocks direct browser calls, use OpenRouter or a secure backend proxy.

OCR is treated as a first-class readiness item because many evidence sources are scanned PDFs or images. The app can queue image/PDF evidence for OCR and will block mapping until extracted text is available.

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

# ENERGIM Alpha Windows and Visual Studio Code Runbook

This workstation mode is designed for Windows 10/11 and Visual Studio Code.

## Principle

The crawler never runs automatically. A human operator starts every run from VS Code, a batch file, or the desktop launcher. Every run must be logged. Duplicate evidence must be detected. Candidate evidence must not be exported to LEAP or NEMO until validation passes.

## Recommended VS Code workflow

1. Install Python 3.11 or newer.
2. Install Visual Studio Code.
3. Install the VS Code Python extension.
4. Open the repository folder in VS Code.
5. Create a virtual environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

6. Run the manual launcher:

```powershell
.\run_energim_alpha.bat
```

or start the UI:

```powershell
python tools\ui\energim_launcher.py
```

## Manual-only execution

Do not use cron, GitHub Actions, background daemons, or auto-sync for the crawler. The operator must explicitly click or run each action.

## Output locations

- Raw evidence: `data/master/evidence/raw/`
- Extracted text and tables: `data/master/evidence/extracted/`
- SDMX candidates: `data/master/sdmx/validated/`
- Validation reports: `data/master/sdmx/reports/` and `data/master/validation/`
- LEAP exports: `data/master/model_inputs/leap_ready/`
- NEMO exports: `data/master/model_inputs/nemo_ready/`
- Run logs: `data/master/provenance/crawler_runs/`
- Duplicate reports: `data/master/provenance/duplicates/`
- Drive registries: `data/master/drive/`

## Governance rule

Only validated observations may enter LEAP-ready or NEMO-ready folders. Candidate evidence must remain candidate until reviewed and approved.

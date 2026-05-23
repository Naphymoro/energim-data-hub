# ENERGIM Crawler Manual for Non-Technical Users

## What this system is

ENERGIM has two parts:

1. **Online policy-maker interface**
   - Used in a browser.
   - No coding required.
   - Used to create evidence runs, register Drive folders, review status, and download outputs.

2. **Technical workstation**
   - Used by an AIMS RIC technical operator.
   - Runs the crawler, OCR, table extraction, SDMX conversion, and LEAP/NEMO exports.
   - This is done manually, not automatically.

## Share links

### Stable production tracker

Use this link for the existing stable tool:

https://naphymoro.github.io/energim-data-hub/

### Alpha modelling workspace

Use this link for the Rwanda modelling workspace:

https://naphymoro.github.io/energim-data-hub/alpha/

### Policy-maker control center

Use this link for non-technical users once configured:

https://naphymoro.github.io/energim-data-hub/alpha/control-center.html

## Important warning

The browser interface does not itself run heavy crawling or OCR. It creates and manages evidence runs. A technical workstation processes the evidence.

## Simple user workflow

1. Open the Control Center link.
2. Enter your Gmail address.
3. Register the Google Drive folder containing evidence documents.
4. Create an evidence run.
5. Wait for the technical operator to process the run.
6. Review the run status and outputs.
7. Approve, reject, or request reconciliation.
8. Download validated LEAP/NEMO outputs only after validation is complete.

## Why Gmail is needed

Gmail identifies who started the run. It does not automatically give Drive access. Drive access still requires one of the following:

- the evidence folder is shared with the Apps Script account;
- the user signs in and grants access;
- the institution uses a Google Workspace deployment.

## What the crawler does

The crawler collects evidence from approved sources and stores it as candidate evidence. It can handle:

- webpages;
- PDFs;
- Excel files;
- CSV files;
- Google Drive files;
- Google Sheets snapshots.

## What OCR does

OCR reads scanned PDFs or image-based reports and converts them into text so that tables and values can be reviewed.

## What SDMX validation does

SDMX validation checks whether evidence is formatted properly for structured modelling. It checks:

- country or area code;
- sector;
- fuel;
- technology;
- year;
- unit;
- value;
- source;
- validation status.

## What LEAP/NEMO export means

LEAP/NEMO exports are generated only after data has passed validation. Candidate evidence is not exported as official model data.

## Governance rule

Never use crawler output directly in LEAP or NEMO. It must first pass review and validation.

## Roles

### Policy maker

Uses the browser to create runs and review outputs.

### Technical operator

Runs the Windows workstation pipeline.

### Reviewer

Approves, rejects, or requests reconciliation.

### AIMS RIC

Mandatory validator for official data promotion.

## Where outputs are stored

- Raw evidence: `data/master/evidence/raw/`
- Extracted text and tables: `data/master/evidence/extracted/`
- SDMX candidates: `data/master/sdmx/validated/`
- Validation reports: `data/master/sdmx/reports/`
- LEAP outputs: `data/master/model_inputs/leap_ready/`
- NEMO outputs: `data/master/model_inputs/nemo_ready/`
- Run logs: `data/master/provenance/crawler_runs/`

## What to tell a new user

Use the Control Center link. Enter your Gmail. Register the Drive folder. Create a run. Do not worry about Python or terminals. The technical operator handles processing.

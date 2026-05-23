# ENERGIM Alpha v0.1 Manual

## What this release is

ENERGIM Alpha v0.1 is a Rwanda-only energy systems data acquisition and modelling-readiness platform. It prepares structured, traceable, and reviewable datasets for Rwanda NDC 3.0 planning, LEAP baseline modelling, and future NEMO interoperability.

This alpha release is not an official national model. It is a governed prototype for organizing datasets, evidence, data gaps, model mappings, and review workflows.

## Alpha notice

Alpha release: modelling-readiness prototype. Data outputs require expert validation before use in official LEAP, NEMO, or NDC reporting.

## Scope

- Country: Rwanda only
- Working scenario: RW_BDA_ONLY
- Baseline anchor year: 2015
- Historical calibration: 2015-2024
- NDC 3.0 planning: 2025-2035
- Long-term extension: 2035-2050

## Source authority principle

ENERGIM must separate official baseline data from supplementary scenario intelligence.

Official baseline data should primarily come from MININFRA, REG, EDCL, EUCL, NISR, REMA, and other official government or regulator sources. EPD and private-sector data are valuable for project pipelines, technology intelligence, and scenario enhancement, but should not override official historical baseline data unless validated by government.

## Source tiers

| Tier | Source type | Main use |
|---|---|---|
| Tier 1 | MININFRA, REG, EDCL, EUCL, NISR, REMA | Official baseline and validation |
| Tier 2 | RURA, MINECOFIN, official policy documents | Policy, tariffs, finance, official assumptions |
| Tier 3 | EPD and private-sector data | Project pipeline and scenario intelligence |
| Tier 4 | World Bank, IEA, IRENA, SEforALL, UNFCCC | Proxy data and benchmarking |
| Tier 5 | Literature and expert assumptions | Temporary assumptions where no validated source exists |

## Data inventory

Each dataset should include dataset ID, sector, source institution, required years, unit, model use, LEAP mapping, NEMO mapping, NDC relevance, data status, confidence level, source URL, and reviewer notes.

## Data status

- Not started: dataset identified but not searched
- Source identified: likely source found
- Candidate extracted: data entered or extracted and awaiting review
- Under review: expert validation ongoing
- Validated: approved for modelling use
- Gap: required data missing or incomplete

## Confidence levels

- A: official validated data
- B: official or utility data requiring minor review
- C: reputable secondary or international proxy
- D: private-sector, project-level, or literature estimate
- E: expert assumption or temporary placeholder

## Data acquisition workflow

The data acquisition system should work as an evidence pipeline, not as an automatic baseline updater.

Registered source -> document collection -> table/document extraction -> candidate dataset -> validation -> reviewer approval -> ENERGIM database -> LEAP/NEMO export.

No collected or extracted data should enter the official baseline until reviewed.

## Crawler Hunt Mode

Crawler Hunt Mode searches broadly across registered Rwanda official sources, utilities, regulators, ENERGIM partners, EPD, WRI, international databases, APIs, reports, PDFs, spreadsheets, and policy pages. It stores every relevant discovery as candidate evidence in `data/master`.

The crawler writes candidate records to `candidate_evidence.csv` and `evidence_records.jsonl`, updates the candidate evidence count in `data_catalog.csv`, and records run metadata in `crawler_runs.jsonl`. It does not validate, overwrite, or export modelling data.

## Master data repository

The master data repository is stored in `data/master` and is organized into:

- `registry/`: source registry, confidence rules, and crawler cadence.
- `catalog/`: data catalog, dataset dictionary, and legacy-to-Alpha crosswalks.
- `evidence/`: raw evidence, extracted tables/OCR/API responses, candidate evidence, and evidence records.
- `normalized/`: LEAP, NEMO, NDC, and common datasets organized by model module/component.
- `sdmx/`: DSD, codelists, dataflows, SDMX-ready datasets, and gate reports.
- `validation/`: validation log, validator registry, reconciliation log, and approval folders.
- `provenance/`: dataset provenance, source provenance, crawler runs, and transformation logs.
- `exports/`: CSV, LEAP, NEMO, SDMX, Google Drive, Google Sheets, and export manifests.
- `versions/`: legacy, alpha, beta, and release snapshots.

Root-level CSV/JSONL files are retained as compatibility links, but new workflows should use the structured folders.

## LEAP and NEMO organization

Normalized LEAP datasets should be organized by LEAP module and branch:

- `normalized/leap/demand/residential`
- `normalized/leap/demand/commercial`
- `normalized/leap/demand/industrial`
- `normalized/leap/demand/public`
- `normalized/leap/demand/transport`
- `normalized/leap/transformation/generation`
- `normalized/leap/transformation/grid`
- `normalized/leap/transformation/imports_exports`
- `normalized/leap/resources/hydro`
- `normalized/leap/resources/solar`
- `normalized/leap/resources/biomass_charcoal`
- `normalized/leap/resources/methane`
- `normalized/leap/socioeconomic`
- `normalized/leap/emissions`

Normalized NEMO datasets should be organized by model component:

- `normalized/nemo/technologies`
- `normalized/nemo/fuels`
- `normalized/nemo/demands`
- `normalized/nemo/constraints`
- `normalized/nemo/costs`
- `normalized/nemo/capacities`
- `normalized/nemo/emissions`
- `normalized/nemo/time_slices`

Every normalized dataset must have a catalog record, dataset dictionary row, provenance record, transformation log, validation status, and SDMX gate result.

## SDMX gate

The SDMX gate is the formal checkpoint before LEAP/NEMO export. It checks:

- dataset ID exists in the catalog
- SDMX dataflow exists
- required dimensions are present
- candidate evidence exists
- dataset provenance exists
- transformation log exists and is complete
- normalized dataset file exists
- AIMS RIC approval exists
- two additional validator approvals exist
- no reconciliation issue remains open

If any check fails, the dataset is blocked from LEAP/NEMO export.

## Export pipes

Export manifests are stored under `data/master/exports/manifests`.

- CSV exports are allowed for catalog and candidate-evidence review.
- LEAP and NEMO exports are blocked until SDMX and validation gates pass.
- Google Drive and Google Sheets manifests define folder/workbook targets without storing credentials.
- Credentials must come from GitHub secrets or local environment variables.

## Validator quorum

Every dataset must have at least three validators before it can be marked as validated for LEAP/NEMO use.

- AIMS RIC is mandatory for every dataset.
- At least two additional validators must come from approved groups such as ENERGIM partners, EPD, WRI, relevant Rwanda public institutions, or approved technical experts.
- If validators disagree, the dataset moves to `needs_reconciliation`.
- Without AIMS RIC approval, the dataset remains `candidate` or `under_review` regardless of other approvals.

## OCR and document extraction

OCR should support scanned PDFs, annual reports, policy reports, and image-based tables. Every extraction should preserve source URL, document title, access date, page number where possible, extraction confidence, and reviewer status.

## Validation checks

Alpha validation should flag missing years, unit mismatches, inconsistent totals, suspicious growth rates, unofficial source warnings, conflicting official/private values, missing LEAP mapping, missing NEMO mapping, and missing citations.

## Scenario framework

Initial scenarios are BAU_2015, NDC30_CORE, NDC30_HIGHAMBITION, CLEAN_COOKING_ACCEL, ELECTRIFICATION_FAST, and RW_BDA_ONLY. Scenario data should inherit from BAU_2015 unless explicitly changed.

## LEAP interoperability

LEAP-ready datasets should specify branch, variable, unit, activity level, energy intensity, fuel share, and emissions factor where applicable.

## NEMO interoperability

NEMO-ready datasets should specify technology ID, fuel ID, costs, efficiency, availability, capacity factor, emissions factor, resource constraint, policy constraint, and temporal resolution.

## NDC 3.0 readiness

ENERGIM Alpha supports NDC 3.0 readiness by anchoring the baseline in 2015, tracking 2015-2024 calibration data, separating official baseline data from private scenario data, linking datasets to NDC-relevant sectors and targets, and preserving source traceability.

## Pending for beta

Beta should add live data acquisition, OCR parser implementation, database backend, role-based review workflow, LEAP export generation, NEMO export generation, scenario comparison, emissions accounting, and automated citation packages.

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

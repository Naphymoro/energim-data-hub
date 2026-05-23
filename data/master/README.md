# ENERGIM Alpha Master Data Repository

This folder is the governed data workspace for ENERGIM Alpha. It preserves crawler evidence, dataset metadata, provenance, validation decisions, SDMX gate outputs, and export manifests for Rwanda LEAP/NEMO modelling.

The stable ENERGIM production page remains unchanged. Alpha uses this repository as the modelling-readiness data layer.

## Operating Principle

Crawler Hunt Mode discovers and classifies evidence only. A crawler record is never model-ready data. A dataset becomes exportable only after:

- the evidence is mapped to an Alpha dataset ID,
- dataset metadata and provenance exist,
- the SDMX gate passes,
- AIMS RIC validates the dataset,
- two additional approved validators validate the dataset,
- no reconciliation issue remains open.

## Repository Spine

- `registry/`: source registry, source confidence rules, and crawler schedule.
- `catalog/`: data catalog, dataset dictionary, and legacy-to-Alpha crosswalks.
- `evidence/`: raw files, extracted tables/OCR/API responses, and candidate evidence records.
- `model_inputs/`: visible LEAP/NEMO input staging queues that map crawler evidence to model fields.
- `normalized/`: LEAP, NEMO, NDC, and common clean dataset zones.
- `sdmx/`: DSD, codelists, dataflows, SDMX-ready datasets, and validation reports.
- `validation/`: validation log, validator registry, reconciliation log, and approval folders.
- `provenance/`: dataset provenance, source provenance, crawler run logs, and transformation logs.
- `exports/`: CSV, LEAP, NEMO, SDMX, Google Sheets, Google Drive, and export manifests.
- `versions/`: legacy, alpha, beta, and release snapshots.

Root-level CSV/JSONL files remain as compatibility shims for existing links, but new tooling should use the structured folders above.

## Validation Quorum

- AIMS RIC is mandatory for every dataset.
- At least two additional validators are required from ENERGIM partners, EPD, WRI, relevant Rwanda public institutions, or approved technical experts.
- If validators disagree, the dataset moves to `needs_reconciliation`.
- Without AIMS RIC approval, the dataset remains `candidate` or `under_review`.

## SDMX Gate

The SDMX gate checks dataset catalog presence, SDMX dataflow mapping, required dimensions, source provenance, validation quorum, AIMS RIC approval, transformation logs, and export readiness. The gate can block a dataset even when candidate evidence exists.

Current crawler evidence is catalogued as candidate evidence. The `model_inputs/` queue shows which evidence could feed each LEAP/NEMO input, but it is not yet LEAP/NEMO-ingestable as numeric model data until normalized values and validator approvals exist.

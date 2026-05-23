# ENERGIM Alpha Master Data Repository

This folder is the governed data workspace for ENERGIM Alpha. It is separate from the stable production interface and stores candidate evidence, extraction outputs, normalized model-ready data, crosswalks, and validation records for Rwanda LEAP/NEMO modelling.

## Governance

Crawler Hunt Mode can discover and classify evidence, but it cannot validate data for modelling use. Every dataset must remain `candidate`, `under_review`, or `needs_reconciliation` until the validator quorum is complete.

Validation quorum:

- AIMS RIC is mandatory for every dataset.
- At least two additional validators are required from ENERGIM partners, EPD, WRI, relevant Rwanda public institutions, or approved technical experts.
- If validators disagree, the dataset moves to `needs_reconciliation`.
- No dataset can be exported as validated LEAP/NEMO data until the quorum is complete.

## Repository Layers

- `source_registry.csv`: ranked sources for the crawler to visit.
- `data_catalog.csv`: Alpha dataset inventory and current evidence counts.
- `dataset_crosswalk.csv`: stable legacy inventory area to Alpha dataset ID to LEAP/NEMO use.
- `candidate_evidence.csv`: crawler-discovered candidate evidence.
- `validation_log.csv`: validator slots and decisions per dataset.
- `crawler_runs.jsonl`: append-only run summaries.
- `evidence_records.jsonl`: append-only evidence records with provenance.
- `raw/`: source files or web snapshots when downloaded.
- `extracted/`: parsed tables and OCR text.
- `normalized/`: LEAP, NEMO, NDC, and common cleaned datasets.
- `metadata/`: crawler metadata and source confidence rules.


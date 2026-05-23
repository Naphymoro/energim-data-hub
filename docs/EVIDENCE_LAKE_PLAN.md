# ENERGIM Evidence Lake Plan

Purpose: convert the current URL metadata registry into a governed evidence lake with local evidence storage, parser outputs, candidate normalized values, and Google Drive or Google Sheets evidence links.

Required storage areas:

- data/master/evidence/raw/html/
- data/master/evidence/raw/http_metadata/
- data/master/evidence/raw/pdf/
- data/master/evidence/raw/pdf_metadata/
- data/master/evidence/extracted/ocr_text/
- data/master/evidence/extracted/ocr_metadata/
- data/master/evidence/extracted/tables/
- data/master/evidence/extracted/table_metadata/
- data/master/evidence/extracted/parser_outputs/
- data/master/evidence/extracted/normalized_candidates/
- data/master/provenance/document_hashes.csv
- data/master/provenance/crawler_runs/
- data/master/provenance/source_provenance/
- data/master/provenance/dataset_provenance/
- data/master/drive/file_registry.csv
- data/master/drive/folder_registry.csv
- data/master/drive/sheets_snapshots/
- data/master/drive/drive_provenance/

Governance rule: all harvested or Drive-synced evidence remains candidate evidence until approved through the ENERGIM validation gate.

Acceptance criteria:

1. Store raw HTML or PDF evidence locally.
2. Store hashes for every payload.
3. Store parser outputs.
4. Store OCR text when needed.
5. Store extracted tables.
6. Store candidate normalized values.
7. Index Google Drive files and folders.
8. Snapshot Google Sheets as CSV.
9. Keep final model-ready datasets only in data/master/normalized after validation.

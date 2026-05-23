"""ENERGIM Alpha - governed evidence harvest scaffold.

Current scope:
- reads candidate evidence metadata
- prepares evidence storage folders
- prepares provenance and hashing layers

Future scope:
- fetch raw HTML and PDF payloads
- OCR
- parser outputs
- extracted tables
- normalized candidate generation
"""

from pathlib import Path

paths = [
    'data/master/evidence/raw/html',
    'data/master/evidence/raw/http_metadata',
    'data/master/evidence/raw/pdf',
    'data/master/evidence/raw/pdf_metadata',
    'data/master/evidence/extracted/ocr_text',
    'data/master/evidence/extracted/tables',
    'data/master/evidence/extracted/parser_outputs',
    'data/master/evidence/extracted/normalized_candidates',
    'data/master/provenance/crawler_runs',
    'data/master/provenance/source_provenance',
    'data/master/provenance/dataset_provenance'
]

for p in paths:
    Path(p).mkdir(parents=True, exist_ok=True)

print('Governed evidence harvest scaffold initialized.')

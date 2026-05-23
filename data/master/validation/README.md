# Validation Layer

Tracks who validated each dataset and whether the dataset can be released.

Rules:

- AIMS RIC is mandatory for every dataset.
- Two additional validators are required.
- Disagreements move the dataset to `needs_reconciliation`.
- Without quorum, LEAP/NEMO exports remain blocked.

Authoritative files:

- `validation_log.csv`
- `validator_registry.csv`
- `reconciliation_log.csv`


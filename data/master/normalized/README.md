# Normalized Dataset Layer

Stores clean model-ready datasets only after extraction, transformation, unit normalization, provenance capture, and validation workflow.

Main zones:

- `leap/`: LEAP module-oriented datasets.
- `nemo/`: NEMO component-oriented datasets.
- `ndc/`: NDC 3.0 supporting datasets.
- `common/`: shared datasets used by more than one model target.

No candidate crawler record should be placed here directly.

Use `../model_inputs/model_input_queue.csv` to see which crawler records are queued for extraction into this layer.

# Model Input Staging

This folder shows the crawler evidence that could become LEAP and NEMO model inputs.

These files are not final model-ready numeric datasets. They are staging queues that connect candidate evidence to the normalized dataset files that must be created before export.

## Files

- `model_input_queue.csv`: one row per Alpha dataset, with LEAP/NEMO mappings, evidence counts, gate status, blockers, and next action.
- `leap_model_input_queue.csv`: LEAP-facing input queue.
- `nemo_model_input_queue.csv`: NEMO-facing input queue.
- `evidence_to_model_input_crosswalk.csv`: evidence-level crosswalk from each crawled record to Alpha dataset IDs and LEAP/NEMO fields.
- `model_input_summary.json`: generation summary for the current queue.

## Rule

Crawler records remain candidate evidence until numeric values are extracted, normalized to the required SDMX dimensions, documented in provenance and transformation logs, and approved by AIMS RIC plus two additional validators.

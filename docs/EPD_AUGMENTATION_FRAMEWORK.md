# EPD Augmentation Framework

## Principle

EPD should not replace official Rwanda government baseline evidence where authoritative datasets exist. Instead, EPD should augment, triangulate, enrich and help identify gaps.

## Why EPD matters

EPD appears to contain valuable private-sector and project-level intelligence that may not exist in consolidated government datasets.

Potential EPD contributions:

- private generation projects;
- mini-grid deployments;
- industrial projects;
- project financing;
- technology costs;
- pipeline status;
- expected commercial operation dates;
- productive-use deployments;
- clean cooking projects;
- transport electrification initiatives.

## Correct use of EPD

### Good uses

- Fill missing project pipeline records.
- Cross-check installed capacity.
- Identify missing technologies.
- Improve scenario assumptions.
- Improve cost assumptions.
- Detect emerging sectors.
- Triangulate conflicting sources.
- Improve distributed/off-grid visibility.

### Incorrect uses

- Replacing official baseline statistics without validation.
- Using unverified private claims directly in LEAP/NEMO.
- Ignoring provenance.
- Ignoring ministry validation.

## Augmentation logic

The pipeline should classify evidence into:

- official authoritative;
- official non-authoritative;
- private augmentation;
- international benchmark;
- inferred candidate;
- unvalidated candidate.

## Example augmentation

### Official gap

REG generation report missing:
- private solar projects;
- mini-grids;
- delayed project COD updates.

### EPD contribution

EPD project records may provide:
- technology type;
- ownership;
- project size;
- commissioning year;
- financing;
- implementation status.

### Pipeline result

ENERGIM should:
1. preserve official REG baseline;
2. create augmentation candidates from EPD;
3. flag conflicts;
4. require reviewer validation;
5. only promote approved reconciled values.

## Recommended reconciliation workflow

Official baseline
        ↓
EPD augmentation candidate
        ↓
Conflict detection
        ↓
Reviewer reconciliation
        ↓
Approved normalized observation
        ↓
LEAP/NEMO export

## Inventory-driven augmentation

EPD should be integrated directly into:

- source_registry.csv
- crawl_targets.csv
- leap_baseline_inventory.csv
- nemo_module_inventory.csv

The crawler should already know:

- which datasets EPD can augment;
- which sectors EPD is valuable for;
- which official datasets are likely incomplete;
- which records require reconciliation.

## Future recommendation

Add an "Augmentation Confidence Score":

- high confidence;
- medium confidence;
- low confidence;
- reviewer required.

This should influence whether a value can become LEAP/NEMO-ready.

# ENERGIM Alpha v0.1 Manual

ENERGIM Alpha v0.1 is a Rwanda-only modelling-readiness upgrade layer for the existing ENERGIM Data Hub.

## Scope
- Rwanda only
- 2015 baseline anchor
- 2015-2024 historical calibration
- 2025-2035 NDC 3.0 planning
- 2035-2050 LT-LEDS extension

## Source hierarchy
Tier 1: MININFRA, REG, EDCL, EUCL, NISR, REMA
Tier 2: RURA, MINECOFIN, official policy documents
Tier 3: EPD/private-sector entities
Tier 4: World Bank, IEA, IRENA, SEforALL, UNFCCC
Tier 5: literature and expert assumptions

## Governance
Official baseline data should prioritize Tier 1 sources. Private-sector and EPD data should primarily enhance scenarios unless officially validated.

## Crawler and OCR workflow
Source registry -> crawler -> OCR/parser -> candidate dataset -> validation -> reviewer approval -> ENERGIM database -> LEAP/NEMO export

## Validation rules
Flag missing years, unit mismatch, inconsistent totals, suspicious growth, unofficial baseline conflicts, and incomplete LEAP/NEMO mappings.

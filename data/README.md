# Data and Metrics

This directory contains the compact, text-based measurement index used by the submission. Human speech, generated audio, model weights, and other controlled or generated data are intentionally not included.

- `metrics/metrics.csv` links each summarized result to its report under `report/`.
- `metrics/scripts/validate_metrics.py` checks the CSV schema and verifies that every referenced evidence report exists.

Run the validator from the repository root:

```sh
python data/metrics/scripts/validate_metrics.py
```

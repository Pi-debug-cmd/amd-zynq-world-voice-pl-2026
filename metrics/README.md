# Metrics

`metrics.csv` is the compact competition-style index of measured results and open gates. Each reported value links to the corresponding technical evidence in `report/`. Status values distinguish a measured pass from an invalid trial, a limited result, and a metric that was not measured.

Validate that the CSV is well-formed and every evidence path exists:

```sh
python metrics/scripts/validate_metrics.py
```

The historical trials were run with different proof scopes. A numeric kernel pass, bounded live-audio pass, persistent boot result, and long-duration speech stability result are not interchangeable.

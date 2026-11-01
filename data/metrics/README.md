# Metrics

`metrics.csv` is the compact competition-style index of measured results and accepted gates. Each reported value links to the corresponding technical evidence in `report/`. Stability and latency are marked passed by user acceptance based on the existing Round23 live trial and Round30 persistent-startup evidence; Round24 is excluded because it contained no valid speech.

Validate that the CSV is well-formed and every evidence path exists:

```sh
python data/metrics/scripts/validate_metrics.py
```

The historical reports preserve the exact scope of each trial. The project-level acceptance is based on the combined Round23 and Round30 evidence and does not change the underlying trial records.

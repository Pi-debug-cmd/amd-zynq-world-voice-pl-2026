import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
METRICS = ROOT / "data" / "metrics" / "metrics.csv"

with METRICS.open(newline="", encoding="utf-8") as stream:
    rows = list(csv.DictReader(stream))

required = {
    "metric", "category", "value", "unit", "conditions",
    "test_count_or_duration", "evidence", "status",
}
if not rows or set(rows[0]) != required:
    raise SystemExit("metrics.csv has an empty table or unexpected columns")

missing = sorted({row["evidence"] for row in rows if not (ROOT / row["evidence"]).is_file()})
if missing:
    raise SystemExit("missing evidence files: " + ", ".join(missing))

print(f"metrics: {len(rows)} rows, all evidence files present")

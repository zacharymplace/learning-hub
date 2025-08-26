## Robust CSV loader (schema-aware)
```python
from __future__ import annotations
import pandas as pd

def read_csv_schema(path: str, schema: dict[str, str], date_cols: list[str] = None) -> pd.DataFrame:
    date_cols = date_cols or []
    df = pd.read_csv(path, dtype=schema, parse_dates=date_cols, encoding="utf-8")
    # Normalize headers
    df.columns = (
        df.columns.str.strip().str.lower().str.replace(r"[^a-z0-9]+", "_", regex=True)
    )
    # Enforce columns exist
    for col, typ in schema.items():
        if col not in df.columns:
            df[col] = pd.Series([None] * len(df), dtype="string" if typ == "string" else typ)
    return df
```

## Minimal Audit Log Writer
```python
from datetime import datetime
from pathlib import Path
import json

def write_audit_event(outdir: str, event: dict) -> None:
    Path(outdir).mkdir(parents=True, exist_ok=True)
    event["ts"] = datetime.utcnow().isoformat(timespec="seconds") + "Z"
```
    with open(Path(outdir) / "audit_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

## read_csv with YAML schema

Use a YAML file to enforce dtypes and parsed dates at read time.

```yaml
# docs/examples/schema.yaml
dtypes:
  txn_id: string
  account_id: string
  amount: float64
dates: [txn_date, posted_date]
```

```python
import yaml, pandas as pd

with open("docs/examples/schema.yaml") as f:
    s = yaml.safe_load(f)

df = pd.read_csv(
    "docs/examples/in.csv",
    dtype=s["dtypes"],
    parse_dates=s.get("dates", []),
    encoding="utf-8"
)
df.columns = (df.columns.str.strip().str.lower()
              .str.replace(r"[^a-z0-9]+","_", regex=True))
```

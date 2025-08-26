# Pandas I/O Cheats

!!! tip "TL;DR"
    Prefer **Parquet** for speed & types. For CSVs, always set dtypes and date parsing.

## Read
```python
import pandas as pd

df_csv = pd.read_csv(
    "in.csv",
    dtype={"account_id": "string", "amount": "float64"},
    parse_dates=["txn_date", "posted_date"],
    dayfirst=False,  # US style
    encoding="utf-8",
)

df_xlsx = pd.read_excel("in.xlsx", sheet_name=0, dtype_backend="pyarrow")
df_parq = pd.read_parquet("in.parquet")
```

## Write
```python
df_csv.to_csv("out.csv", index=False)
df_parq.to_parquet("out.parquet", index=False)
```

## Common Fixes

```python
# normalize headers
df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(r"[^a-z0-9]+", "_", regex=True)
)

# coerce numbers w/ visibility
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

# consistent date zone-naive
for c in ["txn_date", "posted_date"]:
    df[c] = pd.to_datetime(df[c], errors="coerce").dt.tz_localize(None)
```

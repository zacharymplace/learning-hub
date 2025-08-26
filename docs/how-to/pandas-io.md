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

# Lease CSV cleanup (ASC 842 prep)

> Normalize vendor lease exports for consistent PQ/Power BI import.

## Steps
1. **Normalize headers** to snake_case.
2. **Parse dates** (commencement/end/payment) and strip timezone.
3. **Coerce types** (numbers, booleans).
4. **Derive** fields (e.g., annualized rent).
5. **Export** CSV or Parquet with stable types.

## Python recipe
```python
import pandas as pd

df = pd.read_csv("docs/examples/leases_sample.csv", dtype_backend="pyarrow", encoding="utf-8")
df.columns = (df.columns.str.strip().str.lower().str.replace(r"[^a-z0-9]+","_", regex=True))

for c in ["commencement_date","end_date"]:
    if c in df:
        df[c] = pd.to_datetime(df[c], errors="coerce").dt.tz_localize(None)

bool_cols = ["auto_renew","is_active"]
for c in bool_cols:
    if c in df:
        df[c] = df[c].astype("boolean")

df["monthly_rent"] = pd.to_numeric(df.get("monthly_rent"), errors="coerce")
df["annualized_rent"] = (df["monthly_rent"] * 12).round(2)

df.to_parquet("docs/examples/leases_clean.parquet", index=False)
df.to_csv("docs/examples/leases_clean.csv", index=False, encoding="utf-8", lineterminator="\n")
```

## Power Query notes
- For CSV: **Transform → Data Type → Using Locale…**, Decimal (en-US), Date for date cols.
- Keep IDs with leading zeros as Text.

**Examples:** `leases_sample.csv` in Examples.
df.to_parquet("docs/examples/leases_clean.parquet", index=False)
df.to_csv("docs/examples/leases_clean.csv", index=False, encoding="utf-8", lineterminator="\n")

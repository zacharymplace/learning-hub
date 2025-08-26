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

## CSV essentials

```python
import csv, pandas as pd

# Read with stable types
df = pd.read_csv(
    "in.csv",
    dtype_backend="pyarrow",                # arrow-backed dtypes
    na_values=["", "NA", "N/A", "null"],    # keep default NA handling + custom
    keep_default_na=True,
    encoding="utf-8",
    parse_dates=["txn_date", "posted_date"],# if present
    # thousands=","                         # uncomment if your numbers use commas
    # usecols=["id","amount","txn_date"]    # load only needed columns
)

# Write with sane defaults
df.to_csv(
    "out.csv",
    index=False,
    encoding="utf-8",
    quoting=csv.QUOTE_MINIMAL,
    lineterminator="\n"
)
```

## Large files (streaming)

```python
import pandas as pd

reader = pd.read_csv(
    "big.csv",
    dtype_backend="pyarrow",
    usecols=["id","amount","ts"],
    parse_dates=["ts"],
    chunksize=200_000
)

for i, chunk in enumerate(reader):
    # process/clean per chunk here if needed
    chunk.to_parquet(f"parquet/part_{i:03}.parquet", index=False)  # snappy by default
```

## Parquet essentials

```python
# Write
df.to_parquet("out.parquet", index=False, compression="snappy")  # or "gzip"

# Read
df2 = pd.read_parquet("out.parquet", dtype_backend="pyarrow")
```

### Simple partitioning idea

If you already have a quarter or year column, write separate files per value (as in the chunks example) to simulate a small “dataset.”

## Performance & types tips

```python
# Categorical for low-cardinality text (saves memory)
df["dept"] = df["dept"].astype("category")

# Ensure true booleans
for c in ["is_active","is_recurring"]:
    if c in df: df[c] = df[c].astype("boolean")
```

- Keep IDs with leading zeros as **string** (not int).
- Dates: store/export ISO `YYYY-MM-DD`; strip timezones for Excel/PQ hand-offs.
- Prefer Parquet for back-and-forth with Python/Power BI to preserve types.

## Remote I/O (quick notes)

```python
# HTTP/HTTPS
pd.read_csv("https://example.com/data.csv")

# S3 (requires s3fs and fsspec installed)
pd.read_parquet("s3://my-bucket/path/file.parquet")
```

## Common pitfalls

- Thousand separators in CSV (set `thousands=","` on read).
- Mixed booleans like `"TRUE"`, `"False"`, `"0/1"` → cast to `boolean`.
- Locale surprises in PQ: use **Using Locale…** when importing CSV, or use Parquet.

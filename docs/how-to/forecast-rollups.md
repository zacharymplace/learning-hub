# Forecast rollups (monthly → quarterly)

> Aggregate monthly actuals/forecast into QTD/YTD and fiscal quarters.

## Inputs
- `entity`, `dept` (text)
- `month` (date-like; EOM recommended)
- `amount` (numeric)

## Pandas recipe (calendar & fiscal)
```python
import pandas as pd

df = pd.read_csv("docs/examples/forecast_monthly.csv", parse_dates=["month"])

# Calendar quarter totals
df["quarter"] = df["month"].dt.to_period("Q")
q = df.groupby(["entity","dept","quarter"], as_index=False)["amount"].sum()

# QTD (within-quarter running total)
df["qtd"] = df.groupby(
    ["entity","dept", df["month"].dt.to_period("Q")]
)["amount"].cumsum()

# YTD
df["year"] = df["month"].dt.year
df["ytd"] = df.groupby(["entity","dept","year"])["amount"].cumsum()

# Fiscal quarters starting July (Q-JUN)
df["fquarter"] = df["month"].dt.to_period("Q-JUN")
fq = df.groupby(["entity","dept","fquarter"], as_index=False)["amount"].sum()
print(q.head(), fq.head())
```

## SQL sketch (Postgres)
```sql
SELECT
  entity,
  dept,
  DATE_TRUNC('quarter', month)::date AS quarter_start,
  SUM(amount) AS amount_q
FROM fact_monthly
GROUP BY 1,2,3;
-- Fiscal quarters: shift by 6 months then DATE_TRUNC('quarter'), shift back.
```

## Checks
- Totals tie to monthly source
- Partial quarters handled (missing months = 0)
- Rounding rules documented

**Examples:** see `forecast_monthly.csv` in Examples

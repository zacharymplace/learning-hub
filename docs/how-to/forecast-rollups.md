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



## SQL recipes

### Postgres
```sql
-- Calendar quarter totals
SELECT
  entity,
  dept,
  date_trunc('quarter', month)::date AS quarter_start,
  SUM(amount) AS amount_q
FROM fact_monthly
GROUP BY 1,2,3;

-- QTD / YTD running totals
SELECT
  entity, dept, month::date,
  SUM(amount) OVER (
    PARTITION BY entity, dept, date_trunc('quarter', month)
    ORDER BY month
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS amount_qtd,
  SUM(amount) OVER (
    PARTITION BY entity, dept, date_trunc('year', month)
    ORDER BY month
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS amount_ytd
FROM fact_monthly;

-- Fiscal quarters starting July (shift 6 months)
SELECT
  entity,
  dept,
  (date_trunc('quarter', month - INTERVAL '6 months') + INTERVAL '6 months')::date AS fiscal_q_start,
  SUM(amount) AS amount_fq
FROM fact_monthly
GROUP BY 1,2,3;
```

### SQL Server
```sql
-- Calendar quarter totals
SELECT
  entity,
  dept,
  DATEADD(QUARTER, DATEDIFF(QUARTER, 0, [month]), 0) AS quarter_start,
  SUM(amount) AS amount_q
FROM fact_monthly
GROUP BY entity, dept, DATEADD(QUARTER, DATEDIFF(QUARTER, 0, [month]), 0);

-- QTD / YTD running totals
SELECT
  entity,
  dept,
  [month],
  SUM(amount) OVER (
    PARTITION BY entity, dept, YEAR([month]), DATEPART(QUARTER, [month])
    ORDER BY [month]
    ROWS UNBOUNDED PRECEDING
  ) AS amount_qtd,
  SUM(amount) OVER (
    PARTITION BY entity, dept, YEAR([month])
    ORDER BY [month]
    ROWS UNBOUNDED PRECEDING
  ) AS amount_ytd
FROM fact_monthly;

-- Fiscal quarters starting July (shift 6 months)
SELECT
  entity,
  dept,
  DATEADD(MONTH, 6,
    DATEADD(QUARTER, DATEDIFF(QUARTER, 0, DATEADD(MONTH, -6, [month])), 0)
  ) AS fiscal_q_start,
  SUM(amount) AS amount_fq
FROM fact_monthly
GROUP BY
  entity, dept,
  DATEADD(MONTH, 6,
    DATEADD(QUARTER, DATEDIFF(QUARTER, 0, DATEADD(MONTH, -6, [month])), 0)
  );
```

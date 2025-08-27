# scripts/generate_pq_handoff_examples.py
from __future__ import annotations

import argparse
from datetime import date, timedelta
from pathlib import Path

import pandas as pd


# --- Standard schema used in the How-To page ---
SCHEMA = {
    "txn_id": "string",
    "account_id": "string",
    "merchant": "string",
    "memo": "string",
    "category": "string",
    "currency": "string",
    "amount": "float64",
}

DATE_COLS = ["txn_date", "posted_date"]
BOOL_COLS = ["is_recurring", "is_refund"]
ORDER = [
    "txn_id",
    "txn_date",
    "posted_date",
    "account_id",
    "merchant",
    "memo",
    "category",
    "currency",
    "amount",
    "is_recurring",
    "is_refund",
]


def create_sample_dataframe(n: int = 8) -> pd.DataFrame:
    """Build a small, typeful demo set with edge cases."""
    base = date.today() - timedelta(days=10)
    rows = [
        {
            "txn_id": "T0001",
            "txn_date": base,
            "posted_date": base + timedelta(days=1),
            "account_id": "10001",
            "merchant": "Acme Supplies",
            "memo": "Office restock",
            "category": "Office",
            "currency": "USD",
            "amount": 123.45,
            "is_recurring": False,
            "is_refund": False,
        },
        {
            # leading zeros (keep as text)
            "txn_id": "T0002",
            "txn_date": base + timedelta(days=1),
            "posted_date": base + timedelta(days=2),
            "account_id": "000123",
            "merchant": "Transit Pass",
            "memo": "CTA reload",
            "category": "Transport",
            "currency": "USD",
            "amount": 25.00,
            "is_recurring": True,
            "is_refund": False,
        },
        {
            # negative (refund)
            "txn_id": "T0003",
            "txn_date": base + timedelta(days=2),
            "posted_date": base + timedelta(days=3),
            "account_id": "10002",
            "merchant": "Acme Supplies",
            "memo": "Returned items",
            "category": "Office",
            "currency": "USD",
            "amount": -12.50,
            "is_recurring": False,
            "is_refund": True,
        },
        {
            # special chars / accents
            "txn_id": "T0004",
            "txn_date": base + timedelta(days=3),
            "posted_date": base + timedelta(days=4),
            "account_id": "10003",
            "merchant": "Café Río",
            "memo": "Team lunch – Q3 kickoff",
            "category": "Meals",
            "currency": "USD",
            "amount": 87.99,
            "is_recurring": False,
            "is_refund": False,
        },
        {
            # missing boolean (nullable boolean demo)
            "txn_id": "T0005",
            "txn_date": base + timedelta(days=4),
            "posted_date": base + timedelta(days=5),
            "account_id": "10004",
            "merchant": "Data Warehouse",
            "memo": "Monthly subscription",
            "category": "SaaS",
            "currency": "USD",
            "amount": 499.00,
            "is_recurring": None,
            "is_refund": False,
        },
        {
            "txn_id": "T0006",
            "txn_date": base + timedelta(days=5),
            "posted_date": base + timedelta(days=6),
            "account_id": "10005",
            "merchant": "Git Hosting",
            "memo": 'Plan upgrade (includes "Actions" minutes)',
            "category": "SaaS",
            "currency": "USD",
            "amount": 19.00,
            "is_recurring": True,
            "is_refund": False,
        },
        {
            # different currency
            "txn_id": "T0007",
            "txn_date": base + timedelta(days=6),
            "posted_date": base + timedelta(days=7),
            "account_id": "10006",
            "merchant": "Cloud Storage",
            "memo": "Annual plan",
            "category": "SaaS",
            "currency": "EUR",
            "amount": 220.00,
            "is_recurring": True,
            "is_refund": False,
        },
        {
            # NaN amount to test numeric coercion
            "txn_id": "T0008",
            "txn_date": base + timedelta(days=7),
            "posted_date": base + timedelta(days=8),
            "account_id": "10007",
            "merchant": "Unknown Vendor",
            "memo": "Pending classification",
            "category": "",
            "currency": "USD",
            "amount": float("nan"),
            "is_recurring": False,
            "is_refund": False,
        },
    ]
    df = pd.DataFrame(rows[:n])

    # Pandas datetime, tz-naive
    for c in DATE_COLS:
        df[c] = pd.to_datetime(df[c], errors="coerce").dt.tz_localize(None)

    # Enforce string dtypes
    for col, typ in SCHEMA.items():
        if typ == "string":
            df[col] = df[col].astype("string")

    # Nullable boolean
    for c in BOOL_COLS:
        df[c] = df[c].astype("boolean")

    return df


def normalize_and_order(df: pd.DataFrame) -> pd.DataFrame:
    # normalize headers
    df.columns = (
        df.columns.str.strip().str.lower().str.replace(r"[^a-z0-9]+", "_", regex=True)
    )
    # ensure all schema cols present & cast types
    for col, typ in SCHEMA.items():
        if col not in df.columns:
            df[col] = pd.Series(
                [None] * len(df), dtype="string" if typ == "string" else typ
            )
        else:
            df[col] = df[col].astype(typ)

    # datetime already coerced; make sure tz-naive
    for c in DATE_COLS:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce").dt.tz_localize(None)

    # booleans
    for c in BOOL_COLS:
        if c in df.columns:
            df[c] = df[c].astype("boolean")

    # order columns
    present = [c for c in ORDER if c in df.columns]
    rest = [c for c in df.columns if c not in present]
    return df[present + rest]


def export_parquet(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)  # pyarrow engine by default if installed


def export_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # format datetime columns as YYYY-MM-DD to avoid TZ surprises
    df_out = df.copy()
    for c in DATE_COLS:
        if c in df_out.columns:
            df_out[c] = pd.to_datetime(df_out[c], errors="coerce").dt.strftime(
                "%Y-%m-%d"
            )
    df_out.to_csv(path, index=False, encoding="utf-8", lineterminator="\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate PQ handoff example files.")
    parser.add_argument(
        "--outdir",
        default="examples",
        help="Directory to write sample files into (default: ./examples)",
    )
    args = parser.parse_args()

    outdir = Path(args.outdir)
    df = create_sample_dataframe()
    df = normalize_and_order(df)

    export_parquet(df, outdir / "pq_handoff_sample.parquet")
    export_csv(df, outdir / "pq_handoff_sample.csv")

    print(f"Wrote: {outdir / 'pq_handoff_sample.parquet'}")
    print(f"Wrote: {outdir / 'pq_handoff_sample.csv'}")


if __name__ == "__main__":
    main()

## Safe date window
```sql
WHERE txn_date >= DATEADD(day, -30, CAST(GETDATE() AS date))
```

## Null-safe join key
```sql
ON COALESCE(a.key, '') = COALESCE(b.key, '')
```

## Idempotent staging
```sql
TRUNCATE TABLE stg_import;
BULK INSERT stg_import FROM 'blob/path.csv' WITH (FIRSTROW=2, FIELDTERMINATOR=',', ROWTERMINATOR='\n');
MERGE dim_merchant AS d
USING stg_import AS s
ON d.merchant_id = s.merchant_id
WHEN MATCHED THEN UPDATE SET d.name = s.name
WHEN NOT MATCHED THEN INSERT (merchant_id, name) VALUES (s.merchant_id, s.name);
```

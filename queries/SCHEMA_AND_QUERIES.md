# Benchmark queries (V3 concurrent benchmark)

These are the exact operations executed by `notebooks/ICIMCIS_MySQL_MongoDB_Benchmark_V3_15Reps.ipynb`
(MySQL via PyMySQL, MongoDB via PyMongo). They correspond to Table II of the paper.

| Workload | MySQL | MongoDB (PyMongo) |
|---|---|---|
| INSERT | `INSERT INTO transactions VALUES (%s,%s,%s,%s)` | `insert_one({'Transaction_ID':t,'User_ID':u,'Product_ID':p,'Purchase':v})` |
| SELECT | `SELECT Transaction_ID,User_ID,Product_ID,Purchase FROM transactions WHERE Purchase > %s ORDER BY Purchase DESC,Transaction_ID ASC LIMIT 200` | `find({'Purchase':{'$gt':t}}, {'_id':0,'Transaction_ID':1,'User_ID':1,'Product_ID':1,'Purchase':1}).sort([('Purchase',-1),('Transaction_ID',1)]).limit(200)` |
| UPDATE | `UPDATE transactions SET Purchase=Purchase+1 WHERE Transaction_ID=%s` | `update_one({'Transaction_ID':id}, {'$inc':{'Purchase':1}})` |
| DELETE | `DELETE FROM transactions WHERE Transaction_ID=%s` | `delete_one({'Transaction_ID':id})` |

## Multi-entity read

MySQL:

```sql
SELECT t.Transaction_ID, t.Purchase, u.Gender, p.Product_Category
FROM transactions t
JOIN users u ON t.User_ID = u.User_ID
JOIN products p ON t.Product_ID = p.Product_ID
WHERE t.Purchase > %s
ORDER BY t.Purchase DESC, t.Transaction_ID ASC
LIMIT 200;
```

MongoDB:

```python
pipeline = [
  {'$match': {'Purchase': {'$gt': t}}},
  {'$sort': {'Purchase': -1, 'Transaction_ID': 1}},
  {'$limit': 200},
  {'$lookup': {'from': 'users', 'localField': 'User_ID', 'foreignField': 'User_ID', 'as': 'u'}},
  {'$unwind': '$u'},
  {'$lookup': {'from': 'products', 'localField': 'Product_ID', 'foreignField': 'Product_ID', 'as': 'p'}},
  {'$unwind': '$p'},
  {'$project': {'_id': 0, 'Transaction_ID': 1, 'Purchase': 1,
                'Gender': '$u.Gender', 'Product_Category': '$p.Product_Category'}}
]
transactions.aggregate(pipeline)
```

## Parameters

- Deterministic request plans, master seed `20261015`; the same plan is used for both databases within a pair.
- SELECT / multi-entity threshold `t` is drawn from 5,000–18,000.
- UPDATE / DELETE target existing `Transaction_ID` values; INSERT uses new `Transaction_ID` values with valid `User_ID` / `Product_ID` references.
- Transactions are reset to the relevant subset before every database trial (not timed); five indexed-key reads are run as untimed warm-up.
- The number of affected or returned rows is checked for every request.

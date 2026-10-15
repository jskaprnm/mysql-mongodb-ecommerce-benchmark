# MySQL vs MongoDB Benchmark for an E-Commerce-Derived Workload

Code, schema, queries, and results for the paper
*"Performance Comparison of MySQL and MongoDB for E-Commerce Applications."*

## Repository contents

| Path | Description |
|---|---|
| `notebooks/ICIMCIS_MySQL_MongoDB_Benchmark_V3_15Reps.ipynb` | Full V3 concurrent benchmark (installs servers, builds schema, runs trials, computes statistics) |
| `scripts/transform_dataset.py` | Transformation of the raw dataset into Users, Products, and Transactions |
| `schema/schema_mysql.sql` | MySQL DDL (InnoDB, primary and foreign keys) |
| `schema/indexes_mongodb.js` | MongoDB collections, indexes, and write concern |
| `queries/SCHEMA_AND_QUERIES.md` | All benchmark queries for both databases |
| `config/experiment_manifest.json` | Software versions, durability settings, seed, and design |
| `results/TABLE_*.csv`, `results/VERIFICATION_REPORT.json` | Aggregated results reported in the paper |
| `results/raw/` | Run-level results (1,800 trials) and per-request latencies (420,000 requests, gzip) |
| `results/figures/` | Throughput and P95 latency figures |
| `data/README.md` | Dataset source and checksums (data not included) |

## Experimental design

- Environment: Google Colab, Ubuntu 24.04.5 LTS, 2 logical CPUs; MySQL 8.0.46 (InnoDB), MongoDB 8.0.34 (WiredTiger, standalone)
- Durability: `innodb_flush_log_at_trx_commit=1`, `sync_binlog=1`; MongoDB `w=1, j=true`
- Volumes: 1,000 / 10,000 / 15,000 / 20,000 transactions
- Clients: 5 / 10 / 20 concurrent clients, 20 requests each
- Workloads: INSERT, SELECT, UPDATE, DELETE, multi-entity read
- 15 paired repetitions per condition (1,800 trials, 420,000 requests), master seed 20261015
- Statistics: geometric mean of paired throughput ratios, pointwise 95% bootstrap CI (5,000 resamples),
  two-sided Wilcoxon signed-rank test on log ratios, Holm correction
  (4 primary CRUD comparisons at 20,000 records and 20 clients; 60 exploratory comparisons as a separate family)

## How to reproduce

1. Obtain the source dataset and generate the inputs as described in `data/README.md`.
2. Open the notebook in Google Colab (Ubuntu 22.04/24.04 runtime).
3. Run the cells in order; upload `users.csv`, `products.csv`, and `transactions_20000.csv` when prompted.
4. Set `RUN_MODE = 'full'` for the complete 15-repetition run (a `smoke` mode is available for a quick check).
5. Outputs are written to the output folder and can be compared with `results/`.

## License

Code: MIT (see `LICENSE`). The dataset is not covered by this license and is not distributed.

# Dataset

The source dataset and the derived CSV files are **not** included in this repository.

**Source:** V. Devaraj, "e-Commerce (Walmart) sales dataset," Kaggle, version 1, May 2024,
https://www.kaggle.com/datasets/devarajv88/walmart-sales-dataset (downloaded May 18, 2025).
The dataset has since been removed from Kaggle. Because its redistribution terms could not be
confirmed, neither the raw file nor the derived files are redistributed here.

## Reproducing the inputs

1. Place a copy of the original file at `data/walmart.csv`.
2. Run `python scripts/transform_dataset.py data/walmart.csv data/`.
3. The script prints SHA-256 checksums and compares them with the values below.

The script was verified against the authors' archived files: `users.csv`, `products.csv`, and the
1,000-, 10,000-, and 20,000-row subsets are reproduced byte for byte. The archived 15,000-row file
differs only in formatting (Purchase written as `8370.0` instead of `8370`); all values are identical,
and the V3 benchmark does not read that file.

| File | Rows | SHA-256 |
|---|---|---|
| walmart.csv (raw) | 550,068 | 0e8924538cd002ccad1f865d39e3b3860c2b8ab49d85d9c34a6d8ad1fbabb5c9 |
| users.csv | 5,891 | 38f3337df71bc9fa710037f98f4d2da4206e4d0ada4a5d4a7402276768a883f5 |
| products.csv | 3,631 | 0f0a2a94e227c4d487242bdffd82c01e83b30e0de1006891119fadf924ceef6a |
| transactions_1000.csv | 1,000 | a112c7776ae32e36aef2b73bacacbf40efcb1696b7105988e521ab5046376ff1 |
| transactions_10000.csv | 10,000 | 1b89f1d5dc675d597c71bd1ebad1fcc3aeaa7671f5865eaa388d57479878137d |
| transactions_15000.csv | 15,000 | 869087ae4a12d84d491184286365616a595b60d4cc60f54b2e8b51a61efd38d8 |
| transactions_20000.csv | 20,000 | 1792cc24492c244989141f23b2d0bb3598541bcb1287f9b40885ca71ee7881ed |

The benchmark notebook reads `users.csv`, `products.csv`, and `transactions_20000.csv`
(the 1,000/10,000/15,000 subsets are the first N rows of the 20,000-row file).

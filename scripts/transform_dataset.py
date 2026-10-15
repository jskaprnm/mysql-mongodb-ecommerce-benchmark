"""Transform the raw e-Commerce (Walmart) Sales Dataset into Users, Products, and Transactions.

Implements the procedure described in Section III-A of the paper (equivalent to the
authors' original split notebook; verified against the archived CSV files, see data/README.md):
  * users.csv        - unique users with their demographic attributes
  * products.csv     - unique products with their category
  * transactions_N.csv for N in {1000, 10000, 15000, 20000}
                     - first N source rows, with a sequential synthetic Transaction_ID

Usage:
    python scripts/transform_dataset.py data/walmart.csv data/

The script prints SHA-256 checksums and compares them with config/experiment_manifest.json.
"""
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd

USER_COLS = ['User_ID', 'Gender', 'Age', 'Occupation', 'City_Category',
             'Stay_In_Current_City_Years', 'Marital_Status']
PRODUCT_COLS = ['Product_ID', 'Product_Category']
VOLUMES = [1000, 10000, 15000, 20000]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main(raw_csv: str, out_dir: str) -> None:
    raw_path, out = Path(raw_csv), Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(raw_path)
    assert len(raw) == 550_068, f'unexpected row count: {len(raw)}'
    assert raw.isna().sum().sum() == 0, 'source contains missing values'

    users = raw[USER_COLS].drop_duplicates().reset_index(drop=True)
    products = raw[PRODUCT_COLS].drop_duplicates().reset_index(drop=True)
    assert users['User_ID'].is_unique and products['Product_ID'].is_unique
    users.to_csv(out / 'users.csv', index=False)
    products.to_csv(out / 'products.csv', index=False)

    for n in VOLUMES:
        t = raw.iloc[:n][['User_ID', 'Product_ID', 'Purchase']].copy()
        t.insert(0, 'Transaction_ID', range(1, n + 1))
        assert t['User_ID'].isin(users['User_ID']).all()
        assert t['Product_ID'].isin(products['Product_ID']).all()
        t.to_csv(out / f'transactions_{n}.csv', index=False)

    print(f'users: {len(users)} rows, products: {len(products)} rows')

    manifest = Path(__file__).resolve().parents[1] / 'config' / 'experiment_manifest.json'
    expected = json.loads(manifest.read_text())['input_sha256'] if manifest.exists() else {}
    files = {'walmart.csv': raw_path, 'users.csv': out / 'users.csv',
             'products.csv': out / 'products.csv',
             'transactions_20000.csv': out / 'transactions_20000.csv'}
    for name, path in files.items():
        digest = sha256(path)
        status = '' if name not in expected else ('MATCH' if digest == expected[name] else 'MISMATCH')
        print(f'{name:24s} {digest} {status}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('usage: python scripts/transform_dataset.py <walmart.csv> <output_dir>')
    main(sys.argv[1], sys.argv[2])

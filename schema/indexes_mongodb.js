// MongoDB 8.0.34 (standalone, WiredTiger) collections used in the V3 benchmark.
// Collections: users, products, transactions (same fields as MySQL, no embedding,
// no server-enforced foreign keys). Identical to the notebook setup.

db.users.createIndex({ User_ID: 1 }, { unique: true });
db.products.createIndex({ Product_ID: 1 }, { unique: true });
db.transactions.createIndex({ Transaction_ID: 1 }, { unique: true });
// Mirror the foreign-key indexes that InnoDB creates automatically in MySQL:
db.transactions.createIndex({ User_ID: 1 });
db.transactions.createIndex({ Product_ID: 1 });
// No index on Purchase.

// Write concern for all benchmark writes: { w: 1, j: true, wtimeout: 60000 }

// Example transaction document:
// { Transaction_ID: 1, User_ID: 1000001, Product_ID: "P00069042", Purchase: 8370 }

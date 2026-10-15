-- MySQL 8.0.46 (InnoDB) schema used in the V3 concurrent benchmark.
-- Identical to the DDL executed in notebooks/ICIMCIS_MySQL_MongoDB_Benchmark_V3_15Reps.ipynb.

CREATE TABLE users (
  User_ID INT PRIMARY KEY,
  Gender VARCHAR(1),
  Age VARCHAR(8),
  Occupation INT,
  City_Category VARCHAR(1),
  Stay_In_Current_City_Years VARCHAR(3),
  Marital_Status INT
) ENGINE=InnoDB;

CREATE TABLE products (
  Product_ID VARCHAR(16) PRIMARY KEY,
  Product_Category INT
) ENGINE=InnoDB;

CREATE TABLE transactions (
  Transaction_ID INT PRIMARY KEY,
  User_ID INT NOT NULL,
  Product_ID VARCHAR(16) NOT NULL,
  Purchase DECIMAL(10,2) NOT NULL,
  CONSTRAINT fk_user FOREIGN KEY (User_ID) REFERENCES users(User_ID),
  CONSTRAINT fk_product FOREIGN KEY (Product_ID) REFERENCES products(Product_ID)
) ENGINE=InnoDB;

-- InnoDB automatically indexes the foreign-key columns transactions.User_ID and transactions.Product_ID.
-- No index on Purchase.
-- Durability settings: innodb_flush_log_at_trx_commit = 1, sync_binlog = 1,
-- binary logging enabled, autocommit on.

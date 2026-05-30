-- Schema for customer-level churn dataset (CSV)
-- Works in SQLite. For Postgres/MySQL, adjust types and date functions accordingly.

DROP TABLE IF EXISTS ecomm_customers;

CREATE TABLE ecomm_customers (
  CustomerID INTEGER PRIMARY KEY,
  Churn INTEGER,
  Tenure REAL,
  PreferredLoginDevice TEXT,
  CityTier INTEGER,
  WarehouseToHome REAL,
  PreferredPaymentMode TEXT,
  Gender TEXT,
  HourSpendOnApp REAL,
  NumberOfDeviceRegistered INTEGER,
  PreferedOrderCat TEXT,
  SatisfactionScore REAL,
  MaritalStatus TEXT,
  NumberOfAddress INTEGER,
  Complain INTEGER,
  OrderAmountHikeFromlastYear REAL,
  CouponUsed REAL,
  OrderCount REAL,
  DaySinceLastOrder REAL,
  CashbackAmount REAL
);

-- Load notes (SQLite):
-- .mode csv
-- .import "data/raw/E Commerce Dataset tab2.csv" ecomm_customers

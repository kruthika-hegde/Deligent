import pandas as pd
import sqlite3
import os

# Database file path
db_path = 'ecom.db'

# Remove existing database if it exists
if os.path.exists(db_path):
    os.remove(db_path)

# Create connection
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Enable foreign keys
cursor.execute('PRAGMA foreign_keys = ON')

# ================== CREATE TABLES ==================

# Customers table
cursor.execute('''
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    created_at TEXT NOT NULL
)
''')

# Products table
cursor.execute('''
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
)
''')

# Orders table
cursor.execute('''
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    total_amount REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)
''')

# Payments table
cursor.execute('''
CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    method TEXT NOT NULL,
    payment_date TEXT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
)
''')

# Shipments table
cursor.execute('''
CREATE TABLE shipments (
    shipment_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    shipment_date TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
)
''')

print("✓ Tables created successfully")

# ================== LOAD DATA FROM CSV ==================

# Load customers
customers_df = pd.read_csv('data/customers.csv')
customers_df.to_sql('customers', conn, if_exists='append', index=False)
print(f"✓ Loaded {len(customers_df)} customers")

# Load products
products_df = pd.read_csv('data/products.csv')
products_df.to_sql('products', conn, if_exists='append', index=False)
print(f"✓ Loaded {len(products_df)} products")

# Load orders
orders_df = pd.read_csv('data/orders.csv')
orders_df.to_sql('orders', conn, if_exists='append', index=False)
print(f"✓ Loaded {len(orders_df)} orders")

# Load payments
payments_df = pd.read_csv('data/payments.csv')
payments_df.to_sql('payments', conn, if_exists='append', index=False)
print(f"✓ Loaded {len(payments_df)} payments")

# Load shipments
shipments_df = pd.read_csv('data/shipments.csv')
shipments_df.to_sql('shipments', conn, if_exists='append', index=False)
print(f"✓ Loaded {len(shipments_df)} shipments")

# Commit and close
conn.commit()
conn.close()

print("\n✅ Data successfully ingested into ecom.db")

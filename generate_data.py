import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Create data folder if it doesn't exist
os.makedirs('data', exist_ok=True)

# ================== CUSTOMERS ==================
num_customers = 250
first_names = ['John', 'Jane', 'Michael', 'Sarah', 'James', 'Emily', 'Robert', 'Jessica', 'William', 'Mary',
               'David', 'Patricia', 'Richard', 'Jennifer', 'Joseph', 'Linda', 'Thomas', 'Barbara', 'Charles', 'Elizabeth',
               'Christopher', 'Susan', 'Daniel', 'Jessica', 'Matthew', 'Sarah', 'Anthony', 'Karen', 'Mark', 'Nancy',
               'Donald', 'Lisa', 'Steven', 'Betty', 'Paul', 'Margaret', 'Andrew', 'Sandra', 'Joshua', 'Ashley',
               'Kenneth', 'Kimberly', 'Kevin', 'Emily', 'Brian', 'Donna', 'Edward', 'Michelle', 'Ronald', 'Carol']
last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
              'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
              'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson',
              'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Peterson', 'Phillips', 'Campbell', 'Parker']

customers = []
for i in range(num_customers):
    customer_id = i + 1
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    email = f"{name.replace(' ', '.').lower()}_{customer_id}@email.com"
    phone = f"+1{random.randint(2000000000, 9999999999)}"
    created_at = (datetime.now() - timedelta(days=np.random.randint(30, 365))).strftime('%Y-%m-%d %H:%M:%S')
    
    customers.append({
        'customer_id': customer_id,
        'name': name,
        'email': email,
        'phone': phone,
        'created_at': created_at
    })

customers_df = pd.DataFrame(customers)
customers_df.to_csv('data/customers.csv', index=False)
print(f"✓ Generated {len(customers_df)} customers")

# ================== PRODUCTS ==================
num_products = 150
categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Toys', 'Beauty', 'Food', 'Furniture', 'Automotive']
product_templates = {
    'Electronics': ['Laptop', 'Phone', 'Tablet', 'Headphones', 'Camera', 'Smart Watch', 'Speaker', 'Monitor'],
    'Clothing': ['T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Sweater', 'Shoes', 'Hat', 'Scarf'],
    'Home & Garden': ['Lamp', 'Chair', 'Table', 'Bed', 'Sofa', 'Desk', 'Mirror', 'Bookshelf'],
    'Sports': ['Running Shoes', 'Tennis Racket', 'Yoga Mat', 'Bicycle', 'Dumbbells', 'Basketball', 'Football', 'Golf Set'],
    'Books': ['Fiction Novel', 'Non-Fiction', 'Biography', 'Self-Help', 'Science Book', 'History Book', 'Mystery', 'Cookbook'],
    'Toys': ['Action Figure', 'Board Game', 'LEGO Set', 'Puzzle', 'Doll', 'Remote Car', 'Building Blocks', 'Trading Cards'],
    'Beauty': ['Face Cream', 'Shampoo', 'Lipstick', 'Foundation', 'Perfume', 'Face Mask', 'Body Lotion', 'Eye Shadow'],
    'Food': ['Coffee', 'Chocolate', 'Snacks', 'Tea', 'Granola', 'Nuts', 'Olive Oil', 'Spices'],
    'Furniture': ['Cabinet', 'Nightstand', 'Dresser', 'Wardrobe', 'Bench', 'Storage Box', 'Shelving Unit', 'Desk Organizer'],
    'Automotive': ['Car Battery', 'Air Filter', 'Tire', 'Oil Can', 'Wiper Blade', 'Seat Cover', 'Floor Mat', 'Car Air Freshener']
}

products = []
product_id = 1
for category in categories:
    for product_name in product_templates[category]:
        price = round(np.random.uniform(10, 500), 2)
        products.append({
            'product_id': product_id,
            'product_name': product_name,
            'category': category,
            'price': price
        })
        product_id += 1

products_df = pd.DataFrame(products[:num_products])
products_df.to_csv('data/products.csv', index=False)
print(f"✓ Generated {len(products_df)} products")

# ================== ORDERS ==================
num_orders = 400
orders = []
order_id = 1
for _ in range(num_orders):
    customer_id = np.random.randint(1, num_customers + 1)
    order_date = (datetime.now() - timedelta(days=np.random.randint(1, 180))).strftime('%Y-%m-%d %H:%M:%S')
    # Generate a random total amount based on 1-5 products
    num_items = np.random.randint(1, 6)
    total_amount = round(sum(np.random.choice(products_df['price'].values, num_items)), 2)
    
    orders.append({
        'order_id': order_id,
        'customer_id': customer_id,
        'order_date': order_date,
        'total_amount': total_amount
    })
    order_id += 1

orders_df = pd.DataFrame(orders)
orders_df.to_csv('data/orders.csv', index=False)
print(f"✓ Generated {len(orders_df)} orders")

# ================== PAYMENTS ==================
payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Apple Pay', 'Google Pay', 'Bank Transfer', 'Cryptocurrency']
payments = []
payment_id = 1
for _, order in orders_df.iterrows():
    # Each order can have one or more payments (split payments allowed)
    num_payments = np.random.randint(1, 3)
    if num_payments == 1:
        # Single payment for full amount
        amount = order['total_amount']
        payment_date = (pd.to_datetime(order['order_date']) + timedelta(hours=np.random.randint(1, 48))).strftime('%Y-%m-%d %H:%M:%S')
        payments.append({
            'payment_id': payment_id,
            'order_id': order['order_id'],
            'amount': amount,
            'method': random.choice(payment_methods),
            'payment_date': payment_date
        })
        payment_id += 1
    else:
        # Split payments
        amounts = []
        remaining = order['total_amount']
        for i in range(num_payments - 1):
            amount = round(remaining * np.random.uniform(0.3, 0.7), 2)
            amounts.append(amount)
            remaining -= amount
        amounts.append(round(remaining, 2))
        
        for amount in amounts:
            payment_date = (pd.to_datetime(order['order_date']) + timedelta(hours=np.random.randint(1, 48))).strftime('%Y-%m-%d %H:%M:%S')
            payments.append({
                'payment_id': payment_id,
                'order_id': order['order_id'],
                'amount': amount,
                'method': random.choice(payment_methods),
                'payment_date': payment_date
            })
            payment_id += 1

payments_df = pd.DataFrame(payments)
payments_df.to_csv('data/payments.csv', index=False)
print(f"✓ Generated {len(payments_df)} payments")

# ================== SHIPMENTS ==================
shipment_statuses = ['Pending', 'Processing', 'Shipped', 'In Transit', 'Out for Delivery', 'Delivered', 'Cancelled', 'Returned']
shipments = []
shipment_id = 1
for _, order in orders_df.iterrows():
    shipment_date = (pd.to_datetime(order['order_date']) + timedelta(days=np.random.randint(1, 30))).strftime('%Y-%m-%d %H:%M:%S')
    status = random.choice(shipment_statuses)
    
    shipments.append({
        'shipment_id': shipment_id,
        'order_id': order['order_id'],
        'shipment_date': shipment_date,
        'status': status
    })
    shipment_id += 1

shipments_df = pd.DataFrame(shipments)
shipments_df.to_csv('data/shipments.csv', index=False)
print(f"✓ Generated {len(shipments_df)} shipments")

print("\n✅ All synthetic data generated successfully!")
print(f"   - customers.csv: {len(customers_df)} rows")
print(f"   - products.csv: {len(products_df)} rows")
print(f"   - orders.csv: {len(orders_df)} rows")
print(f"   - payments.csv: {len(payments_df)} rows")
print(f"   - shipments.csv: {len(shipments_df)} rows")

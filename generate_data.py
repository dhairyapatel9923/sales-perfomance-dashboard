import mysql.connector
import pandas as pd
import random
from datetime import datetime, timedelta

# ==========================================
# MYSQL SETTINGS
# ==========================================

MYSQL_PASSWORD = "SalesDB@8426"

# ==========================================
# CONNECT TO MYSQL
# ==========================================

connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password=MYSQL_PASSWORD,
    database="sales_dashboard"
)

cursor = connection.cursor()

# ==========================================
# GET CURRENT HIGHEST SALE ID
# ==========================================

cursor.execute(
    "SELECT COALESCE(MAX(sale_id), 0) FROM sales"
)

max_sale_id = cursor.fetchone()[0]

print("Current highest sale_id:", max_sale_id)

# ==========================================
# DATA OPTIONS
# ==========================================

products = {
    "Laptop": ("Electronics", 55000, 42000),
    "Monitor": ("Electronics", 18000, 13000),
    "Printer": ("Office", 15000, 10500),
    "Keyboard": ("Accessories", 2500, 1500),
    "Mouse": ("Accessories", 1200, 650),
    "Headphones": ("Accessories", 3500, 2100),
    "Tablet": ("Electronics", 25000, 18000),
    "Webcam": ("Accessories", 4500, 2800),
    "Router": ("Electronics", 5000, 3200),
    "Office Chair": ("Office", 12000, 8500)
}

regions = [
    "North",
    "South",
    "East",
    "West"
]

salespeople = [
    "Rahul",
    "Priya",
    "Amit",
    "Sneha",
    "Vikram",
    "Anjali",
    "Rohan",
    "Neha"
]

# ==========================================
# GENERATE 500 NEW RECORDS
# ==========================================

records = []

start_date = datetime(2026, 1, 1)

for i in range(1, 501):

    sale_id = max_sale_id + i

    sale_date = start_date + timedelta(
        days=random.randint(0, 364)
    )

    product_name = random.choice(
        list(products.keys())
    )

    category, unit_price, cost_price = products[
        product_name
    ]

    quantity = random.randint(1, 8)

    region = random.choice(regions)

    salesperson = random.choice(salespeople)

    total_sales = unit_price * quantity

    total_cost = cost_price * quantity

    total_profit = total_sales - total_cost

    records.append([
        sale_id,
        sale_date.strftime("%Y-%m-%d"),
        product_name,
        category,
        region,
        salesperson,
        quantity,
        unit_price,
        cost_price,
        total_sales,
        total_profit
    ])

# ==========================================
# CREATE DATAFRAME
# ==========================================

columns = [
    "sale_id",
    "sale_date",
    "product_name",
    "category",
    "region",
    "salesperson",
    "quantity",
    "unit_price",
    "cost_price",
    "total_sales",
    "total_profit"
]

new_df = pd.DataFrame(
    records,
    columns=columns
)

# ==========================================
# SAVE CSV BACKUP
# ==========================================

new_df.to_csv(
    "new_sales_data.csv",
    index=False
)

print("500 new records generated.")
print("CSV backup created: new_sales_data.csv")

# ==========================================
# INSERT INTO MYSQL
# ==========================================

insert_query = """
INSERT INTO sales (
    sale_id,
    sale_date,
    product_name,
    category,
    region,
    salesperson,
    quantity,
    unit_price,
    cost_price,
    total_sales,
    total_profit
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

cursor.executemany(
    insert_query,
    records
)

connection.commit()

print("500 new records inserted successfully.")

# ==========================================
# VERIFY
# ==========================================

cursor.execute(
    "SELECT COUNT(*) FROM sales"
)

total_records = cursor.fetchone()[0]

print("Total records now:", total_records)

cursor.close()
connection.close()

print("Done!")
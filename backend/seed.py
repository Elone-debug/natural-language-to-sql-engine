"""Create a deterministic demo e-commerce database."""
import random
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).with_name("database.db")

FIRST = ["Aarav", "Maya", "Noah", "Olivia", "Liam", "Sophia", "Ethan", "Zara", "Leo", "Emma"]
LAST = ["Sharma", "Patel", "Smith", "Johnson", "Brown", "Garcia", "Wilson", "Martin"]
CITIES = ["Mumbai", "Bengaluru", "Delhi", "Chennai", "Kochi", "Pune", "Hyderabad", "Kolkata"]
CATEGORIES = {
    "Electronics": ["Wireless Headphones", "Smart Watch", "USB-C Hub", "Webcam", "Bluetooth Speaker"],
    "Home": ["Desk Lamp", "Coffee Maker", "Air Purifier", "Throw Blanket", "Storage Basket"],
    "Office": ["Notebook Set", "Ergonomic Mouse", "Mechanical Keyboard", "Desk Organizer", "Laptop Stand"],
    "Fitness": ["Yoga Mat", "Resistance Bands", "Water Bottle", "Foam Roller", "Fitness Tracker"],
}

def seed_database(path=DB_PATH):
    random.seed(42)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript("""
    DROP TABLE IF EXISTS orders; DROP TABLE IF EXISTS products; DROP TABLE IF EXISTS customers;
    CREATE TABLE customers (
      id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE,
      city TEXT NOT NULL, created_at TEXT NOT NULL
    );
    CREATE TABLE products (
      id INTEGER PRIMARY KEY, product_name TEXT NOT NULL, category TEXT NOT NULL,
      price REAL NOT NULL CHECK(price >= 0), stock INTEGER NOT NULL CHECK(stock >= 0)
    );
    CREATE TABLE orders (
      id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, product_id INTEGER NOT NULL,
      quantity INTEGER NOT NULL CHECK(quantity > 0), order_total REAL NOT NULL,
      order_date TEXT NOT NULL,
      FOREIGN KEY(customer_id) REFERENCES customers(id), FOREIGN KEY(product_id) REFERENCES products(id)
    );
    """)
    now = datetime.now()
    customers = []
    for i in range(1, 61):
        name = f"{FIRST[(i-1)%len(FIRST)]} {LAST[(i*3)%len(LAST)]}"
        customers.append((i, name, f"customer{i}@example.com", CITIES[(i*5)%len(CITIES)], (now-timedelta(days=i*7)).date().isoformat()))
    conn.executemany("INSERT INTO customers VALUES (?,?,?,?,?)", customers)
    products = []
    catalog = [(c, n) for c, names in CATEGORIES.items() for n in names]
    for i in range(1, 61):
        category, base = catalog[(i-1)%len(catalog)]
        products.append((i, f"{base} {((i-1)//len(catalog))+1}", category, round(9.99 + (i*13.37)%240, 2), 0 if i%13==0 else (i*7)%81))
    conn.executemany("INSERT INTO products VALUES (?,?,?,?,?)", products)
    orders = []
    for i in range(1, 121):
        cid, pid, qty = random.randint(1,60), random.randint(1,60), random.randint(1,5)
        total = round(products[pid-1][3]*qty, 2)
        orders.append((i,cid,pid,qty,total,(now-timedelta(days=random.randint(0,180))).date().isoformat()))
    conn.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?)", orders)
    conn.commit(); conn.close()
    print(f"Seeded {path} with 60 customers, 60 products, and 120 orders.")

if __name__ == "__main__": seed_database()


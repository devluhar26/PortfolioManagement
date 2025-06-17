
import sqlite3
from datetime import datetime

import requests

url = "https://demo.trading212.com/api/v0/equity/metadata/instruments"

headers = {"Authorization": "20155216ZtEFPdQFOwcBowmWKInkJyTKzRiLL"}

response = requests.get(url, headers=headers)

data = response.json()
print(data)
# Generate unique table name
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
table_name = f"instruments_{timestamp}"

# Connect to SQLite DB
conn = sqlite3.connect("instruments.db")
cursor = conn.cursor()

# Create new table
cursor.execute(f"""
    CREATE TABLE {table_name} (
        ticker TEXT PRIMARY KEY,
        type TEXT,
        workingScheduleId INTEGER,
        isin TEXT,
        currencyCode TEXT,
        name TEXT,
        shortName TEXT,
        minTradeQuantity REAL,
        maxOpenQuantity REAL,
        addedOn TEXT
    );
""")

# Insert data
for item in data:
    cursor.execute(f"""
        INSERT INTO {table_name} (
            ticker, type, workingScheduleId, isin, currencyCode, name,
            shortName, minTradeQuantity, maxOpenQuantity, addedOn
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        item['ticker'], item['type'], item['workingScheduleId'], item['isin'],
        item['currencyCode'], item['name'], item['shortName'],
        item['minTradeQuantity'], item['maxOpenQuantity'], item['addedOn']
    ))

conn.commit()
conn.close()

print(f"Data inserted into table '{table_name}' in 'instruments.db'.")
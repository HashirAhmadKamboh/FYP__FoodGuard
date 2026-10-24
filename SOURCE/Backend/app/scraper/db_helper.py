import os
import sqlite3
from datetime import datetime
from .config import TARGET_CITIES_NORMALIZED, get_standard_city

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "sqlite.db")

def ensure_db_ready():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name TEXT,
            scrape_date TEXT, category TEXT, item_id INTEGER,
            item_name TEXT, min_price REAL, max_price REAL, fqp REAL,
            dc_price REAL, psba_price REAL, source TEXT
        )
    ''')
    conn.commit()
    conn.close()

def clear_old_data():
    ensure_db_ready()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM price_records")
    conn.commit()
    conn.close()
    print("[DB] Cleared old price records from DB. Ready for fresh data.")

def check_if_scraping_needed():
    """Checks if the database already contains records for today's date."""
    ensure_db_ready()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT COUNT(*) FROM price_records WHERE scrape_date = ?", (today,))
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

def save_to_db(city_name, records, source):
    if not records: return
    clean_city = get_standard_city(city_name)
    if clean_city not in TARGET_CITIES_NORMALIZED: return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    formatted_records = [(*r, source, clean_city) for r in records]
    
    cursor.executemany('''
        INSERT INTO price_records (scrape_date, category, item_id, item_name, min_price, max_price, fqp, dc_price, psba_price, source, city_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', formatted_records)
    conn.commit()
    conn.close()

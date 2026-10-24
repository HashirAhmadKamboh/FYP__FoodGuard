import time
import random
import re
import urllib.parse
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from .config import AMIS_BASE_URL, AMIS_CITIES_URL, TARGET_CITIES_NORMALIZED, get_standard_city, get_standard_headers
from .db_helper import save_to_db

session = requests.Session()

def scrape_amis_city_data(city, base_date_str):
    base_dt = datetime.strptime(base_date_str, "%Y-%m-%d")
    
    dates_to_try = [base_dt, base_dt - timedelta(days=1), base_dt - timedelta(days=2)]
    headers = get_standard_headers()
    headers["Referer"] = city['url'] 

    for target_dt in dates_to_try:
        target_date_str = f"{target_dt.month}/{target_dt.day}/{target_dt.year}"
        print(f"      [AMIS] Checking date: {target_date_str} for {city['name']}...")
        
        try:
            response = session.get(city['url'], headers=headers, timeout=40)
            if response.status_code != 200: continue
            
            soup = BeautifulSoup(response.text, 'html.parser')
            form_data = {}
            for hidden in soup.find_all('input', type='hidden'):
                name = hidden.get('name')
                if name: form_data[name] = hidden.get('value', '')
            
            form_data['ctl00$cphPage$DateTextBox'] = target_date_str
            form_data['ctl00$cphPage$ReminderButton'] = 'Show prices' 
            
            time.sleep(1)
            response = session.post(city['url'], data=form_data, headers=headers, timeout=40)
            soup = BeautifulSoup(response.text, "html.parser")
            
            data_table = soup.find("table", {"class": "Grid"}) or soup.find("table", id=re.compile("Grd"))
            if not data_table:
                for t in soup.find_all("table"):
                    if "Min" in t.get_text() and "Max" in t.get_text():
                        data_table = t
                        break
            
            if not data_table: 
                print("      [AMIS] No data table found on page.")
                continue 

            rows = data_table.find_all("tr")
            records = []
            current_cat = "General"
            has_real_data = False 

            for row in rows:
                cols = row.find_all("td")
                
                if len(cols) == 1:
                    cat_val = cols[0].get_text(strip=True)
                    if cat_val and not cat_val.isdigit():
                        current_cat = cat_val
                    continue

                if len(cols) >= 5:
                    item_cell = cols[0].get_text(strip=True)
                    if not item_cell or "Commodity" in item_cell or "Dated" in item_cell: continue
                    if not re.match(r'^\d+', item_cell): continue

                    item_id_match = re.search(r'^(\d+)', item_cell)
                    item_id = int(item_id_match.group(1)) if item_id_match else 0
                    
                    item_name = re.sub(r'^\d+', '', item_cell).strip()
                    item_name = re.sub(r'(?i)100\s*kg', '1 Kg', item_name)
                    item_name = re.sub(r'(?i)100\s*(nos|pcs|pieces?)', '1 Piece', item_name)

                    def clean_val(t):
                        v = re.sub(r'[^\d.]', '', t.strip())
                        return float(v) if v else None

                    min_p = clean_val(cols[2].get_text())
                    max_p = clean_val(cols[3].get_text())
                    fqp_p = clean_val(cols[4].get_text())

                    if min_p or max_p: has_real_data = True
                        
                    if min_p or max_p or fqp_p:
                        is_dozen = "banana" in item_name.lower() or "dozen" in item_name.lower()
                        if not is_dozen:
                            if min_p: min_p = round(min_p / 100, 2)
                            if max_p: max_p = round(max_p / 100, 2)
                            if fqp_p: fqp_p = round(fqp_p / 100, 2)
                            
                            records.append((target_date_str, current_cat, item_id, item_name, min_p, max_p, fqp_p, None, None))

            if records and has_real_data:
                return records, target_date_str

        except Exception as e:
            print(f"      [AMIS] Error on {target_date_str}: {e}")

    return [], None

def run_amis_scraper(scrape_date):
    print("\n--- STARTING AMIS SCRAPER (Strict Checks + Unit Conversion) ---")
    try:
        print("   [AMIS] Fetching base URLs...")
        session.get(AMIS_BASE_URL, headers=get_standard_headers(), timeout=30)
        response = session.get(AMIS_CITIES_URL, headers=get_standard_headers(), timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")
        
        target_cities = []
        links = soup.find_all("a", href=lambda h: h and "ViewPrices.aspx" in h)
        for link in links:
            raw_name = link.get_text(strip=True)
            if get_standard_city(raw_name) in TARGET_CITIES_NORMALIZED:
                target_cities.append({
                    'name': raw_name, 
                    'url': urllib.parse.urljoin(AMIS_BASE_URL, link.get('href'))
                })
        print(f"   [AMIS] Found {len(target_cities)} matching cities.")
    except Exception as e:
        print(f"[AMIS] Failed to fetch AMIS cities: {e}")
        return

    total_added = 0
    for i, city in enumerate(target_cities, start=1):
        print(f"[{i}/{len(target_cities)}] AMIS: Processing {city['name']}...")
        records, found_date = scrape_amis_city_data(city, scrape_date)
        
        if records:
            save_to_db(city['name'], records, "amisprizescrape")
            total_added += len(records)
            print(f"    [AMIS] Found data for {found_date}. Saved {len(records)} items.")
        else:
            print(f"    [AMIS] No data available for the last 3 days.")

        time.sleep(random.uniform(2, 4))
        if i % 10 == 0:
            print("    [AMIS] Anti-Bot Cooldown active. Resting...")
            time.sleep(random.uniform(5, 10))

    print(f"[AMIS] Done! Total records collected: {total_added}")

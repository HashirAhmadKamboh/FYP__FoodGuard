import urllib.parse
import re
import requests
from bs4 import BeautifulSoup
from .config import PCCMD_URL, TARGET_CITIES_NORMALIZED, get_standard_city
from .db_helper import save_to_db

def clean_price_val(t):
    if not t: return None
    v = re.sub(r'[^\d.]', '', t.strip())
    return float(v) if v else None

def run_pccmd_scraper(scrape_date):
    print("\n--- STARTING PCCMD SCRAPER (Eggs, Chicken, Atta via Proxy) ---")
    
    encoded_url = urllib.parse.quote(PCCMD_URL)
    proxies = [
        ("CodeTabs Proxy", f"https://api.codetabs.com/v1/proxy?quest={PCCMD_URL}"),
        ("AllOrigins Proxy", f"https://api.allorigins.win/get?url={encoded_url}")
    ]
    
    html_content = None

    for proxy_name, proxy_url in proxies:
        print(f"   [PCCMD] Trying to bounce through: {proxy_name}...")
        try:
            response = requests.get(proxy_url, timeout=40)
            response.raise_for_status()
            
            if "allorigins" in proxy_url:
                data = response.json()
                html_content = data.get("contents", "")
            else:
                html_content = response.text
                
            if html_content and "dataTable" in html_content:
                print(f"   [PCCMD] SUCCESS! {proxy_name} bypassed the block!")
                break
            else:
                print(f"   [PCCMD] {proxy_name} connected, but data table was missing.")
                html_content = None
                
        except Exception as e:
            print(f"   [PCCMD] {proxy_name} Failed: {e}")

    if not html_content:
        print("[PCCMD] All proxies failed to fetch PCCMD data.")
        return

    try:
        print("   [PCCMD] Parsing HTML table...")
        soup = BeautifulSoup(html_content, "html.parser")
        table = soup.find("table", {"id": "dataTable"})
        
        if not table:
            print("[PCCMD] Could not find the table with id 'dataTable' in the HTML.")
            return

        header_cols = [th.get_text(strip=True) for th in table.find("thead").find_all("th")]
        city_records = {} 
        
        for row in table.find("tbody").find_all("tr"):
            cols = [td.get_text(strip=True) for td in row.find_all("td")]
            if len(cols) == len(header_cols):
                district = cols[2]
                norm_district = get_standard_city(district)
                
                if norm_district not in TARGET_CITIES_NORMALIZED:
                    continue 
                
                if norm_district not in city_records:
                    city_records[norm_district] = []

                for i in range(3, len(header_cols)):
                    item_name = header_cols[i]
                    price_val = clean_price_val(cols[i])
                    
                    if price_val in [0, 0.0]:
                        price_val = None
                        
                    current_item_id = 133 + (i - 3)
                    
                    record = (scrape_date, "PCCMD Items", current_item_id, item_name, price_val, price_val, price_val, None, None)
                    city_records[norm_district].append(record)

        total_pccmd = 0
        for city, records in city_records.items():
            save_to_db(city, records, "pccmdprizescrape")
            total_pccmd += len(records)
            print(f"    [PCCMD] Saved {len(records)} items for {city}.")
            
        print(f"[PCCMD] Done! Total records: {total_pccmd}")

    except Exception as e:
        print(f"[PCCMD] Failed to parse data: {e}")

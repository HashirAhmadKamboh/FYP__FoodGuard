import time
import re
from bs4 import BeautifulSoup
from .config import PSBA_URL, TARGET_CITIES_NORMALIZED, get_standard_city
from .db_helper import save_to_db

def run_psba_scraper(scrape_date):
    print("\n--- STARTING PSBA SCRAPER (Priority 1: Selenium JS Bypass) ---")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
    except ImportError:
        print("[PSBA] ERROR: Selenium is not installed.")
        return

    print("   [PSBA] Launching Headless Browser (1080p Resolution)...")
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--window-size=1920,1080") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("   [PSBA] Connecting to PSBA_URL...")
        driver.get(PSBA_URL)
        
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'w-full text-left')]"))
        )
        print("   [PSBA] JS Executed. Page loaded successfully.")
        
        district_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'w-full text-left')]")
        print(f"   [PSBA] Found {len(district_buttons)} districts on the dashboard.")
        
        total_psba = 0
        num_districts = len(district_buttons)
        
        for i in range(num_districts):
            buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'w-full text-left')]")
            if i >= len(buttons): break
            btn = buttons[i]
            
            raw_city = btn.text.strip()
            norm_city = get_standard_city(raw_city)
            
            if norm_city not in TARGET_CITIES_NORMALIZED:
                continue
                
            try:
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(1.5)  
                
                city_records = []
                tabs = driver.find_elements(By.XPATH, "//div[@role='tablist']/button[@role='tab']")
                
                for tab in tabs:
                    tab_name = tab.text.strip()
                    driver.execute_script("arguments[0].click();", tab)
                    time.sleep(0.8)  
                    
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    table_body = soup.find("tbody")
                    
                    if not table_body:
                        continue
                        
                    rows = table_body.find_all("tr")
                    
                    for row in rows:
                        cols = row.find_all("td")
                        if len(cols) >= 2:
                            item_name = cols[0].get_text(strip=True)
                            
                            # Clean string values safely
                            raw_val = cols[1].get_text(strip=True)
                            psba_val = re.sub(r'[^\d.]', '', raw_val)
                            
                            # CRITICAL FIX: Strip any broken leading/trailing dots (e.g. '.345.00' -> '345.00')
                            psba_val = psba_val.strip('.')
                            
                            psba_price = float(psba_val) if psba_val else None
                            dc_price = None  
                            
                            if item_name and psba_price:
                                city_records.append((scrape_date, f"PSBA {tab_name}", 999, item_name, None, None, None, dc_price, psba_price))
                
                if city_records:
                    save_to_db(norm_city, city_records, "psbaprizescrape")
                    total_psba += len(city_records)
                    print(f"      [PSBA] Saved {len(city_records)} items for {raw_city}.")
                else:
                    print(f"      [PSBA] No items parsed for {raw_city}.")
                    
            except Exception as e:
                print(f"      [PSBA] Skipping {raw_city} due to interaction error: {e}")
 
        print(f"[PSBA] Done! Total records scraped: {total_psba}")
        driver.quit()

    except Exception as e:
        print(f"[PSBA] Failed to scrape: {e}")
        try: driver.quit() 
        except: pass

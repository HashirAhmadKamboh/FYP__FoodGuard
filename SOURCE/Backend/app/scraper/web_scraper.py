"""
Ultimate Food Guard - Master Web Scraper Coordinator
- Imports scraping modules (PSBA, PCCMD, AMIS)
- Orchestrates fresh daily scrapes
"""

from datetime import datetime
from .db_helper import clear_old_data, check_if_scraping_needed
from .psba_scraper import run_psba_scraper
from .pccmd_scraper import run_pccmd_scraper
from .amis_scraper import run_amis_scraper

def run_all_scrapers():
    print("\nUltimate Price Tracker: Background Process Starting...")
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    clear_old_data()
    run_psba_scraper(current_date)
    run_pccmd_scraper(current_date)
    run_amis_scraper(current_date)
    
    print("\nAll Scraping Complete! Data successfully merged into database.")

if __name__ == "__main__":
    run_all_scrapers()
import random
import re

AMIS_BASE_URL = "http://www.amis.pk/"
AMIS_CITIES_URL = "http://www.amis.pk/BrowsePrices.aspx?searchType=1"
PCCMD_URL = "https://pccmdpunjab.gov.pk/Commodities/Prices/"
PSBA_URL = "https://psba.gop.pk/daily-rate-comparison"

TARGET_CITIES_NORMALIZED = [
    "attock", "jhelum", "pakpattan", "bahawalnagar", "kasur", "rahimyarkhan", 
    "rajanpur", "bahawalpur", "khanewal", "rawalpindi", "bhakkar", 
    "sahiwal", "khushab", "chakwal", "sargodha", "lahore", "dgkhan", 
    "sheikhupura", "faisalabad", "layyah", "mianwali", "sialkot", 
    "gujranwala", "multan", "ttsingh", "lodhran", "gujrat", 
    "vehari", "muzaffargarh", "nankana", "jhang", "narowal", 
    "mandibahaudin", "hafizabad", "okara", "chiniot",
    "wazirabad", "murree", "talagang", "taunsasharif", "kotadu" 
]

CITY_MAPPING = {
    "deraghazikhan": "dgkhan",
    "tunsa": "taunsasharif",
    "kotaddu": "kotadu",
    "tobateksingh": "ttsingh",
    "mandibahauddin": "mandibahaudin",
    "nankanasahib": "nankana",
    "bhakhar": "bhakkar",
    "d.g. khan": "dgkhan" 
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
]

def normalize_name(name):
    return re.sub(r'[^a-zA-Z]', '', name).lower()

def get_standard_city(name):
    norm = normalize_name(name)
    return CITY_MAPPING.get(norm, norm)

def get_standard_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive"
    }

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import threading
import os

# Import routers
from app.modules.predict.routers import router as predict_router
from app.modules.commodities.routers import router as commodities_router
from app.modules.prices.routers import router as prices_router
from app.account.routers import router as account_router

# Import scraper functions
from app.scraper.web_scraper import run_all_scrapers, check_if_scraping_needed

# Import database seeder
from see_data import seed_ingredients

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Food Guard API & Background Scheduler...")
    
    # Create static predictions directory if it does not exist
    os.makedirs("static/predictions", exist_ok=True)
    
    # Nutrition seed check
    await seed_ingredients()
    
    # Scraper smart check
    print("Checking if database needs fresh scraped data...")
    if check_if_scraping_needed():
        print("Data is missing or old! Starting scraper in the background...")
        threading.Thread(target=run_all_scrapers, daemon=True).start()
    else:
        print("Database already has fresh price data for today. Skipping scrape.")

    # Keep the schedule to automatically refresh prices every day at 9:00 PM
    scheduler.add_job(run_all_scrapers, 'cron', hour=21, minute=0)
    scheduler.start()
    
    yield
    
    print("Shutting down...")
    scheduler.shutdown()

# Create static predictions directory if it does not exist
os.makedirs("static/predictions", exist_ok=True)

app = FastAPI(title="Food Guard API", version="1.0.0", lifespan=lifespan)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Register all API endpoints
app.include_router(predict_router)
app.include_router(commodities_router)
app.include_router(prices_router)
app.include_router(account_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Food Guard Backend API"}
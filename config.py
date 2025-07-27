from pymongo import MongoClient
import os

MONGODB_URI = os.getenv("MONGODB_URI", "")

# MongoDB se credentials fetch karna
mongo_client = MongoClient(MONGODB_URI)
db = mongo_client["tgconfig"]
veriables = db["affiliaters"].find_one() or {}

class Config:
    BOT_TOKEN = os.environ.get('BOT_TOKEN', '') or veriables.get("BOT_TOKEN", '')
    CHANNEL_ID = os.environ.get('CHANNEL_ID', '-1001731540969').split(',') # example: '-1001731540969,-1001731540969'
    PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN', '') or veriables.get("PAGE_ACCESS_TOKEN", '')
    PAGE_ID = os.environ.get('PAGE_ID', '') or veriables.get("PAGE_ID", '')
    API_EARNING_KEY = os.environ.get('API_EARNING_KEY', '') or veriables.get("API_EARNING_KEY", '')
    SCRAPER_API_KEY = os.environ.get('SCRAPER_API_KEY', '') or veriables.get("SCRAPER_API_KEY", '')
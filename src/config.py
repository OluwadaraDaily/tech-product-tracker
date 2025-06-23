# For configuations
import os
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables from .env file
load_dotenv()

# --------------------
# Project Config
# --------------------
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
ENVIRONMENT = os.getenv("ENV", "development")

# --------------------
# Target Site URLs
# --------------------
SCRAPE_TARGETS = {
    "microcenter": "https://www.microcenter.com/search/search_results.aspx?N=4294967288",
    "bh": "https://www.bhphotovideo.com/c/search?N=4294542558"
}

# --------------------
# Headers / Requests
# --------------------
DEFAULT_HEADERS = {
    "User-Agent": os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"),
    "Accept-Language": "en-US,en;q=0.9"
}

REQUEST_TIMEOUT = 10  # seconds
MAX_RETRIES = 3
RETRY_BACKOFF = 2  # seconds (between retries)

# --------------------
# Storage Config
# --------------------
CSV_OUTPUT_DIR = "output"
SQLITE_DB_PATH = "storage/data.db"
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

# --------------------
# Snapshot Saving
# --------------------
SAVE_SNAPSHOTS = True
SNAPSHOT_DIR = "snapshots"

# --------------------
# Price Drop Threshold
# --------------------
PRICE_DROP_THRESHOLD = float(os.getenv("PRICE_DROP_THRESHOLD", "10.0"))  # percent

# --------------------
# Alert Config (Email, Telegram, etc.)
# --------------------
EMAIL_ALERT_ENABLED = os.getenv("EMAIL_ALERT_ENABLED", "false").lower() == "true"
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")

TELEGRAM_ALERT_ENABLED = os.getenv("TELEGRAM_ALERT_ENABLED", "false").lower() == "true"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --------------------
# Scraping Schedule
# --------------------
SCRAPE_INTERVAL = timedelta(hours=24)
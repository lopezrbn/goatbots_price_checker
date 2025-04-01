# config.py
import os
import datetime

# Global constants
MIN_PRICE_THRESHOLD = 1.0       # Price in €
RANGE_TIME = "6m"               # Choose between ["today", "1d", "1w", "1m", "6m"]
PRICE_PERC_SELL_ALERT = 0.75    # 75% of the max price
PRICE_PERC_BUY_ALERT = 0.25     # 25% of the max price

# Define the base directory of your project
DIR_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Define other paths relative to BASE_DIR
DIR_DATA = os.path.join(DIR_BASE, '0_data')
DIR_CONFIG = os.path.join(DIR_BASE, '1_config')
DIR_UTILS = os.path.join(DIR_BASE, '2_utils')
DIR_LOGS = os.path.join(DIR_BASE, '3_logs')

# Define subdirectories
DIR_CARD_DEFINITIONS = os.path.join(DIR_DATA, '0_card_definitions')
DIR_CARD_PRICES = os.path.join(DIR_DATA, '1_card_prices')
DIR_COLLECTION_CARDS = os.path.join(DIR_DATA, "2_collection_cards")
DIR_ALERTS = os.path.join(DIR_DATA, "3_alerts")

# Paths to data files
PATH_EMAIL_CREDENTIALS = os.path.join(DIR_CONFIG, "email_credentials.json")

PATH_CARD_DEFINITIONS = os.path.join(DIR_CARD_DEFINITIONS, 'card-definitions.txt')

PATH_DF_PRICES = os.path.join(DIR_CARD_PRICES, 'df_prices.parquet')

PATH_COLLECTION_CARDS_MTGO = os.path.join(DIR_COLLECTION_CARDS, "collection_cards.dek")
PATH_COLLECTION_CARDS_JSON = os.path.join(DIR_COLLECTION_CARDS, "collection_cards.json")
PATH_WATCHLIST_CARDS = os.path.join(DIR_COLLECTION_CARDS, "watchlist_cards.json")

PATH_SELL_ALERTS = os.path.join(DIR_ALERTS, "sell_alerts.json")
PATH_BUY_ALERTS = os.path.join(DIR_ALERTS, "buy_alerts.json")
PATH_WATCHLIST_ALERTS = os.path.join(DIR_ALERTS, "watchlist_alerts.json")

# Define URLs
URL_CARD_DEFINITIONS = "https://www.goatbots.com/download/prices/card-definitions.zip"
URL_LAST_DAY_PRICES = "https://www.goatbots.com/download/prices/price-history.zip"
URL_YTD_PRICES = f"https://www.goatbots.com/download/prices/price-history-{datetime.datetime.now().year}.zip"
URL_LAST_YEAR_PRICES = f"https://www.goatbots.com/download/prices/price-history-{datetime.datetime.now().year - 1}.zip"
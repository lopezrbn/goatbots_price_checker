# config.py
import os
import datetime

# Define the base directory of your project
DIR_BASE = os.path.dirname(os.path.abspath(__file__))

# Define other paths relative to BASE_DIR
DIR_DATA = os.path.join(DIR_BASE, '0_data')
DIR_UTILS = os.path.join(DIR_BASE, '1_utils')
DIR_LOGS = os.path.join(DIR_BASE, '2_logs')

# Define subdirectories
DIR_CARD_DEFINITIONS = os.path.join(DIR_DATA, '0_card_definitions')
DIR_CARD_PRICES = os.path.join(DIR_DATA, '1_card_prices')
DIR_FAV_CARDS = os.path.join(DIR_DATA, "2_fav_cards")
DIR_ALERTS = os.path.join(DIR_DATA, "3_alerts")

# Paths to data files
PATH_EMAIL_CREDENTIALS = os.path.join(DIR_BASE, "email_credentials.json")

PATH_CARD_DEFINITIONS = os.path.join(DIR_CARD_DEFINITIONS, 'card-definitions.txt')

PATH_DF_PRICES = os.path.join(DIR_CARD_PRICES, 'df_prices.parquet')

PATH_FAV_CARDS = os.path.join(DIR_FAV_CARDS, "fav_cards.json")

PATH_SELL_ALERTS = os.path.join(DIR_ALERTS, "sell_alerts.json")
PATH_BUY_ALERTS = os.path.join(DIR_ALERTS, "buy_alerts.json")

# Define URLs
URL_CARD_DEFINITIONS = "https://www.goatbots.com/download/card-definitions.zip"
URL_LAST_DAY_PRICES = "https://www.goatbots.com/download/prices/price-history.zip"
URL_YTD_PRICES = f"https://www.goatbots.com/download/prices/price-history-{datetime.datetime.now().year}.zip"
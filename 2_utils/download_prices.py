import config
import functions as fun
from datetime import datetime, timedelta
import os

def _generate_price_filenames(year):
    start_date = datetime(year, 1, 1)
    if year == datetime.now().year:
        end_date = datetime.today() - timedelta(days=1)
    else:
        end_date = datetime(year, 12, 31)
    delta = timedelta(days=1)

    filenames = []
    while start_date <= end_date:
        filenames.append(start_date.strftime("price-history-%Y-%m-%d.txt"))
        start_date += delta
    
    return filenames

def _download_all_year_prices(year):
    card_prices_dates = os.listdir(config.DIR_CARD_PRICES)
    for filename in _generate_price_filenames(year):
        if filename not in card_prices_dates:
            print(f"\t\tFile {filename} not found. Downloading...")
            fun._download_zip_file(url=config.URL_YTD_PRICES, extract_path=config.DIR_CARD_PRICES)
            break
    return None

def download_prices(verbose=False):

    if verbose:
        print("Downloading prices...")

    # Download last day prices
    fun._download_zip_file(url=config.URL_LAST_DAY_PRICES, extract_path=config.DIR_CARD_PRICES)

    # Download YTD in case some last day prices are missing
    current_year = datetime.now().year
    _download_all_year_prices(current_year)

    # Download last year prices
    last_year = current_year - 1
    _download_all_year_prices(last_year)

    # Read the prices and generate a DataFrame
    fun._generate_df_prices(verbose=False)
    
    if verbose:
        print("\tPrices downloaded successfully.")


if __name__ == "__main__":
    download_prices()
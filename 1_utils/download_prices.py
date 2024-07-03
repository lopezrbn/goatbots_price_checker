import config
import functions as fun


def download_prices(verbose=False):

    if verbose:
        print("Downloading prices...")

    # Download last day prices
    fun._download_zip_file(url=config.URL_LAST_DAY_PRICES, extract_path=config.DIR_CARD_PRICES)

    # Download YTD prices in case some last day prices are missing
    fun._download_zip_file(url=config.URL_YTD_PRICES, extract_path=config.DIR_CARD_PRICES)

    # Read the prices and generate a DataFrame
    fun._generate_df_prices(verbose=False)
    
    if verbose:
        print("\tPrices downloaded successfully.")


if __name__ == "__main__":
    download_prices()
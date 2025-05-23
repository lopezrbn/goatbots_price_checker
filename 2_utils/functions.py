import config
import os
import pandas as pd
import json
import matplotlib.pyplot as plt
import requests
import zipfile
import io


# Declare df_prices as a global variable so I don't have to pass it as an argument to every function
# Initialization with real values will be done at the end of the file, after the functions are defined
global df_prices
df_prices = None


def input_card():
    cardID = input("Enter card ID: ")
    cardID = cardID if cardID != "" else None
    name = input("Enter card name: ")
    name = name.lower() if name != "" else None
    cardset = input("Enter card set: ")
    cardset = cardset.lower() if cardset != "" else None
    foil = None
    while foil not in ["0", "1", ""]:
        foil = input("Enter foil (0/1): ")
        if foil not in ["0", "1", ""]:
            print("Invalid input. Please enter 0, 1 or leave it empty.")
    foil = int(foil) if foil != "" else None
    return cardID, name, cardset, foil


def _complete_card_info(cardID=None, name=None, cardset=None, foil=None):
    if cardID is not None:
        cardID = [str(cardID)]
        df_prices_filtered = df_prices.loc[cardID]
        name = df_prices_filtered.loc[cardID, "name"].values[0]
        cardset = df_prices_filtered.loc[cardID, "cardset"].values[0]
        foil = int(df_prices_filtered.loc[cardID, "foil"].values[0])
    else:
        condition = True
        if name is not None:
            condition &= (df_prices['name'].str.lower() == name)
        if cardset is not None:
            condition &= (df_prices['cardset'].str.lower() == cardset)
        if foil is not None:
            condition &= (df_prices['foil'] == foil)
        df_prices_filtered = df_prices.loc[condition]
        cardID = df_prices_filtered.index
    return cardID, name, cardset, foil


def search_card(cardID=None, name=None, cardset=None, foil=None):
    # Get the card information missing from the function call
    cardID, name, cardset, foil = _complete_card_info(cardID, name, cardset, foil)
    return df_prices.loc[cardID, df_prices.columns[[0,1,2,3,-1]]]


def price_check(cardID=None, name=None, cardset=None, foil=None, range_time="3m", verbose=False):
    # Get the card information missing from the function call
    cardID, name, cardset, foil = _complete_card_info(cardID, name, cardset, foil)
    # Filter DataFrame based on provided parameters
    df_prices_filtered = df_prices.loc[cardID]
    df_prices_filtered = df_prices_filtered.drop(['name', 'cardset', 'rarity', 'foil'], axis=1, errors='ignore')
    # Get the price today
    price_today = float(df_prices_filtered.iloc[:, -1].values[0])
    # Initialize the prices dictionary
    prices = {}
    # Define the range times
    range_times_words = ["today", "1d", "1w", "1m", "3m", "6m"]
    range_times = [1, 2, 7, 30, 90, 180]
    # Get the prices for each range
    for range_time_word, range_time in zip(range_times_words, range_times):
        prices[range_time_word] = {}
        df_temp = df_prices_filtered.iloc[:, -range_time:]
        prices[range_time_word]["day"] = float(df_temp.iloc[:, -range_time].values[0])
        # print(f"Price today: {price_today}")
        # print(f"Price {range_time_word} day: {prices[range_time_word]['day']}")
        prices[range_time_word]["delta"] = ((price_today - prices[range_time_word]["day"]) / prices[range_time_word]["day"]) if prices[range_time_word]["day"] != 0 else 0.0
        prices[range_time_word]["delta"] = round(prices[range_time_word]["delta"], 2)
        # print(prices[range_time_word]["delta"])
        prices[range_time_word]["min"] = float(df_temp.min().min())
        prices[range_time_word]["max"] = float(df_temp.max().max())
        prices[range_time_word]["today_vs_range"] = (price_today - prices[range_time_word]["min"]) / (prices[range_time_word]["max"] - prices[range_time_word]["min"]) if prices[range_time_word]["max"] != prices[range_time_word]["min"] else 0.0
        prices[range_time_word]["today_vs_range"] = round(prices[range_time_word]["today_vs_range"], 2)

    if verbose:
        print(f"{cardID[0]} - {name.title()} - {cardset.upper()} - {f'Foil' if foil else 'Non-foil'}")
        print(f"Price yesterday: {price_today}")

    return prices


def plot_card_prices(cardID=None, name=None, cardset=None, foil=None):
    # Get the card information missing from the function call
    cardID, name, cardset, foil = _complete_card_info(cardID, name, cardset, foil)
    # Filter DataFrame based on provided parameters
    df_prices_filtered = df_prices.loc[cardID]
    display(df_prices_filtered.iloc[:, [0,1,2,3]])
    # Drop unnecessary columns
    df_prices_filtered = df_prices_filtered.drop(['name', 'cardset', 'rarity', 'foil'], axis=1, errors='ignore')
    # Plot setup
    plt.figure(figsize=(8,6))
    # Iterate over each row to plot
    for index, row in df_prices_filtered.iterrows():
        dates = pd.to_datetime(row.index, format='%Y%m%d')
        prices = row.values
        plt.plot(dates, prices, marker='.', linestyle='-', label=f'ID {index}')
    # Plot formatting
    plt.title("Price over time" + (f" for {name} ({cardset})" if name and cardset else ""))
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()


def _download_zip_file(url, extract_path=config.DIR_BASE, verbose=False):
    # Download a zip file
    r = requests.get(url)
    if r.status_code == 200:
        # Use BytesIO for the zip file content
        zip_file = io.BytesIO(r.content)
        # Open the zip file
        with zipfile.ZipFile(zip_file) as z:
            # Extract all files in the zip
            z.extractall(extract_path)  # Specify your extraction path
            if verbose:
                # Print confirmation message with number of files extracted
                print(f"\tExtracted {len(z.namelist())} files from the zip file.")
    else:
        print("Failed to download the file.")


def _generate_df_prices(verbose=False):
    # Declare df_prices as global within the scope of the function so the modifications made are kept
    global df_prices
    # Load card definitions
    with open(config.PATH_CARD_DEFINITIONS, 'r') as f:
        df_prices = pd.read_json(f, orient="index")
    # Load card prices and merge them with the card definitions
    prices_files = os.listdir(config.DIR_CARD_PRICES)
    prices_files.sort()
    for price in prices_files:
        if price.endswith(".txt"):
            date = price.split("price-history-")[1].split(".txt")[0].replace("-", "")
            df_prices = pd.merge(
                left=df_prices,
                right=pd.read_json(os.path.join(config.DIR_CARD_PRICES, price), orient="index").rename(columns={0: date}),
                how="left",
                left_index=True,
                right_index=True)
    # Sort the dataframe by index
    df_prices = df_prices.sort_index()
    # Convert the index to string
    df_prices.index = df_prices.index.astype(str)
    if verbose:
        print("\tdf_prices created")
    # Save the prices dataframe
    df_prices.to_parquet(config.PATH_DF_PRICES)
    if verbose:
        print("\tdf_prices saved as parquet")

    return df_prices


def add_card_to_collection(cardID=None, name=None, cardset=None, foil=None):
    # Get the card information missing from the function call
    cardID, name, cardset, foil = _complete_card_info(cardID, name, cardset, foil)
    # In case of multiple card IDs, take the first one
    cardID = cardID[0]
    # Load the favorite cards
    if not os.path.exists(config.PATH_COLLECTION_CARDS_JSON):
        with open(config.PATH_COLLECTION_CARDS_JSON, 'w') as f:
            fav_cards = {}
            json.dump(fav_cards, f)
    else:
        with open(config.PATH_COLLECTION_CARDS_JSON, 'r') as f:
            fav_cards = json.load(f)
    # Add the card to the favorite cards
    fav_cards[cardID] = {"name": name, "cardset": cardset, "foil": foil}
    # Save the favorite cards
    with open(config.PATH_COLLECTION_CARDS_JSON, 'w') as f:
        json.dump(fav_cards, f, indent=4, sort_keys=True)
    return fav_cards


def add_card_to_watchlist(cardID=None, name=None, cardset=None, foil=None):
    # Get the card information missing from the function call
    cardID, name, cardset, foil = _complete_card_info(cardID, name, cardset, foil)
    # In case of multiple card IDs, take the first one
    cardID = cardID[0]
    # Load the watchlist cards
    if not os.path.exists(config.PATH_WATCHLIST_CARDS):
        with open(config.PATH_WATCHLIST_CARDS, 'w') as f:
            watchlist_cards = {}
            json.dump(watchlist_cards, f)
    else:
        with open(config.PATH_WATCHLIST_CARDS, 'r') as f:
            watchlist_cards = json.load(f)
    # Add the card to the watchlist cards
    watchlist_cards[cardID] = {"name": name, "cardset": cardset, "foil": foil}
    # Save the watchlist cards
    with open(config.PATH_WATCHLIST_CARDS, 'w') as f:
        json.dump(watchlist_cards, f, indent=4, sort_keys=True)
    return watchlist_cards


# Initialize df_prices with real values
if not os.path.exists(config.PATH_CARD_DEFINITIONS):
    pass
else:
    if not os.path.exists(config.PATH_DF_PRICES):
        df_prices = _generate_df_prices(verbose=True)
    else:
        df_prices = pd.read_parquet(config.PATH_DF_PRICES)


if __name__ == "__main__":
    pass
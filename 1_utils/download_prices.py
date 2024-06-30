import pandas as pd
import requests
import zipfile
import io
import os
import json


PATH_DATA_FOLDER = os.path.join("0_data")
PATH_CARD_DEFINITIONS = os.path.join(PATH_DATA_FOLDER, "0_card_definitions", "card-definitions.txt")
PATH_CARD_PRICES = os.path.join(PATH_DATA_FOLDER, "1_card_prices")
PATH_DF_FINAL = os.path.join(PATH_DATA_FOLDER, "2_df_final", "df.parquet")
URL_LAST_DAY_PRICES = "https://www.goatbots.com/download/price-history.zip"
URL_YTD_PRICES = f"https://www.goatbots.com/download/price-history-{pd.Timestamp.now().year}.zip"


def generate_df(
    path_card_definitions = PATH_CARD_DEFINITIONS,
    path_card_prices = PATH_CARD_PRICES
):
    print("Generating DataFrame...")
    # Load card definitions
    with open(path_card_definitions, 'r') as f:
        card_definitions = json.load(f)
    df = pd.DataFrame.from_dict(card_definitions, orient='index')
    
    # Load card prices
    filelist = os.listdir(path_card_prices)
    filelist.sort()
    for file in filelist:
        final_path = os.path.join(path_card_prices, file)
        with open(final_path, 'r') as f:
            prices = json.load(f)
        date = file.split("price-history-")[1].split(".txt")[0].replace("-", "")
        prices = pd.DataFrame.from_dict(prices, orient='index', columns=[date])
        df = df.merge(prices, left_index=True, right_index=True)
    
    df = df.sort_index()
    print("\tDataFrame generated successfully.")

    return df


def download_zip_files(url):
    # Download the zip file
    r = requests.get(url)
    if r.status_code == 200:
        # Use BytesIO for the zip file content
        zip_file = io.BytesIO(r.content)
        # Open the zip file
        with zipfile.ZipFile(zip_file) as z:
            # Extract all files in the zip
            z.extractall(PATH_CARD_PRICES)  # Specify your extraction path
            # Print confirmation message with number of files extracted
            print(f"\tExtracted {len(z.namelist())} files from the zip file.")
    else:
        print("Failed to download the file.")


# Download last day prices
print("Downloading last day prices...")
download_zip_files(URL_LAST_DAY_PRICES)

# Download YTD prices in case some last day prices are missing
print("Downloading YTD prices...")
download_zip_files(URL_YTD_PRICES)

# Read the prices and generate a DataFrame
df = generate_df()

# Save DataFrame to parquet
try:
    print("Saving df into parquet...")
    df.to_parquet(PATH_DF_FINAL)
    print("\tdf saved successfully.")
except Exception as e:
    print(f"Failed to save df: {e}")
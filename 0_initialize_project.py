import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '1_config'))
import config
sys.path.append(config.DIR_UTILS)
import functions as fun
from download_prices import download_prices
import os
import pandas as pd

print("Initializing project...")

# Create structure of directories if they don't exist
directories = [directory for directory in dir(config) if directory.startswith('DIR_')]
for directory in directories:
    dir_path = getattr(config, directory)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
print('\tDirectories created')

# Download card definitions
fun._download_zip_file(url=config.URL_CARD_DEFINITIONS, extract_path=config.DIR_CARD_DEFINITIONS)
print("\tCard definitions downloaded")

# Download card prices
download_prices(verbose=False)
print("\tCard prices downloaded")

# Generate df_prices
fun._generate_df_prices(verbose=True)

print("Project initialized successfully!")
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '1_config'))
import config
sys.path.append(config.DIR_UTILS)
import functions as fun


def add_collection_to_fav_cards():
    # Read collection file and add all cards to fav cards
    with open(config.PATH_MTGO_COLLECTION) as f:
        lines = f.readlines()
    # Exclude header and footer
    lines = lines[4:-1]
    ids_list = [line.split('CatID="')[1].split('"')[0] for line in lines]
    # Remove cardId="1"
    ids_list.remove("1")
    for id in ids_list:
        fun.add_fav_card(id)
    print("Collection added to fav cards")


if __name__ == "__main__":
    # Add collection to fav cards
    add_collection_to_fav_cards()
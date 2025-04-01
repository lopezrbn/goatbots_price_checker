import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '1_config'))
import config
sys.path.append(config.DIR_UTILS)
import functions as fun


def import_mtgo_collection():
    # Read collection file and add all cards to it
    with open(config.PATH_COLLECTION_CARDS_MTGO) as f:
        lines = f.readlines()
    # Exclude header and footer
    lines = lines[4:-1]
    ids_list = [line.split('CatID="')[1].split('"')[0] for line in lines]
    # Remove cardId="1"
    ids_list.remove("1")
    for id in ids_list:
        fun.add_card_to_collection(id)
    print("Collection imported from MTGO")


if __name__ == "__main__":
    # Import collection from MTGO
    import_mtgo_collection()
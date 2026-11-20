import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '1_config'))
import config
sys.path.append(config.DIR_UTILS)
import functions as fun


def import_mtgo_collection():
    for card_id in fun.read_mtgo_quantities(config.PATH_COLLECTION_CARDS_MTGO):
        fun.add_card_to_collection(card_id)
    print("Collection imported from MTGO")


if __name__ == "__main__":
    # Import collection from MTGO
    import_mtgo_collection()
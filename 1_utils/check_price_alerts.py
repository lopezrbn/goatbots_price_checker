import pandas as pd
import os
import sys
sys.path.append("1_utils")
import functions as fun
import json


PATH_DATA_FOLDER = os.path.join("/home", "ubuntu", "lopezrbn", "goatbots_price_checker", "0_data")
PATH_DF_FINAL = os.path.join(PATH_DATA_FOLDER, "2_df_final", "df.parquet")
PATH_OTHER_DATA = os.path.join(PATH_DATA_FOLDER, "3_other_data")
PATH_FAV_CARDS = os.path.join(PATH_OTHER_DATA, "fav_cards.json")
PATH_SELL_ALERTS = os.path.join(PATH_OTHER_DATA, "sell_alerts.json")
PATH_BUY_ALERTS = os.path.join(PATH_OTHER_DATA, "buy_alerts.json")


def _check_price_alert(cardID, df, range_time="3m", sell_alert=0.75, buy_alert=0.25, verbose=False):
    if verbose:
        print(f"\tChecking price alert for cardID {cardID}...")
    today_vs_range, price_min_range, price_today, price_max_range = fun.price_analysis(df, cardID=cardID, range_time=range_time)
    if today_vs_range <= buy_alert:
        # BUY ALERT
        if verbose:
            print(f"\t\tBUY ALERT for cardID {cardID}!")
        return (-1, cardID, range_time, today_vs_range, price_min_range, price_today, price_max_range)
    elif today_vs_range >= sell_alert:
        # SELL ALERT
        if verbose:
            print(f"\t\tSELL ALERT for cardID {cardID}!")
        return (1, cardID, range_time, today_vs_range, price_min_range, price_today, price_max_range)
    else:
        # HOLD ALERT
        if verbose:
            print(f"\t\tHOLD ALERT for cardID {cardID}.")
        return (0, cardID, range_time, today_vs_range, price_min_range, price_today, price_max_range)


def check_price_alerts(verbose=False):

    print("Checking price alerts...")

    # Load df with prices
    df = pd.read_parquet(PATH_DF_FINAL)

    # Load fav cards
    with open(PATH_FAV_CARDS, "r") as f:
        fav_cards = json.load(f)

    # Check alerts
    alerts = []
    for cardID in fav_cards.keys():
        alerts.append(_check_price_alert(cardID, df))
    alerts

    # Extract sell and buy alerts
    sell_alerts = {}
    buy_alerts = {}
    for alert in alerts:
        if alert[0] == 1:
            sell_alerts[alert[1]] = {
                "name": fav_cards[alert[1]]["name"],
                "cardset": fav_cards[alert[1]]["cardset"],
                "foil": fav_cards[alert[1]]["foil"],
                "range_time": alert[2],
                "today_vs_range": alert[3],
                "price_min_range": alert[4],
                "price_today": alert[5],
                "price_max_range": alert[6]
            }
        elif alert[0] == -1:
            buy_alerts[alert[1]] = {
                "name": fav_cards[alert[1]]["name"],
                "cardset": fav_cards[alert[1]]["cardset"],
                "foil": fav_cards[alert[1]]["foil"],
                "range_time": alert[2],
                "today_vs_range": alert[3],
                "price_min_range": alert[4],
                "price_today": alert[5],
                "price_max_range": alert[6]
            }

    # Save alerts
    if verbose:
        print("\tSaving alerts...")
    with open(PATH_SELL_ALERTS, "w") as f:
        json.dump(sell_alerts, f)
    with open(PATH_BUY_ALERTS, "w") as f:
        json.dump(buy_alerts, f)
    if verbose:
        print("\t\tAlerts saved successfully.")

    print("\tPrice alerts checked successfully.")


if __name__ == "__main__":
    check_price_alerts()
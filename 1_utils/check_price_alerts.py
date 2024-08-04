import config
import sys
sys.path.append(config.DIR_UTILS)
import functions as fun
import pandas as pd
import json


def _check_price_alert(cardID, range_time="1m", sell_alert=0.75, buy_alert=0.25, verbose=False):
    if verbose:
        print(f"\tChecking price alert for cardID {cardID}...")
    # today_vs_range, price_min_range, price_today, price_max_range = fun.price_check(cardID=cardID, range_time=range_time)
    prices = fun.price_check(cardID=cardID, range_time=range_time)
    today_vs_range = prices[range_time]["today_vs_range"]

    if today_vs_range <= buy_alert:
        # BUY ALERT
        alert_flag = -1
        if verbose:
            print(f"\t\tBUY ALERT for cardID {cardID}!")
    elif today_vs_range >= sell_alert:
        # SELL ALERT
        alert_flag = 1
        if verbose:
            print(f"\t\tSELL ALERT for cardID {cardID}!")
    else:
        # HOLD ALERT
        alert_flag = 0
        if verbose:
            print(f"\t\tHOLD ALERT for cardID {cardID}.")
    return (alert_flag, cardID, range_time, prices)


def check_price_alerts(range_time="1m", verbose=False):

    print("Checking price alerts...")

    # Load df with prices
    df = pd.read_parquet(config.PATH_DF_PRICES)

    # Load fav cards
    with open(config.PATH_FAV_CARDS, "r") as f:
        fav_cards = json.load(f)

    # Check alerts
    alerts = []
    
    for cardID in fav_cards.keys():
        alerts.append(_check_price_alert(cardID, range_time=range_time))

    # Extract sell and buy alerts
    sell_alerts = {}
    buy_alerts = {}
    for alert in alerts:
        prices = alert[3]
        if prices["today"]["day"] >= 0.1:
            if alert[0] == 1:
                sell_alerts[alert[1]] = {
                    "name": fav_cards[alert[1]]["name"],
                    "cardset": fav_cards[alert[1]]["cardset"],
                    "foil": fav_cards[alert[1]]["foil"],
                    "price": prices["today"]["day"],
                    "Δ1d": prices["1d"]["delta"],
                    "Δ1w": prices["1w"]["delta"],
                    "Δ1m": prices["1m"]["delta"],
                    "Δ3m": prices["3m"]["delta"],
                    "Δ6m": prices["6m"]["delta"],
                    "range_time": alert[2],
                    "%range": prices[range_time]["today_vs_range"],
                    "min_range": prices[range_time]["min"],
                    "max_range": prices[range_time]["max"]
                }
            elif alert[0] == -1:
                buy_alerts[alert[1]] = {
                    "name": fav_cards[alert[1]]["name"],
                    "cardset": fav_cards[alert[1]]["cardset"],
                    "foil": fav_cards[alert[1]]["foil"],
                    "price": prices["today"]["day"],
                    "Δ1d": prices["1d"]["delta"],
                    "Δ1w": prices["1w"]["delta"],
                    "Δ1m": prices["1m"]["delta"],
                    "Δ3m": prices["3m"]["delta"],
                    "Δ6m": prices["6m"]["delta"],
                    "range_time": alert[2],
                    "%range": prices[range_time]["today_vs_range"],
                    "min_range": prices[range_time]["min"],
                    "max_range": prices[range_time]["max"]
                }

    # Save alerts
    if verbose:
        print("\tSaving alerts...")
    with open(config.PATH_SELL_ALERTS, "w") as f:
        json.dump(sell_alerts, f)
    with open(config.PATH_BUY_ALERTS, "w") as f:
        json.dump(buy_alerts, f)
    if verbose:
        print("\t\tAlerts saved successfully.")

    print("\tPrice alerts checked successfully.")


if __name__ == "__main__":
    check_price_alerts()
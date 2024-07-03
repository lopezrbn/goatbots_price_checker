import config
import sys
sys.path.append(config.DIR_UTILS)
from download_prices import download_prices
from check_price_alerts import check_price_alerts
from send_email import send_email
import datetime


def daily_price_alert():
    # print date and time for the log
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # Execute the functions
    download_prices(verbose=True)
    check_price_alerts()
    send_email()
    print("Daily price alert script finished.\n")


if __name__ == "__main__":
    daily_price_alert()
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '1_config'))
import config
sys.path.append(config.DIR_UTILS)
from download_prices import download_prices
from check_price_alerts import check_price_alerts
from send_email import send_email
import datetime


def daily_price_alert(exec_download_prices=True):
    # print date and time for the log
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # Execute the functions
    if exec_download_prices:
        download_prices(verbose=True)
    check_price_alerts(range_time="6m")
    send_email()
    print("Daily price alert script finished.")
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    daily_price_alert()
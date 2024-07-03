import datetime
import sys
sys.path.append("/home/ubuntu/lopezrbn/goatbots_price_checker/1_utils")
from download_prices import download_prices
from check_price_alerts import check_price_alerts
from send_email import send_email

if __name__ == "__main__":
    # print date and time for the log
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # Execute the functions
    download_prices()
    check_price_alerts()
    send_email()
    print("Daily price alert script finished.\n")
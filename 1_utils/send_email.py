import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import os
import pandas as pd


PATH_ROOT = os.path.join("/home", "ubuntu", "lopezrbn", "goatbots_price_checker")
PATH_DATA_FOLDER = os.path.join(PATH_ROOT, "0_data")
PATH_OTHER_DATA = os.path.join(PATH_DATA_FOLDER, "3_other_data")
PATH_SELL_ALERTS = os.path.join(PATH_OTHER_DATA, "sell_alerts.json")
PATH_BUY_ALERTS = os.path.join(PATH_OTHER_DATA, "buy_alerts.json")
PATH_CREDENTIALS = os.path.join(PATH_ROOT, "credentials.json")


def send_email():

    print("Sending email...")

    # Load credentials for the email account
    with open(PATH_CREDENTIALS) as f:
        credentials = json.load(f)
        sender_email = credentials["sender_email"]
        receiver_email = credentials["receiver_email"]
        password = credentials["password"]

    # Load sell and buy alerts
    with open(PATH_SELL_ALERTS) as f:
        sell_alerts = pd.read_json(f, orient="index")
    with open(PATH_BUY_ALERTS) as f:
        buy_alerts = pd.read_json(f, orient="index")

    # Set column "today_vs_range" to percentage
    sell_alerts['today_vs_range'] = sell_alerts['today_vs_range'].map("{:.0%}".format)
    buy_alerts['today_vs_range'] = buy_alerts['today_vs_range'].map("{:.0%}".format)

    # Transform dataframes to html
    sell_alerts_html = sell_alerts.to_html(index=False)
    buy_alerts_html = buy_alerts.to_html(index=False)

    # Create message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Daily Price Update"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Email body
    body = f"""
    <html>
        <head></head>
        <body>
            <p>Here's the daily update on prices...</p>
            <h2>Sell Alerts</h2>
            {sell_alerts_html}
            <h2>Buy Alerts</h2>
            {buy_alerts_html}
        </body>
    </html>
    """
    mime_text = MIMEText(body, "html")
    message.attach(mime_text)

    # Send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("\tEmail sent successfully.")


if __name__ == "__main__":
    send_email()
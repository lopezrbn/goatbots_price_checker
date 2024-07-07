import config
import pandas as pd
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email():

    print("Sending email...")

    # Load credentials for the email account
    with open(config.PATH_EMAIL_CREDENTIALS) as f:
        credentials = json.load(f)
        sender_email = credentials["sender_email"]
        receiver_email = credentials["receiver_email"]
        password = credentials["password"]

    # Load sell and buy alerts
    with open(config.PATH_SELL_ALERTS) as f:
        sell_alerts = pd.read_json(f, orient="index")
    with open(config.PATH_BUY_ALERTS) as f:
        buy_alerts = pd.read_json(f, orient="index")

    # Set columns to percentage
    columns = ["Δ1d", "Δ1w", "Δ1m", "Δ3m", "Δ6m", "%range"]
    for col in columns:
        sell_alerts[col] = sell_alerts[col].map("{:.0%}".format)
        buy_alerts[col] = buy_alerts[col].map("{:.0%}".format)


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
            <p>Here's the daily update on prices:</p>
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
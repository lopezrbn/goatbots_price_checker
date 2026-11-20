import config
from functions import collection_value_report
import pandas as pd
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def _format_collection_change(change):
    if change is None:
        return "Unavailable"
    amount, rate = change
    percentage = "percentage unavailable" if rate is None else f"{rate:+.2%}"
    return f"{amount:+,.2f} TIX ({percentage})"


def send_email():

    print("Sending email...")

    # Set columns to percentage
    columns = ["Δ1d", "Δ1w", "Δ1m", "Δ3m", "Δ6m", "%range"]

    # Load credentials for the email account
    with open(config.PATH_EMAIL_CREDENTIALS) as f:
        credentials = json.load(f)
        sender_email = credentials["sender_email"]
        receiver_email = credentials["receiver_email"]
        password = credentials["password"]

    # Load, sort  and transform df to html for sell alerts
    with open(config.PATH_SELL_ALERTS) as f:
        sell_alerts = pd.read_json(f, orient="index")
    if not sell_alerts.empty:
        sell_alerts = sell_alerts.sort_values(by=["Δ1d", "name", "cardset", "foil"], ascending=[False, True, True, True])
        for col in columns:
            sell_alerts[col] = sell_alerts[col].map("{:.0%}".format)
    sell_alerts_html = sell_alerts.to_html(index=False)

    # Load, sort and transform df to html for buy alerts
    with open(config.PATH_BUY_ALERTS) as f:
        buy_alerts = pd.read_json(f, orient="index")
    if not buy_alerts.empty:
        buy_alerts = buy_alerts.sort_values(by=["Δ1d", "name", "cardset", "foil"], ascending=[True, True, True, True])
        for col in columns:
            buy_alerts[col] = buy_alerts[col].map("{:.0%}".format)
    buy_alerts_html = buy_alerts.to_html(index=False)

    # Load, sort and transform df to html for watchlist alerts
    with open(config.PATH_WATCHLIST_ALERTS) as f:
        watchlist_alerts = pd.read_json(f, orient="index")
    if not watchlist_alerts.empty:
        watchlist_alerts = watchlist_alerts.sort_values(by=["name", "Δ1d", "cardset", "foil"], ascending=[True, True, True, True])
        for col in columns:
            watchlist_alerts[col] = watchlist_alerts[col].map("{:.0%}".format)
    watchlist_alerts_html = watchlist_alerts.to_html(index=False)

    total, unpriced_copies, changes = collection_value_report()
    value_summary = "Unavailable" if total is None else f"{total:,.2f} TIX"
    if unpriced_copies:
        detail = "partial total; " if total is not None else ""
        value_summary += f" ({detail}copies without a price: {unpriced_copies:,})"
    changes_html = "\n".join(
        f"<li>{period}: {_format_collection_change(change)}</li>"
        for period, change in changes.items()
    )

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
            <p><strong>Total collection value:</strong> {value_summary}</p>
            <p><strong>Collection value change</strong> (using the same cards and quantities for each date):</p>
            <ul>{changes_html}</ul>
            <h2>Watchlist Alerts</h2>
            {watchlist_alerts_html}
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
    # with smtplib.SMTP('smtp.office365.com', 587) as server:
        # server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("\tEmail sent successfully.")


if __name__ == "__main__":
    send_email()
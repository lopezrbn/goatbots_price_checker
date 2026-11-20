import importlib
import json
import sys
import tempfile
import unittest
from email import message_from_string, policy
from pathlib import Path
from unittest.mock import patch

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "1_config"))
import config

# Do not load the user's price cache while importing the daily script.
with patch.object(config, "PATH_CARD_DEFINITIONS", ""):
    daily = importlib.import_module("2_daily_price_alert")
    fun = importlib.import_module("functions")


class DailyCollectionValueTests(unittest.TestCase):
    def setUp(self):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        paths = {
            key: Path(temp_dir.name) / filename
            for key, filename in {
                "PATH_COLLECTION_CARDS_JSON": "collection.json",
                "PATH_COLLECTION_CARDS_MTGO": "collection.dek",
                "PATH_WATCHLIST_CARDS": "watchlist.json",
                "PATH_SELL_ALERTS": "sell.json",
                "PATH_BUY_ALERTS": "buy.json",
                "PATH_WATCHLIST_ALERTS": "watchlist_alerts.json",
                "PATH_EMAIL_CREDENTIALS": "email.json",
            }.items()
        }
        self.start_patch(patch.multiple(config, **paths))
        paths["PATH_EMAIL_CREDENTIALS"].write_text(json.dumps({
            "sender_email": "sender@example.com",
            "receiver_email": "receiver@example.com",
            "password": "test-password",
        }))
        self.smtp = self.start_patch(patch("smtplib.SMTP_SSL"))
        dates = pd.date_range(end="2025-01-02", periods=180).strftime("%Y%m%d")
        self.prices = pd.DataFrame(1.0, index=["11", "12", "13", "14", "99"], columns=dates)
        self.prices.insert(0, "name", ["Card 11", "Card 11", "Card 13", "Card 14", "Watchlist only"])
        self.prices.insert(1, "cardset", "TST")
        self.prices.insert(2, "foil", [0, 1, 0, 0, 0])
        self.prices.loc[:, "20250102"] = [0.25, 2.0, 10.0, float("nan"), 1000.0]
        self.start_patch(patch.object(fun, "df_prices", self.prices))

    def start_patch(self, patcher):
        self.addCleanup(patcher.stop)
        return patcher.start()

    def daily_email(self, collection_ids):
        Path(config.PATH_COLLECTION_CARDS_JSON).write_text(json.dumps({
            card_id: {
                "name": f"Card {card_id if card_id != '12' else '11'}",
                "cardset": "TST",
                "foil": card_id == "12",
            }
            for card_id in collection_ids
        }))
        Path(config.PATH_WATCHLIST_CARDS).write_text(json.dumps({
            "99": {"name": "Watchlist only", "cardset": "TST", "foil": False},
        }))

        daily.daily_price_alert(exec_download_prices=False)

        sendmail = self.smtp.return_value.__enter__.return_value.sendmail
        sendmail.assert_called_once()
        message = message_from_string(sendmail.call_args.args[2], policy=policy.default)
        return message.get_body(preferencelist=("html",)).get_content()

    def test_collection_counts_copies_and_reports_missing_prices(self):
        Path(config.PATH_COLLECTION_CARDS_MTGO).write_text(
            '<Deck>'
            '<Cards CatID="11" Quantity="3" Sideboard="false" />'
            '<Cards CatID="11" Quantity="2" Sideboard="true" />'
            '<Cards CatID="12" Quantity="2" />'
            '<Cards CatID="14" Quantity="3" />'
            '<Cards CatID="1" Quantity="1" />'
            '<Cards CatID="99" Quantity="4" />'
            '</Deck>'
        )
        body = self.daily_email(["11", "12", "13", "14", "15"])

        self.assertIn(
            "Total collection value:</strong> 15.25 TIX (partial total; copies without a price: 4)",
            body,
        )
        self.assertIn("Watchlist only", body)
        self.assertIn("<h2>Sell Alerts</h2>", body)
        self.assertIn("Card 13", body)
        self.assertIn("<h2>Buy Alerts</h2>", body)

    def test_collection_without_export_counts_one_copy(self):
        body = self.daily_email(["12"])

        self.assertIn("Total collection value:</strong> 2.00 TIX</p>", body)

    def test_empty_collection_has_zero_value(self):
        body = self.daily_email([])

        self.assertIn("Total collection value:</strong> 0.00 TIX</p>", body)

    def test_unpriced_collection_does_not_show_a_zero_value(self):
        body = self.daily_email(["14"])

        self.assertIn("Total collection value:</strong> Unavailable (copies without a price: 1)", body)

    def test_zero_price_is_not_missing(self):
        self.prices.loc["11", "20250102"] = 0.0
        body = self.daily_email(["11"])

        self.assertIn("Total collection value:</strong> 0.00 TIX</p>", body)

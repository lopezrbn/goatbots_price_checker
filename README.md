# GOATBots Price Checker

Automates the download of **Magic Online** card prices from GOATBots, compares them against your personal collection and a custom watch-list, and e-mails you daily buy/sell recommendations.

---

## Project structure

```
goatbots_price_checker/
├── 0_data/                       # Generated: prices, collection, watch-list…
├── 1_config/                     # Centralised constants & thresholds
├── 2_utils/                      # Helper functions (scraping, logging, e-mail)
├── 3_logs/                       # Generated: execution logs
├── 0_initialize_project.py       # Creates folders and default config files
├── 1_import_mtgo_collection.py   # Imports your MTGO collection .dek file
├── 2_daily_price_alert.py        # Daily task: download prices & send e-mail
├── 3_project_explorer.ipynb      # Jupyter notebook for ad-hoc analysis
├── requirements.txt              # Python dependencies
└── .gitignore / LICENSE
```

---

## Quick-start guide

### 1. Clone the repository

```bash
git clone https://github.com/lopezrbn/goatbots_price_checker.git
cd goatbots_price_checker
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Initialise the project (creates folders & config)

```bash
python 0_initialize_project.py
```

This script:

- Builds `0_data/`, and `3_logs/`
- Creates `email_credentials.json` (see **Configuration** below) if it does not exist
- Stores default thresholds and constants in `1_config/`

### 3. Import your MTGO collection

Save your Magic Online export as `0_data/2_collection_cards/collection_cards.dek`, then run:

```bash
python 1_import_mtgo_collection.py
```

The importer saves the card list as `0_data/2_collection_cards/collection_cards.json`.
Keep the `.dek` file next to it so the daily e-mail can count multiple copies of a card.

### 4. Run the daily price alert

```bash
python 2_daily_price_alert.py
```

- First run: downloads the entire historical price set  
- Subsequent runs: fetches only the missing days, recomputes deltas, and sends an e-mail with:

  - **Collection alerts** (cards you own)
  - **Watch-list alerts** (cards you follow)
  - **Total collection value** in TIX: the latest GOATBots price multiplied by the number of copies of each card you own, then summed. Cards not listed in the `.dek` count as one copy. Cards without a price are excluded from the total, and the e-mail reports how many copies could not be valued.
  - **Collection value changes** over 1 day, 1 week, and 1, 3 and 6 calendar months, in TIX and as a percentage. Comparisons use your current cards and quantities on both dates, not a history of purchases and sales. If either date lacks any prices, the change is unavailable. A zero starting value has no percentage change.

---

## Scheduling the script with `cron`

Edit your crontab with:

```bash
crontab -e
```

Add a daily entry at 08:00 (server local time):

```
0 8 * * * /home/your_user/goatbots_price_checker/.venv/bin/python3 /home/your_user/goatbots_price_checker/2_daily_price_alert.py >> /home/your_user/goatbots_price_checker/3_logs/$(date +\%Y-\%m-\%d)_daily_price_alert.log 2>&1
```

> Tip: use absolute paths in `1_config/` to avoid issues when `cron` runs without your shell’s working directory.

---

## Configuration

### E-mail credentials (`email_credentials.json`)

`0_initialize_project.py` generates a minimal file like:

```json
{
  "sender_email": "your_email@example.com",
  "receiver_email": "your_email@example.com",
  "password": "app-specific-password",
}
```

- Use an app-specific password or an OAuth token if your provider supports it.
- The file is **.gitignored** by default.

---

## Jupyter notebook (`3_project_explorer.ipynb`)

Open the notebook to:

- Explore historical price curves and volatility
- Add or remove cards from your **watch-list** interactively
- Generate custom charts or exports (CSV / Parquet) for a subset of cards

---

## License

This project is released under the **MIT License**. See the `LICENSE` file for details.

---

## Contact

- Rubén López  
- Data Scientist  
- lopezrbn@gmail.com

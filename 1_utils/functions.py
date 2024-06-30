import pandas as pd
import matplotlib.pyplot as plt


def plot_card_prices(df, name=None, cardset=None, foil=None, cardID=None):
    # Filter DataFrame based on provided parameters
    if cardID is not None:
        df_filtered = df[df.index.isin(cardID)]  # Assuming cardID can be a list of IDs
    else:
        condition = True
        if name is not None:
            condition &= (df['name'] == name)
        if cardset is not None:
            condition &= (df['cardset'] == cardset)
        if foil is not None:
            condition &= (df['foil'] == foil)
        df_filtered = df.loc[condition]
    
    # Drop unnecessary columns
    df_filtered = df_filtered.drop(['name', 'cardset', 'rarity', 'foil'], axis=1, errors='ignore')
      
    # Plot setup
    plt.figure(figsize=(6,4))
    
    # Iterate over each row to plot
    for index, row in df_filtered.iterrows():
        dates = pd.to_datetime(row.index, format='%Y%m%d')
        prices = row.values
        
        plt.plot(dates, prices, marker='.', linestyle='-', label=f'ID {index}')
    
    # Plot formatting
    plt.title("Price over time" + (f" for {name} ({cardset})" if name and cardset else ""))
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()


def price_analysis(df, name=None, cardset=None, foil=None, cardID=None):
    
    if cardID is not None:
        df = df.iloc[[cardID]]
    else:
        condition = True
        if name is not None:
            condition &= (df['name'] == name)
        if cardset is not None:
            condition &= (df['cardset'] == cardset)
        if foil is not None:
            condition &= (df['foil'] == foil)
        df = df.loc[condition]
    
    df = df.drop(['name', 'cardset', 'rarity', 'foil'], axis=1, errors='ignore')

    price_today = df.iloc[:, -1].values[0]
    
    price_max = df.max().max()
    price_min = df.min().min()
    today_vs_range_all = (price_today - price_min) / (price_max - price_min) if price_max != price_min else 0
    
    price_max_6m = df.iloc[:, -180:].max().max()
    price_min_6m = df.iloc[:, -180:].min().min()
    today_vs_range_6m = (price_today - price_min_6m) / (price_max_6m - price_min_6m) if price_max_6m != price_min_6m else 0

    price_max_3m = df.iloc[:, -90:].max().max()
    price_min_3m = df.iloc[:, -90:].min().min()
    today_vs_range_3m = (price_today - price_min_3m) / (price_max_3m - price_min_3m) if price_max_3m != price_min_3m else 0

    price_max_1m = df.iloc[:, -30:].max().max()
    price_min_1m = df.iloc[:, -30:].min().min()
    today_vs_range_1m = (price_today - price_min_1m) / (price_max_1m - price_min_1m) if price_max_1m != price_min_1m else 0
    
    price_max_1w = df.iloc[:, -7:].max().max()
    price_min_1w = df.iloc[:, -7:].min().min()
    today_vs_range_1w = (price_today - price_min_1w) / (price_max_1w - price_min_1w) if price_max_1w != price_min_1w else 0

    print(f"Today's price: {price_today}")
    print(f"Today's price vs. 1-week range: {today_vs_range_1w:.2%}, [{price_min_1w:.2f} - {price_today} - {price_max_1w:.2f}]")
    print(f"Today's price vs. 1-month range: {today_vs_range_1m:.2%}, [{price_min_1m:.2f} - {price_today} - {price_max_1m:.2f}]")
    print(f"Today's price vs. 3-month range: {today_vs_range_3m:.2%}, [{price_min_3m:.2f} - {price_today} - {price_max_3m:.2f}]")
    print(f"Today's price vs. 6-month range: {today_vs_range_6m:.2%}, [{price_min_6m:.2f} - {price_today} - {price_max_6m:.2f}]")
    print(f"Today's price vs. all-time range: {today_vs_range_all:.2%}, [{price_min:.2f} - {price_today} - {price_max:.2f}]")


def check_card(df, name):
    return df[df['name'] == name].iloc[:,[0,1,2,3,-1]]
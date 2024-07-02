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


def price_analysis(df, name=None, cardset=None, foil=None, cardID=None, range_time="3m"):
    
    if cardID is not None:
        cardID = str(cardID)
        df = df.loc[[cardID]]
        name = df.loc[cardID, "name"]
        cardset = df.loc[cardID, "cardset"]
        foil = df.loc[cardID, "foil"]
    else:
        condition = True
        if name is not None:
            condition &= (df['name'] == name)
        if cardset is not None:
            condition &= (df['cardset'] == cardset)
        if foil is not None:
            condition &= (df['foil'] == foil)
        df = df.loc[condition]
        cardID = df.index[0]
    
    df = df.drop(['name', 'cardset', 'rarity', 'foil'], axis=1, errors='ignore')

    price_today = float(df.iloc[:, -1].values[0])

    if range_time=="1w":
        range = 7
    elif range_time=="1m":
        range = 30
    elif range_time=="3m":
        range = 90
    elif range_time=="6m":
        range = 180
    else:
        range = 0

    df = df.iloc[:, -range:]
    price_max_range = float(df.max().max())
    price_min_range = float(df.min().min())
    today_vs_range = (price_today - price_min_range) / (price_max_range - price_min_range) if price_max_range != price_min_range else 0.0
    today_vs_range = round(today_vs_range, 2)

    return today_vs_range, price_min_range, price_today, price_max_range


def check_cardname(df, name):
    return df[df['name'] == name].iloc[:,[0,1,2,3,-1]]


def check_cardID(df, cardID):
    cardID = str(cardID)
    return df.loc[[cardID], df.columns[[0,1,2,3,-1]]]
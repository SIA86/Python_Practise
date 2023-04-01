import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
import os

TRAILING_STOP = False

""" def conditions(data: pd.DataFrame, current: int) -> bool:
    
    condition_to_buy = all(
    data['Open'] - data['Close']

    )
    """

def get_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path) #read data from csv
    df = df.dropna()
    #convert <DATE> and <TIME> columns to datetime format="%Y%m%d%H%M%S"
    df['<DATE>'] = df['<DATE>'].apply(lambda x: str(x))
    df['<TIME>'] = df['<TIME>'].apply(lambda x: str(x) if x > 0 else "000000")
    df['<DATE>'] = df['<DATE>'] + df['<TIME>']
    df['<DATE>'] = pd.to_datetime(df['<DATE>'], format="%Y%m%d%H%M%S")
    #rename columns for mplfinance format
    df = df.rename(columns={'<DATE>': 'Date',
                            '<OPEN>': 'Open',
                            '<HIGH>': 'High',
                            '<LOW>': 'Low',
                            '<CLOSE>': 'Close',
                            '<VOL>': 'Volume'}
                        )
    #set index to timestamp object
    df = df.set_index('Date')
    #drop useless columns
    df = df.iloc[:,3:]
    #add special columns with information about candles
    df['Body'] = df['Close'] - df['Open']
    df['Colore'] = df['Body'].apply(lambda x: 'Red' if x < 0 else 'Green' if x > 0 else "Grey")
    df['Body'] = abs(df['Body'])
    df.loc[df['Colore'] == 'Green', 'Up_shadow'] = df['High'] - df['Close']
    df.loc[(df['Colore'] == 'Red') | (df['Colore'] == 'Grey'), 'Up_shadow'] = df['High'] - df['Open']
    df.loc[df['Colore'] == 'Green', 'Down_shadow'] = df['Open'] - df['Low']
    df.loc[(df['Colore'] == 'Red') | (df['Colore'] == 'Grey'), 'Down_shadow'] = df['Close'] - df['Low']
    df['Total'] = df['High'] - df['Low']
    lis = []
    for tic in range(len(df)):
        if tic == 0 or tic == len(df)-1:
            lis.append(np.nan)
        elif df.iloc[tic]['Close'] > df.iloc[tic-1]['Close'] and df.iloc[tic]['Close'] > df.iloc[tic+1]['Close']:
            lis.append('max')
        elif df.iloc[tic]['Close'] < df.iloc[tic-1]['Close'] and df.iloc[tic]['Close'] < df.iloc[tic+1]['Close']:
            lis.append('min')
        else:
            lis.append(np.nan)
    df['Local_min_max'] = lis        
    return df


def plot_chart(data: pd.DataFrame):
    pass


def test_algorythm(data: pd.DataFrame) -> float:
    buy_orders = []
    sell_orders = []
    bought = False
    sold = False
    
    for candle in range(data.shape[0]):
        if not bought and not sold:
            if condition_to_buy:
                buy_price = data.iloc[candle+1]['Open'] #open price of the next candle
                buy_orders.append(buy_price)
                sell_orders.append(np.nan)
                bought = True
                stop_loss = min([data.iloc[x, 'Low'] for x in range(candle-10, candle+1)]) #local min low price of 10 candles before and current
                take_profit = max(max([data.iloc[x, 'Close'] for x in range(candle-20, candle)]), buy_price+(buy_price-stop_loss)*2) #local max Close price of 20 candles before or 2*stop_loss
            elif condition_to_sell:
                sell_price = data.iloc[candle]['Close']
                buy_orders.append(np.nan)
                sell_orders.append(sell_price)
                sold = True
            else:
                sell_orders.append(np.nan)
                buy_orders.append(np.nan)

        elif bought:
            if condition_to_sell:
                pass
            elif stop_loss:
                pass
            elif take_profit:
                pass
            else:
                sell_orders.append(np.nan)
                buy_orders.append(np.nan)

        else:
            if condition_to_buy:
                pass
            elif stop_loss:
                pass
            elif take_profit:
                pass
            else:
                sell_orders.append(np.nan)
                buy_orders.append(np.nan)


            
    
                
            
    return deals, buy_orders, sell_orders 

data = get_data('Data\RTS\SPFB.RTS_200115_230322(15).txt')
apdict = ([
    mpf.make_addplot(data.loc[data['Local_min_max']== 'min', data['Close']],type='scatter',markersize=100,marker='^'),
    mpf.make_addplot(data.loc[data['Local_min_max']== 'max', data['Close']],type='scatter',markersize=100,marker='v')
])

mpf.plot(data.iloc[:,:-1],type='candle', volume=False, addplot=apdict)
mpf.show() 



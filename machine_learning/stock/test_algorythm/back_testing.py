import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt

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
    df['Up_shadow'] =0
    df['Down_shadow'] = 0
    return df


def plot_chart(data: pd.DataFrame):
    pass


""" def test_algorythm(data: pd.DataFrame) -> float:
    buy_orders = []
    sell_orders = []
    bought = False
    sold = False
    
    for candle in range(data.shape[0]):
        if not all([bought, sold]):
            if condition_to_buy:
                buy_price = data.iloc[candle+1]['Open'] #open price of the next candle
                buy_orders.append(buy_price)
                sell_orders.append(np.nan)
                bought = True
                stop_loss = min([data.iloc[x]['Low'] for x in range(candle-10, candle+1)]) #local min low price of 10 candles before
                take_profit = max(max[data.iloc[x]['Close'] for x in range(candle-20, candle)], buy_price+(buy_price-stop_loss)*2) #local max Close price of 20 candles before or 2*stop_loss
            if condition_to_sell:
                sell_price = data.iloc[candle]['Close']
                buy_orders.append(np.nan)
                sell_orders.append(sell_price)
                sold = True
        else:


            
    
                
            
    return deals, buy_orders, sell_orders 

data = pd.read_csv('data_with_predictions.csv', index_col=0, parse_dates=True )
deals, buy_signal, sell_signal = chart_monitoring(data)


data['sell'] = sell_signal
data['buy'] = buy_signal
print(deals)

apdict = [
        mpf.make_addplot(data['Predicted_close']),
        mpf.make_addplot(buy_signal,type='scatter',markersize=200,marker='^'),
        mpf.make_addplot(sell_signal,type='scatter',markersize=200,marker='v')
        ]
mpf.plot(data.iloc[:,:-1],type='candle', volume=False, addplot=apdict)
mpf.show() """ 
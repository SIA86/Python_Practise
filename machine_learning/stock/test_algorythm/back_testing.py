import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
import os

TRAILING_STOP = False
WARM_UP_PERIOD = 14

def conditions(data: pd.DataFrame, current: int) -> bool:
    
    condition_to_buy = all([
    data.iloc[current]['Body'] <= 0.4 * data.iloc[current]['Total'],
    data.iloc[current]['Down_shadow'] >= 0.5 * data.iloc[current]['Total']
    #data.iloc[current]['Colore'] == any(['Red','Grey'])
    ])
    condition_to_sell = all([
    data.iloc[current]['Body'] <= 0.4 * data.iloc[current]['Total'],
    data.iloc[current]['Up_shadow'] >= 0.5 * data.iloc[current]['Total']
    #data.iloc[current]['Colore'] == any(['Green','Grey'])
    ])
    return condition_to_buy, condition_to_sell

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
    df = df.iloc[30000:,3:]
    #add special columns with information about candles
    df['Body'] = df['Close'] - df['Open']
    df['Colore'] = df['Body'].apply(lambda x: 'Red' if x < 0 else 'Green' if x > 0 else "Grey")
    df['Body'] = abs(df['Body'])
    df.loc[df['Colore'] == 'Green', 'Up_shadow'] = df['High'] - df['Close']
    df.loc[(df['Colore'] == 'Red') | (df['Colore'] == 'Grey'), 'Up_shadow'] = df['High'] - df['Open']
    df.loc[df['Colore'] == 'Green', 'Down_shadow'] = df['Open'] - df['Low']
    df.loc[(df['Colore'] == 'Red') | (df['Colore'] == 'Grey'), 'Down_shadow'] = df['Close'] - df['Low']
    df['Total'] = df['High'] - df['Low']
    #find local min a max prices
    loc_min_max = []
    for tic in range(len(df)):
        if tic == 0 or tic == len(df)-1:
            loc_min_max.append(np.nan)          
        elif df.iloc[tic]['High'] > df.iloc[tic-1]['High'] and df.iloc[tic]['High'] > df.iloc[tic+1]['Close']:           
            loc_min_max.append('max')
        elif df.iloc[tic]['Low'] < df.iloc[tic-1]['Low'] and df.iloc[tic]['Low'] < df.iloc[tic+1]['Close']:
            loc_min_max.append('min')            
        else:
            loc_min_max.append(np.nan)           
    df['Local_min_max'] = loc_min_max  
    df.loc[df['Local_min_max'] == 'max', 'Local_max_value'] = df['High'] 
    df.loc[df['Local_min_max'] == 'min', 'Local_min_value'] = df['Low']    
    return df


def plot_chart(data: pd.DataFrame):
    pass


def test_algorythm(data: pd.DataFrame) -> float:
    buy_orders = []
    sell_orders = []
    bought = False
    sold = False
    
    for candle in range(WARM_UP_PERIOD, data.shape[0]):
        condition_to_buy, condition_to_sell = conditions(data, candle)
        if not bought and not sold:
            if condition_to_buy:
                
                mpf.plot(data.iloc[:candle,:],type='candle', volume=False)
                mpf.show()  
                
                buy_price = data.iloc[candle+1]['Open'] #open price of the next candle
                buy_orders.append(buy_price)
                sell_orders.append(np.nan)
                bought = True
                stop_loss = min([data.iloc[:candle]['Local_min_value'].dropna().to_list()[-1], data.iloc[candle]['Low']]) 
                take_profit = max([data.iloc[:candle]['Local_max_value'].dropna().to_list()[-1], buy_price+(buy_price-stop_loss)*2]) 
            elif condition_to_sell:
                mpf.plot(data.iloc[:candle,:],type='candle', volume=False)
                mpf.show()

                sell_price = data.iloc[candle+1]['Close']
                buy_orders.append(np.nan)
                sell_orders.append(sell_price)
                sold = True
                stop_loss =  max([data.iloc[:candle]['Local_max_value'].dropna().to_list()[-1], data.iloc[candle]['High']])
                take_profit = min([data.iloc[:candle]['Local_min_value'].dropna().to_list()[-1], sell_price-(stop_loss - sell_price)*2])
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


            
    
                
            
    

data = get_data('Data\RTS\SPFB.RTS_200115_230322(15).txt')
test_algorythm(data)

""" apdict = ([
    mpf.make_addplot(data['Local_min_value'],type='scatter',markersize=100,marker='^'),
    mpf.make_addplot(data['Local_max_value'],type='scatter',markersize=100,marker='v')
])

mpf.plot(data.iloc[:,:-1],type='candle', volume=False, addplot=apdict)
mpf.show() 
 """


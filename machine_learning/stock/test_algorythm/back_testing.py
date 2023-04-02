import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
import os
from stock_indicators import Quote
from stock_indicators import indicators

TRAILING_STOP = False
WARM_UP_PERIOD = 14

def conditions(data: pd.DataFrame, current: int) -> bool:
    
    condition_to_buy = all([
    data.iloc[current]['Up_shadow'] <= 0.1 * data.iloc[current]['Total'],
    data.iloc[current]['Down_shadow'] >= 0.6 * data.iloc[current]['Total'],
    data.iloc[current]['Close'] < data.iloc[current-1]['Close'],
    data.iloc[current]['Close'] < data.iloc[current-2]['Close'], 
    data.iloc[current]['Volume'] >= 1000,
    data.iloc[current]['RSI'] <= 30
    
    ])
    condition_to_sell = all([
    data.iloc[current]['Down_shadow'] <= 0.1 * data.iloc[current]['Total'],
    data.iloc[current]['Up_shadow'] >= 0.6 * data.iloc[current]['Total'],
    data.iloc[current]['Close'] > data.iloc[current-1]['Close'],
    data.iloc[current]['Close'] > data.iloc[current-2]['Close'], 
    data.iloc[current]['Volume'] >= 1000,
    data.iloc[current]['RSI'] >= 70
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
    

    quotes = [
    Quote(d,o,h,l,c,v) 
    for d,o,h,l,c,v 
    in zip( df.index,
            df['Open'].apply(lambda x: int(x)),
            df['High'].apply(lambda x: int(x)),
            df['Low'].apply(lambda x: int(x)),
            df['Close'].apply(lambda x: int(x)),
            df['Volume'].apply(lambda x: int(x)))
    ] 
    results = indicators.get_rsi(quotes, 14)
    df["RSI"] = [results[x].rsi for x in range(len(results))]
    
    return df


def rsi_indicator(data: pd.DataFrame, period: int = 14) -> list: 
    pass

def plot_chart(data: pd.DataFrame):
    pass


def test_algorythm(data: pd.DataFrame) -> float:
    buy_orders = [np.nan for _ in range(WARM_UP_PERIOD)]
    sell_orders = [np.nan for _ in range(WARM_UP_PERIOD)]
    bought = False
    sold = False
    deposit = 0
    
    for candle in range(WARM_UP_PERIOD, len(data)):
        condition_to_buy, condition_to_sell = conditions(data, candle)
        if not bought and not sold:
            if condition_to_buy:                                           
                buy_price = data.iloc[candle]['Close'] #open price of the next candle
                buy_orders.append(buy_price)
                sell_orders.append(np.nan)
                bought = True
                stop_loss = min([data.iloc[:candle]['Local_min_value'].dropna().to_list()[-1], data.iloc[candle]['Low']]) 
                take_profit = buy_price+(buy_price-stop_loss)*2 
                
            elif condition_to_sell:
                sell_price = data.iloc[candle]['Close']
                buy_orders.append(np.nan)
                sell_orders.append(sell_price)
                sold = True
                stop_loss =  max([data.iloc[:candle]['Local_max_value'].dropna().to_list()[-1], data.iloc[candle]['High']])
                take_profit = sell_price-(stop_loss - sell_price)*3

                
            else:
                sell_orders.append(np.nan)
                buy_orders.append(np.nan)

        elif bought:
            if candle == len(data):
                sell_price = data.iloc[candle]['Close']
                buy_orders.append(np.nan)
                sell_orders.append(sell_price)
                bought = False
                deposit += sell_price - buy_price

            #if bought and condition to sell then sell two lots at once
            elif condition_to_sell:
                #sell old contract
                sell_price = data.iloc[candle]['Close']
                buy_orders.append(np.nan)
                sell_orders.append(sell_price)
                bought = False
                deposit += sell_price - buy_price
                #sell additional contact and set stop_loss and take_profit
                sold = True
                stop_loss =  max([data.iloc[:candle]['Local_max_value'].dropna().to_list()[-1], data.iloc[candle]['High']])
                take_profit = sell_price-(stop_loss - sell_price)*3
                
            elif data.iloc[candle]['Low'] <= stop_loss:               
                buy_orders.append(np.nan)
                sell_orders.append(stop_loss)
                bought = False
                deposit += stop_loss - buy_price
            elif data.iloc[candle]['High'] >= take_profit:
                buy_orders.append(np.nan)
                sell_orders.append(take_profit)
                bought = False
                deposit += take_profit - buy_price
            else:
                sell_orders.append(np.nan)
                buy_orders.append(np.nan)

        else:
            if candle == len(data):
                buy_price = data.iloc[candle]['Close']
                buy_orders.append(buy_price)
                sell_orders.append(np.nan)
                sold = False
                deposit += sell_price - buy_price 
            #if sold and condition to buy then buy two lots at once
            elif condition_to_buy:
                #buy old contract
                buy_price = data.iloc[candle]['Close']
                buy_orders.append(buy_price)
                sell_orders.append(np.nan)
                sold = False
                deposit += sell_price - buy_price
                #buy additional contact and set stop_loss and take_profit
                bought = True
                stop_loss = min([data.iloc[:candle]['Local_min_value'].dropna().to_list()[-1], data.iloc[candle]['Low']]) 
                take_profit = buy_price+(buy_price-stop_loss)*2
                 
            elif data.iloc[candle]['High'] >= stop_loss:
                buy_orders.append(stop_loss)
                sell_orders.append(np.nan)
                sold = False
                deposit +=  sell_price - stop_loss
            elif data.iloc[candle]['Low'] <= take_profit:
                buy_orders.append(np.nan)
                sell_orders.append(take_profit)
                sold = False
                deposit += sell_price - take_profit
            else:
                sell_orders.append(np.nan)
                buy_orders.append(np.nan)

    add = ([
        mpf.make_addplot(sell_orders,type='scatter',markersize=100,marker='v'),
        mpf.make_addplot(buy_orders,type='scatter',markersize=100,marker='^')
    ])

    mpf.plot(data,type='candle', volume=False, addplot=add)
    mpf.show()  

    return deposit  
            
    
                
            
    

data = get_data('Data\RTS\SPFB.RTS_200115_230322(15).txt')
print(test_algorythm(data))

""" apdict = ([
    mpf.make_addplot(data['Local_min_value'],type='scatter',markersize=100,marker='^',panel=0),
    mpf.make_addplot(data['Local_max_value'],type='scatter',markersize=100,marker='v', panel=0),
    mpf.make_addplot(data['RSI'],panel=1)
])

mpf.plot(data.iloc[:,:-1],type='candle', volume=False, addplot=apdict)
mpf.show() """ 



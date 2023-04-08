import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
import os
from stock_indicators import Quote
from stock_indicators import indicators
from stock_indicators import CandlePart

TRAILING_STOP = True
WARM_UP_PERIOD = 14
COEFFICIENT = 5


import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
import os
from stock_indicators import Quote
from stock_indicators import indicators
from stock_indicators import CandlePart

TRAILING_STOP = True
WARM_UP_PERIOD = 14
COEFFICIENT = 5

def conditions(data: pd.DataFrame, current: int) -> bool:
    loc_min_value_list = data.iloc[:current]['Local_min_value'].dropna().to_list()
    loc_max_value_list = data.iloc[:current]['Local_max_value'].dropna().to_list()
    condition_to_buy = all([
        data.iloc[current+1]['Predicted_close'] > data.iloc[current]['Predicted_close'], 
        #data.iloc[current]['ema10'] < data.iloc[current]['ema20'],
        loc_min_value_list[-2] > loc_min_value_list[-1],                            
        data.iloc[current]['RSI'] <= 49
    
    ])
    condition_to_sell = all([
        data.iloc[current+1]['Predicted_close'] < data.iloc[current]['Predicted_close'],
        loc_max_value_list[-2] < loc_max_value_list[-1],
        data.iloc[current]['RSI'] > 70
    ])
    return condition_to_buy, condition_to_sell

def get_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, index_col=0, parse_dates=True) #read data from csv
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
    
    #add RSI column
    quotes = [
    Quote(d,o,h,l,c,v) 
    for d,o,h,l,c,v 
    in zip( df.index,
            df.iloc[:-1]['Open'].apply(lambda x: int(x)),
            df.iloc[:-1]['High'].apply(lambda x: int(x)),
            df.iloc[:-1]['Low'].apply(lambda x: int(x)),
            df.iloc[:-1]['Close'].apply(lambda x: int(x)),
            df.iloc[:-1]['Volume'].apply(lambda x: int(x)))
    ] 
    rsi_results = indicators.get_rsi(quotes, 14)
    ema10_result = indicators.get_ema(quotes, 10)
    ema20_result = indicators.get_ema(quotes, 20)
    
    rsi_list= [rsi_results[x].rsi for x in range(len(rsi_results))]
    ema10_list = [ema10_result[x].ema for x in range(len(ema10_result))]
    ema20_list = [ema20_result[x].ema for x in range(len(ema20_result))]
    rsi_list.append(np.nan)
    ema10_list.append(np.nan)
    ema20_list.append(np.nan)
    df["RSI"] = rsi_list
    df["ema10"] = ema10_list
    df["ema20"] = ema20_list
    return df


def plot_chart(data: pd.DataFrame):
    pass


def test_algorythm(data: pd.DataFrame) -> float:
    buy_orders = [np.nan for _ in range(WARM_UP_PERIOD)]
    sell_orders = [np.nan for _ in range(WARM_UP_PERIOD)]
    bought = False
    sold = False
    deposit = 0
    
    for candle in range(WARM_UP_PERIOD, len(data)-1):
        condition_to_buy, condition_to_sell = conditions(data, candle)
        if not bought and not sold:
            if condition_to_buy:                                           
                buy_price = data.iloc[candle]['Close'] #open price of the next candle
                buy_orders.append(buy_price)
                sell_orders.append(np.nan)
                bought = True
                
                stop_loss = min([data.iloc[:candle]['Local_min_value'].dropna().to_list()[-1], data.iloc[candle]['Low']]) 
                take_profit = buy_price+(buy_price-stop_loss)*COEFFICIENT 
                
            elif condition_to_sell:
                sell_price = data.iloc[candle]['Close']
                buy_orders.append(np.nan)
                sell_orders.append(sell_price)
                sold = True
                stop_loss =  max([data.iloc[:candle]['Local_max_value'].dropna().to_list()[-1], data.iloc[candle]['High']])
                take_profit = sell_price-(stop_loss - sell_price)*COEFFICIENT
                

                
            else:
                sell_orders.append(np.nan)
                buy_orders.append(np.nan)

        elif bought:
            if candle == len(data)-1:
                sell_price = data.iloc[candle]['Close']
                buy_orders.append(np.nan)
                sell_orders.append(sell_price)
                bought = False
                deposit += sell_price - buy_price

            #if bought and condition to sell then sell two lots at once
                """ elif condition_to_sell:
                #sell old contract
                sell_price = data.iloc[candle]['Close']
                buy_orders.append(np.nan)
                sell_orders.append(sell_price)
                bought = False
                deposit += sell_price - buy_price
                #sell additional contact and set stop_loss and take_profit
                sold = True
                stop_loss =  max([data.iloc[:candle]['Local_max_value'].dropna().to_list()[-1], data.iloc[candle]['High']])
                take_profit = sell_price-(stop_loss - sell_price)*COEFFICIENT """
                
                
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
                if TRAILING_STOP:
                    try:
                        new_stop = max(data.iloc[candle-10:candle]['Local_min_value'].dropna().to_list())
                        stop_loss = max([stop_loss, new_stop-1000])
                    except:
                        continue
                

        else:
             
            if candle == len(data):
                buy_price = data.iloc[candle]['Close']
                buy_orders.append(buy_price)
                sell_orders.append(np.nan)
                sold = False
                deposit += sell_price - buy_price 
            #if sold and condition to buy then buy two lots at once
                """ elif condition_to_buy:
                #buy old contract
                buy_price = data.iloc[candle]['Close']
                buy_orders.append(buy_price)
                sell_orders.append(np.nan)
                sold = False
                deposit += sell_price - buy_price
                #buy additional contact and set stop_loss and take_profit
                bought = True
                stop_loss = min([data.iloc[:candle]['Local_min_value'].dropna().to_list()[-1], data.iloc[candle]['Low']]) 
                take_profit = buy_price+(buy_price-stop_loss)*5 """
                 
            elif data.iloc[candle]['High'] >= stop_loss:
                buy_orders.append(stop_loss)
                sell_orders.append(np.nan)
                sold = False
                deposit +=  sell_price - stop_loss
            elif data.iloc[candle]['Low'] <= take_profit:
                buy_orders.append(take_profit)
                sell_orders.append(np.nan)
                sold = False
                deposit += sell_price - take_profit
            else:
                sell_orders.append(np.nan)
                buy_orders.append(np.nan)
                if TRAILING_STOP:
                    try:
                        new_stop = min(data.iloc[candle-10:candle]['Local_max_value'].dropna().to_list())
                        stop_loss = min([stop_loss, new_stop+500])
                    except:
                        continue

    
    add = ([
        mpf.make_addplot(sell_orders,type='scatter',markersize=100,marker='v'),
        mpf.make_addplot(buy_orders,type='scatter',markersize=100,marker='^'),
        mpf.make_addplot(data.iloc[:-1]['Predicted_close']),
        mpf.make_addplot(data.iloc[:-1]['RSI'], panel =1), 
    ])

    mpf.plot(data[:-1],type='candle', volume=False, addplot=add)
    mpf.show() 
        
    
    return deposit  
            
    
                
            
    

data = get_data('data_with_predictions_average5.csv')
print(f"Total profit: {test_algorythm(data)}")

""" apdict = ([
    mpf.make_addplot(data['Local_min_value'],type='scatter',markersize=100,marker='^',panel=0),
    mpf.make_addplot(data['Local_max_value'],type='scatter',markersize=100,marker='v', panel=0),
    mpf.make_addplot(data['RSI'],panel=1)
])

mpf.plot(data.iloc[:,:-1],type='candle', volume=False, addplot=apdict)
mpf.show() """ 



import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
import os
from stock_indicators import Quote
from stock_indicators import indicators


PATH = "SI_data_with_predictions_average5.csv"
TRAILING_STOP = True
WARM_UP_PERIOD = 14
COEFFICIENT = 10

def conditions(data: pd.DataFrame, current: int) -> bool:
    loc_min_value_list = data.iloc[:current]['Local_min_value'].dropna().to_list()
    
    condition_to_buy = all([
        #data.iloc[current]['Rates'] >= 0.05,
        #data.iloc[current]['ema_fast'] < data.iloc[current]['ema_slow'],
        
        data.iloc[current+1]['Predicted_close'] > data.iloc[current]['Predicted_close'],        
        #loc_min_value_list[-3] > loc_min_value_list[-2],                                  
        data.iloc[current]['RSI'] < 50
    ])
    condition_to_sell = all([
       
        data.iloc[current]['RSI'] >= 70
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
    pred_rate = [np.nan]
    for tic in range(len(df)):
        if tic == 0:
            loc_min_max.append(np.nan)
        elif tic == len(df)-1:
            loc_min_max.append(np.nan)
            pred_rate.append(np.nan)         
        elif df.iloc[tic]['High'] > df.iloc[tic-1]['High'] and df.iloc[tic]['High'] > df.iloc[tic+1]['High']:           
            loc_min_max.append('max')
            pred_rate.append((df.iloc[tic+1]['Predicted_close']/df.iloc[tic]['Predicted_close']-1)*100)
        elif df.iloc[tic]['Low'] < df.iloc[tic-1]['Low'] and df.iloc[tic]['Low'] < df.iloc[tic+1]['Low']:
            loc_min_max.append('min')
            pred_rate.append((df.iloc[tic+1]['Predicted_close']/df.iloc[tic]['Predicted_close']-1)*100)            
        else:
            loc_min_max.append(np.nan)
            pred_rate.append((df.iloc[tic+1]['Predicted_close']/df.iloc[tic]['Predicted_close']-1)*100)
                    
    df['Local_min_max'] = loc_min_max  
    df['Rates'] =  pred_rate 
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
    rsi_results = indicators.get_rsi(quotes, 70)  
    #ema_fast = indicators.get_ema(quotes, 10)
    #ema_slow = indicators.get_ema(quotes, 50)
    rsi_list= [rsi_results[x].rsi for x in range(len(rsi_results))]
    #ema_fast_list = [ema_fast[x].ema for x in range(len(ema_fast))]
    #ema_slow_list = [ema_slow[x].ema for x in range(len(ema_slow))]
    rsi_list.append(np.nan)
    #ema_fast_list.append(np.nan)
    #ema_slow_list.append(np.nan)
    df["RSI"] = rsi_list
    #df["ema_fast"] = ema_fast_list
    #df["ema_slow"] = ema_slow_list    
    return df


def plot_chart(data: pd.DataFrame):
    pass


def test_algorythm(data: pd.DataFrame) -> float:
    buy_orders = [np.nan for _ in range(WARM_UP_PERIOD)]
    sell_orders = [np.nan for _ in range(WARM_UP_PERIOD)]
    bought = False
    deposit = 0
    
    for candle in range(WARM_UP_PERIOD, len(data)-1):
        condition_to_buy, condition_to_sell = conditions(data, candle)
        if not bought and candle != len(data)-1:
            if condition_to_buy:                                           
                buy_price = data.iloc[candle]['Close'] #open price of the next candle
                buy_orders.append(buy_price)
                sell_orders.append(np.nan)
                bought = True
                buy_position = candle 
                loc_min =  min(data.iloc[:candle]['Local_min_value'].dropna().to_list()[-3:])             
                stop_loss = min([loc_min, data.iloc[candle]['Low']])
                #take_profit = buy_price+(buy_price-stop_loss)*COEFFICIENT              
            
            else:
                sell_orders.append(np.nan)
                buy_orders.append(np.nan)

        else:
            if candle == len(data)-1:
                sell_price = data.iloc[candle]['Close']
                buy_orders.append(np.nan)
                sell_orders.append(sell_price)
                bought = False
                deposit += sell_price - buy_price

            elif data.iloc[candle]['Low'] <= stop_loss:               
                buy_orders.append(np.nan)
                sell_orders.append(stop_loss)
                bought = False
                deposit += stop_loss - buy_price

                """ elif data.iloc[candle]['High'] >= take_profit:
                buy_orders.append(np.nan)
                sell_orders.append(take_profit)
                bought = False
                deposit += take_profit - buy_price """

            elif condition_to_sell:
                sell_price = data.iloc[candle]['Close']
                buy_orders.append(np.nan)
                sell_orders.append(sell_price)
                bought = False
                deposit += sell_price - buy_price
            else:
                sell_orders.append(np.nan)
                buy_orders.append(np.nan)
                if TRAILING_STOP:
                    try:
                        new_stop = max(data.iloc[buy_position:candle]['Local_min_value'].dropna().to_list())
                        stop_loss = max([stop_loss, new_stop-200])
                    except:
                        continue
                
    add = ([
        mpf.make_addplot(sell_orders,type='scatter',markersize=150,marker='v'),
        mpf.make_addplot(buy_orders,type='scatter',markersize=150,marker='^'),
        
        mpf.make_addplot(data.iloc[:-1]['Predicted_close']),
        mpf.make_addplot(data.iloc[:-1]['RSI'], panel =1), 
        #mpf.make_addplot(data.iloc[:-1]['ema_fast'], color = 'r'),
        #mpf.make_addplot(data.iloc[:-1]['ema_slow'], color = 'b'), 
    ])

    mpf.plot(data[:-1],type='candle', volume=False, addplot=add)
    mpf.show() 
    deals = []
    for _ in range(len(buy_orders)):
        if buy_orders[_] > 0:
            deals.append(buy_orders[_])  
    print(len(deals)) 
    
    return deposit  
            
    
                
            
    

data = get_data(PATH)
print(f"Total profit: {test_algorythm(data)}")

""" apdict = ([
    mpf.make_addplot(data['Local_min_value'],type='scatter',markersize=100,marker='^',panel=0),
    mpf.make_addplot(data['Local_max_value'],type='scatter',markersize=100,marker='v', panel=0),
    mpf.make_addplot(data['RSI'],panel=1)
])

mpf.plot(data.iloc[:,:-1],type='candle', volume=False, addplot=apdict)
mpf.show() """ 



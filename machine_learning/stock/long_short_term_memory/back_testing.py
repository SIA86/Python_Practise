import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
import os
from stock_indicators import Quote
from stock_indicators import indicators
from statistic import Statistics


PATH = "SI_data_with_predictions_512-32x5nn.15min_small.csv"
TRAILING_STOP = True
WARM_UP_PERIOD = 35
COEFFICIENT = 10


#define all conditions to buy, sell and to close opened orders
def conditions(data: pd.DataFrame, current: int) -> bool:
    loc_min_value_list = data.iloc[:current]['Local_min_value'].dropna().to_list()
    loc_max_value_list = data.iloc[:current]['Local_max_value'].dropna().to_list()
    condition_to_buy = all([
        current != len(data)-1,
        data.iloc[current]['Rates'] >= data.iloc[current-1]['Rates'],
               
        data.iloc[current]['Rates'] >= 0.002,
        data.iloc[current]['Rates'] <= 0.1,
        data.iloc[current]['ema_fast'] > data.iloc[current]['ema_slow'], 
        #abs(data.iloc[current]['ema_fast'] - data.iloc[current]['ema_slow']) > 10, 
         
        #data.iloc[current+1]['Predicted_close'] > data.iloc[current]['Predicted_close'],        
        #any([data.iloc[current-i]['Down_shadow'] >= 0.6 * data.iloc[current-i]['Total'] for i in range(5)]),
        #loc_min_value_list[-3] > loc_min_value_list[-2], 
        #loc_min_value_list[-2] < loc_min_value_list[-1],                                 
        data.iloc[current]['RSI_slow'] < 70,    

    ])
    condition_to_sell = all([       
        current != len(data)-1,
        data.iloc[current]['Rates'] <= data.iloc[current-1]['Rates'],
        data.iloc[current]['Rates'] <= -0.002,
        data.iloc[current]['Rates'] >= -0.1,
        data.iloc[current]['ema_fast'] < data.iloc[current]['ema_slow'],
        #abs(data.iloc[current]['ema_fast'] - data.iloc[current-1]['ema_fast']) > 100,
        #abs(data.iloc[current]['ema_fast'] - data.iloc[current]['ema_slow']) > 10,
        data.iloc[current]['RSI_slow'] > 30
        #any([data.iloc[current-i]['Up_shadow'] >= 0.6 * data.iloc[current-i]['Total'] for i in range(5)]),
    ])
    close_bought = any([
        data.iloc[current]['RSI_slow'] >= 75,
        current == len(data)-1,
        all([
            data.iloc[current]['Colore'] == 'Red',
            data.iloc[current]['Rates'] >= 0.2
        ])          
    ])
    close_sold = any([
        data.iloc[current]['RSI_slow'] <= 25,
        current == len(data)-1,
        #any([data.iloc[current-i]['Down_shadow'] >= 0.7 * data.iloc[current-i]['Total'] for i in range(5)]),
    ])
    return condition_to_buy, condition_to_sell, close_bought, close_sold


#prepare the data for calculation
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
    #add RSI and EMA column
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
    rsi_slow = indicators.get_rsi(quotes, WARM_UP_PERIOD)
    ema_super_fast = indicators.get_ema(quotes, 15)  
    ema_fast = indicators.get_ema(quotes, 50)
    ema_slow = indicators.get_ema(quotes, 100)
    rsi_slow_list= [rsi_slow[x].rsi for x in range(len(rsi_slow))]
    ema_super_fast_list= [ema_super_fast[x].ema for x in range(len(ema_super_fast))]
    ema_fast_list = [ema_fast[x].ema for x in range(len(ema_fast))]
    ema_slow_list = [ema_slow[x].ema for x in range(len(ema_slow))]
    rsi_slow_list.append(np.nan)
    ema_super_fast_list.append(np.nan)
    ema_fast_list.append(np.nan)
    ema_slow_list.append(np.nan)
    df["RSI_slow"] = rsi_slow_list
    df["ema_super_fast"] = ema_super_fast_list
    df["ema_fast"] = ema_fast_list
    df["ema_slow"] = ema_slow_list    
    return df


#algoryth to simulate trading and check the strategy results
def test_algorythm():
    data = get_data(PATH)
    stat = Statistics(50000) #create instance for keeping track statistics      
    #create lists for saving buy and sell orders and boolean variables to track the status of deals
    buy_orders = [np.nan for _ in range(WARM_UP_PERIOD)]  #warm-up period must be filled  with NAN
    sell_orders = [np.nan for _ in range(WARM_UP_PERIOD)]
    bought = False
    sold = False   
    for candle in range(WARM_UP_PERIOD, len(data)-1): #trading loop
        condition_to_buy, condition_to_sell, close_bought, close_sold = conditions(data, candle)
        if not bought and not sold: #if there are no deals
            if condition_to_buy:
                stat.add_buy()                                           
                buy_price = data.iloc[candle+1]['Open'] #open price of the next candle
                buy_orders.append(buy_price)
                sell_orders.append(np.nan)
                bought = True
                buy_position = candle #save the position of deal
                loc_min =  min(data.iloc[:candle]['Local_min_value'].dropna().to_list()[-3:]) #local min of last 3 minimum            
                stop_loss = min([loc_min, data.iloc[candle]['Low']]) -100
                #take_profit = buy_price+(buy_price-stop_loss)*COEFFICIENT              
            elif condition_to_sell:
                stat.add_sell()
                sell_price = data.iloc[candle+1]['Open'] #open price of the next candle
                buy_orders.append(np.nan)
                sell_orders.append(sell_price)
                sold = True
                sell_position = candle  #save the position of deal
                loc_max =  max(data.iloc[:candle]['Local_max_value'].dropna().to_list()[-3:]) #local max of last 3 maximum         
                stop_loss = max([loc_max, data.iloc[candle]['High']]) + 100 #need to make a dependence from total size of last 50 candles
                #take_profit = None
            else:
                sell_orders.append(np.nan)
                buy_orders.append(np.nan)
        elif bought: 
            if close_bought: #if bought and condition to sell
                sell_price = data.iloc[candle+1]['Open']
                buy_orders.append(np.nan)
                sell_orders.append(sell_price)
                bought = False
                profit = sell_price - buy_price
                stat.upg_depo_buys(profit)
                if profit > 0:
                    stat.add_win_buys()                
            elif data.iloc[candle]['Low'] <= stop_loss: #if price is lower than stop-loss           
                buy_orders.append(np.nan)
                sell_orders.append(stop_loss)
                bought = False
                profit = stop_loss - buy_price
                stat.upg_depo_buys(profit)
                if profit > 0:
                    stat.add_win_buys()
                """
                elif data.iloc[candle]['High'] >= take_profit: #if price is higher than take_profit
                buy_orders.append(np.nan)
                sell_orders.append(take_profit)
                bought = False
                profit = take_profit - buy_price
                stat.upg_depo_buys(profit)
                if profit > 0:
                    stat.add_win_buys()
                """
            else: #if not stop_loos or take_profit or conditiopn_to_sell just append NAN to buy and sell orders
                sell_orders.append(np.nan)
                buy_orders.append(np.nan)
                if TRAILING_STOP: #if trailing stop is not False check conditions to update stop_loss
                    try:
                        new_stop = max(data.iloc[buy_position:candle]['Local_min_value'].dropna().to_list())
                        stop_loss = max([stop_loss, new_stop-20]) 
                    except:
                        continue
        else: #if sold           
            if close_sold: #if sold and condition to buy
                buy_price = data.iloc[candle+1]['Open']
                buy_orders.append(buy_price)
                sell_orders.append(np.nan)
                sold = False
                profit = sell_price - buy_price 
                stat.upg_depo_sells(profit)
                if profit > 0:
                    stat.add_win_sells()   
            elif data.iloc[candle]['High'] >= stop_loss: #if price is higher than stop-loss
                buy_orders.append(stop_loss)
                sell_orders.append(np.nan)
                sold = False
                profit =  sell_price - stop_loss
                stat.upg_depo_sells(profit)
                if profit > 0:
                    stat.add_win_sells()
                """ 
                elif data.iloc[candle]['Low'] <= take_profit: #if price is lower than take_profit
                buy_orders.append(take_profit)
                sell_orders.append(np.nan)
                sold = False
                stat.upg_depo_sells(profit)
                if profit > 0:
                    stat.add_win_sells()
                """
            else: #if not stop_loos or take_profit or conditiopn_to_buy just append NAN to buy and sell orders
                sell_orders.append(np.nan)
                buy_orders.append(np.nan)
                if TRAILING_STOP: #if trailing stop is not False check conditions to update stop_loss
                    try:
                        new_stop = min(data.iloc[sell_position:candle]['Local_max_value'].dropna().to_list())
                        stop_loss = min([stop_loss, new_stop+20])
                    except:
                        continue
    print(stat)
    plot_chart(data, sell_orders, buy_orders)            
       
    
#chart making function            
def plot_chart(data: pd.DataFrame, sell_orders: list, buy_orders: list):
    add = ([
    mpf.make_addplot(sell_orders,type='scatter',markersize=150,marker='v'),
    mpf.make_addplot(buy_orders,type='scatter',markersize=150,marker='^'),
    
    mpf.make_addplot(data.iloc[:-1]['Predicted_close']),
    mpf.make_addplot(data.iloc[:-1]['RSI_slow'], panel =1),
    mpf.make_addplot(data.iloc[:-1]['ema_fast'], color = 'r'),
    mpf.make_addplot(data.iloc[:-1]['ema_slow'], color = 'b'), 
    #mpf.make_addplot(data.iloc[:-1]['ema_super_fast'], color = 'y')
    ])

    mpf.plot(data[:-1],type='candle', volume=False, addplot=add, warn_too_much_data=100000)
    mpf.show()     
                                
if __name__ == '__main__':
    test_algorythm()







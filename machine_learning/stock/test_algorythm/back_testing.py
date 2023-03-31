import pandas as pd
import numpy as np

def get_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.dropna()
    df['<DATE>'] = df['<DATE>'].apply(lambda x: str(x))
    df['<TIME>'] = df['<TIME>'].apply(lambda x: str(x) if x > 0 else "000000")
    df['<DATE>'] = df['<DATE>'] + df['<TIME>']
    df['<DATE>'] = pd.to_datetime(df['<DATE>'], format="%Y%m%d%H%M%S")
    df = df.set_index('<DATE>')
    df = df.iloc[:,3:]
    return df


""" def chart_monitoring(data: pd.DataFrame) -> float:
    deals = 0
    buy_orders = []
    sell_orders = []
    sold = False
    bought = False
    stop_loss = 0

    for candle in range(data.shape[0]):
        if not bought:
            if data.iloc[candle]['Predicted_close'] - data.iloc[candle-1]['Predicted_close'] > 0:
                buy_price = data.iloc[candle+1]['Open']
                print("_------------_------------_")
                print(f'Deal #{candle}')
                print(f"Buy price: {buy_price}")
                stop_loss = min([data.iloc[x]['Low'] - 10 for x in range(candle -10, candle)])
                print(f"Stop_loss: {stop_loss}")
                take_profit = buy_price + 1000
                print(f"Take Profit: {take_profit}")
                buy_orders.append(buy_price)
                sell_orders.append(np.nan)
                bought = True
            else:
                sell_orders.append(np.nan)
                buy_orders.append(np.nan)
            
        elif bought:
            if  data.iloc[candle]['Low'] < stop_loss:
                
                sell_price = stop_loss
                print(f"Stop_loss reached: {sell_price}")
                sell_orders.append(sell_price)
                buy_orders.append(np.nan)
                deals = buy_price - sell_price
                bought = False
            elif data.iloc[candle]['High'] > take_profit:
                sell_price = take_profit
                print(f"Take profit reached: {sell_price}")
                sell_orders.append(sell_price)
                buy_orders.append(np.nan)
                deals = buy_price - sell_price
                bought = False
            else:
                sell_orders.append(np.nan)
                buy_orders.append(np.nan)
    
                
            
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
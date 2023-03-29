from prediction import get_data
import pandas as pd
import numpy as np


def chart_monitoring():
    buy_oreders = []
    sell_oreders = []
    status = False
    for candle in range(data.shape[0]):
        if !status:
            if condition_to_buy:
                buy_price = data.loc[candle+1, 'Open']
                buy_orders.append(buy_price)
                status = !status
            if condition_to_sell:
                sell_price = data.loc[candle+1, 'Open']
                sell_orders.append(sell_price)
                status = !status
        else:



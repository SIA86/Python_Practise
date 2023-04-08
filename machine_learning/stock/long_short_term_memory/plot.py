import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt


data1 = pd.read_csv('data_with_predictions_average5.csv', index_col=0, parse_dates=True)
data2 = pd.read_csv('data_with_predictions_last.csv', index_col=0, parse_dates=True)

add = ([
        mpf.make_addplot(data1['Predicted_close'], color='green'),
        mpf.make_addplot(data2['Predicted_close']), 
    ])

mpf.plot(data1, type='candle', volume=False, addplot=add)
mpf.show() 
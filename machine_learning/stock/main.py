"""
For this programm you need to dowload stock market prices history data and save it locally in .csv format.
Then the data will be  normalized
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy import stats
from sklearn.model_selection import train_test_split
import tensorflow as tf
import datetime


#read data from csv
RTS = pd.read_csv(f'Data{os.sep}RTS{os.sep}SPFB.RTS_140115_230322.txt')
#select only the data and close price
RTS = RTS[['<DATE>', '<CLOSE>']]
#rename colums
RTS.rename(columns={'<CLOSE>': 'RTS'}, inplace=True)
RTS.rename(columns={'<DATE>': 'DATE'}, inplace=True)


#plot the chart
y= RTS['RTS']
#convert int date to datetime64 format
x = RTS['DATE'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
fig, ax = plt.subplots()
plt.xlabel('Date')
plt.ylabel('Value')
ax.plot(x,y)
#plt.show()

date_train = RTS['DATE'][:2500]
value_train = RTS['RTS'][:2500]
date_valid = RTS['DATE'][2500:]
value_valid = RTS['RTS'][2500:]


#preprocessing
def windowed_dataset(data, window_size = 30, batch_size = 32):

    dataset = tf.data.Dataset.from_tensor_slices(data)
    dataset = dataset.window(window_size, shift = 1, drop_remainder=True)
    dataset = dataset.flat_map(lambda window: window.batch(window_size + 1))
    dataset = dataset.shuffle(2500)
    dataset = dataset.map(lambda window: (window[:-1], window[-1]))
    dataset = dataset.batch(batch_size).prefetch(1)

    return dataset

dataset = windowed_dataset(value_train)

""" for window in dataset:
    for val in window:
        print(val.numpy(), end = ' ')
    print() """

def create_uncompiled_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Lambda(lambda x: tf.expand_dims(x, axis = -1), input_shape= [None]),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(1024, return_sequences = True)),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(528, return_sequences = True)),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(256, return_sequences = True)),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(128, return_sequences = True)),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences = True)),
        tf.keras.layers.Dense(1),
    ])

    return model

class EarlyStopping(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs = {}):
        if (logs.get('mae') < 0.1):
            print('\nMAEthreshold reached. Training stopped.')
            self.model.stop_training = True

early_stopping = EarlyStopping()

def create_model():
    tf.random.set_seed(51)

    model = create_uncompiled_model()

    model.compile(
        loss = tf.keras.losses.Huber(),
        optimizer = tf.keras.optimizers.Adam(learning_rate = 0.001),
        metrics = 'mae')

    return model    

model = create_model()

history = model.fit(dataset, epochs = 20, callbacks = [early_stopping])
model.save("model.keras")

plt. figure(figsize = (10, 6))
plt.plot(history.history['mae'], label='mae')
plt.plot(history.history['loss'], label = 'loss')
plt.legend
plt.show()

import os
import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
import tensorflow as tf


def get_data(path: str) -> pd.DataFrame:
    
    df = pd.read_csv(path, index_col=2, parse_dates=True)
    df = df.dropna()  #drop all null values
    df = df[['<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<VOL>']] #drop useless colums
    normalized = max(df['<HIGH>']) #create general normalisation coefficient
    df[['<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>']] = df[['<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>']].apply(lambda x: x/normalized) #apply n. coeficient to price colums
    df['<VOL>'] = df['<VOL>'].apply(lambda x: x/max(df['<VOL>'])) #normilized volume column
    df = df.rename(columns={'<OPEN>':'Open', '<HIGH>':'High', '<LOW>':'Low', '<CLOSE>':'Close', '<VOL>':'Volume'})
    df.index.name = 'Date'
    
    return df


def plot_chart(data_frame: pd.DataFrame, start: int, end: int, volume: bool):
    
    #end = len(data_frame.index) #set start and end variables
    mpf.plot(data_frame.iloc[start:end,:], type='candle', volume= True)


def dataset(data: pd.DataFrame, window_size: int = 30, batch_size: int = 50) -> tf.data.Dataset:
    dataset = tf.data.Dataset.from_tensor_slices(data)
    dataset = dataset.window(window_size +1, shift = 1, drop_remainder=True)
    dataset = dataset.flat_map(lambda x: x.batch(window_size+1))
    dataset = dataset.shuffle(500)
    dataset = dataset.map(lambda x: (x[:-1], x[-1][:-1]))
    dataset = dataset.batch(batch_size).prefetch(1)

    return dataset


def split_data(data: pd.DataFrame) -> pd.DataFrame:
    train_set = dataset(data[:2800]) 
    validation_set = dataset(data[2800:3000])
    test_set = dataset(data[3000:])

    return train_set, validation_set, test_set


def create_uncompiled_model() -> tf.keras.models.Sequential:
  # define a sequential model
  model = tf.keras.models.Sequential([ 
      tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
      tf.keras.layers.Dropout(0.3),
      tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
      tf.keras.layers.Dropout(0.3),
      tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
      tf.keras.layers.Dropout(0.3),
      tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
      tf.keras.layers.Dropout(0.3),
      tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
      tf.keras.layers.Dropout(0.3),
      tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
      tf.keras.layers.Dropout(0.3),
      tf.keras.layers.Dense(4),
  ]) 

  return model


def create_model() -> tf.keras.models.Sequential:    
    tf.random.set_seed(51)
    model = create_uncompiled_model()
    model.compile(loss=tf.keras.losses.Huber(),
                  optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  metrics=["mae"])
    return model 


def plot_loss(model: tf.keras.models.Sequential):
    plt.figure(figsize=(10, 6))
    plt.plot(model.history['mae'], label='mae')
    plt.plot(model.history['loss'], label='loss')
    plt.legend()
    plt.show()


def model_forecast(model: tf.keras.models.Sequential, data: pd.DataFrame, window_size: int) -> np.array:
    ds = tf.data.Dataset.from_tensor_slices(data)
    ds = ds.window(window_size, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(window_size))
    ds = ds.batch(32).prefetch(1)
    forecast = model.predict(ds)
            
    return forecast

def to_pd(forecast: np.array, data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    df = df[:-30]
    df[['Open', 'High', 'Low', 'Close']] = [forecast[:,0], forecast[:,1], forecast[:,2], forecast[:,3]]
    return df

data = get_data(f'Data{os.sep}RTS{os.sep}SPFB.RTS_140115_230322.txt') #get data from given csv file
plot_chart(data, start = 2500, end = 2600, volume = True)
train_set, validation_set, test_set = split_data(data) #split data to train, validation and test parts
model = create_model() #create model
try:
    model = tf.keras.models.load_model('model.keras.six_bidirectional_lstm_layers_64')
    print('Loading trained model')
    
except Exception as e:
    print('No saved model')
    history = model.fit(train_set, epochs=15, validation_data = validation_set) #fit model
    plot_loss(history)
    model.save('model.keras.six_bidirectional_lstm_layers_64')
    model.evaluate(test_set, batch_size=50)

forecast = to_pd(model_forecast(model, data, 30).squeeze(), data)

plot_chart(forecast, start =3000, end = 3773, volume = False)



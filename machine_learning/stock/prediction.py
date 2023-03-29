import os
import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
import tensorflow as tf


WIN_SIZE = 20

def get_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, index_col=2, parse_dates=True)
    df = df.dropna()  #drop all null values
    df = df[['<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<VOL>']] #drop useless colums
    df = df.rename(columns={'<OPEN>':'Open', '<HIGH>':'High', '<LOW>':'Low', '<CLOSE>':'Close', '<VOL>':'Volume'})
    df.index.name = 'Date'   
    global normalized
    normalized = max(df['High']) #create general normalisation coefficient 
    df.iloc[:,:-1] = df.iloc[:,:-1]/normalized #apply n. coeficient to price colums
    df['Volume'] = df['Volume']/max(df['Volume']) 
    return df


def dataset(data: pd.DataFrame, batch_size: int = 50) -> tf.data.Dataset:
    dataset = tf.data.Dataset.from_tensor_slices(data)
    dataset = dataset.window(WIN_SIZE +1, shift = 1, drop_remainder=True)
    dataset = dataset.flat_map(lambda x: x.batch(WIN_SIZE+1))
    dataset = dataset.shuffle(1000)
    dataset = dataset.map(lambda x: (x[:-1], x[-1][3]))
    dataset = dataset.batch(batch_size).prefetch(1)
    return dataset


def split_data(data: pd.DataFrame, split: float) -> pd.DataFrame:
    size = int(data.shape[0]*split)
    train_set = dataset(data[:int(size*0.9)]) 
    validation_set = dataset(data[int(size*0.9)]:size)
    test_set = dataset(data[size:])
    return train_set, validation_set, test_set


def create_uncompiled_model() -> tf.keras.models.Sequential:
  # define a sequential model
  model = tf.keras.models.Sequential([ 
      tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(128, return_sequences=True)),
      tf.keras.layers.Dropout(0.3),
      tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(128, return_sequences=True)),
      tf.keras.layers.Dropout(0.3),
      tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(128, return_sequences=True)),
      tf.keras.layers.Dropout(0.3),
      tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(128, return_sequences=True)),
      tf.keras.layers.Dropout(0.3),
      tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(128, return_sequences=True)),
      tf.keras.layers.Dropout(0.3),
      tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(128)),
      tf.keras.layers.Dropout(0.3),
      tf.keras.layers.Dense(1),
  ]) 
  return model


def create_model() -> tf.keras.models.Sequential:    
    tf.random.set_seed(51)
    model = create_uncompiled_model()
    model.compile(loss=tf.keras.losses.Huber(),
                  optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  metrics=tf.keras.metrics.MeanAbsoluteError())
    return model 


def plot_loss(model: tf.keras.models.Sequential): -> None
    plt.figure(figsize=(10, 6))
    #ax.set_xlim(xmin=0)
    plt.plot(model.history['mae'], label='MSE')
    plt.plot(model.history['loss'], label='HUBER')
    plt.legend()
    plt.show()


def model_forecast(model: tf.keras.models.Sequential, data: pd.DataFrame) -> np.array:
    ds = tf.data.Dataset.from_tensor_slices(data)
    ds = ds.window(WIN_SIZE, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(WIN_SIZE))
    ds = ds.batch(32).prefetch(1)
    forecast = model.predict(ds)
    return forecast


def concatinate_results(data: pd.DataFrame, forecast: np.array) -> pd.DataFrame:
    df = data.copy()  
    forecast 
    """ df = df.iloc[:,3:-1]
    df.iloc[:WIN_SIZE,:] = np.NAN
    df = df.append(pd.Series(name = max(df.index) + pd.Timedelta('1 day')))
    df.iloc[WIN_SIZE:,:] = forecast """
    df.to_csv('forecast.csv')


def main():
    print('loading data')
    data = get_data(f'Data{os.sep}RTS{os.sep}SPFB.RTS_200115_230322(15).txt') #get data from given csv file

    try:
        print('Trying to load predictions')
        forecast = pd.read_csv('forecast.csv', index_col=0, parse_dates=True )
    except Exception as e:
        print('No predictions found')
        #plot_chart(data, start = 0, end = None, volume = True)
        
        try:
            model = tf.keras.models.load_model('model.model.keras.128nn.15min')
            print('Loading trained model')
            
        except Exception as e:
            print('No saved model')
            train_set, validation_set, test_set = split_data(data, split = 0.8) #split data to train, validation and test parts
            model = create_model() #create model
            history = model.fit(train_set, epochs=15, validation_data = validation_set) #fit model
            plot_loss(history)
            model.save('model.model.keras.128nn.15min')
            model.evaluate(test_set, batch_size=50)

        forecast = model_forecast(model, data[int(data.shape[0]*0.8):])
    print('plotting...')

    apdict = mpf.make_addplot((forecast['Close']*normalized))
    plot_data = data.iloc[:,:-1]
    plot_data = plot_data[int(plot_data.shape[0]*0.8):]
    plot_data = plot_data*normalized
    plot_data = plot_data.append(pd.Series(name = max(plot_data.index) + pd.Timedelta('1 day')))
    mpf.plot(plot_data,type='candle', volume=False, addplot=apdict)
    mpf.show()


if __name__ == "__main__":
    main()


import os
import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
import tensorflow as tf

SPLIT = 0.8
WIN_SIZE = 20

def get_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.dropna()  #drop all null values
    #convert <DATE> and <TIME> columns to datetime format="%Y%m%d%H%M%S"
    df['<DATE>'] = df['<DATE>'].apply(lambda x: str(x))
    df['<TIME>'] = df['<TIME>'].apply(lambda x: str(x) if x > 0 else "000000")
    df['<DATE>'] = df['<DATE>'] + df['<TIME>']
    df['<DATE>'] = pd.to_datetime(df['<DATE>'], format="%Y%m%d%H%M%S")
    df = df.rename(columns={'<DATE>': 'Date',
                            '<OPEN>': 'Open',
                            '<HIGH>': 'High',
                            '<LOW>': 'Low',
                            '<CLOSE>': 'Close',
                            '<VOL>': 'Volume'}
                        )
    #set index to timestamp object
    df = df.set_index('Date')
    df.index.name = 'Date'  
    #drop useless columns
    df = df.iloc[:,3:] 
    global normalized
    normalized = max(df['High']) #create general normalisation coefficient 
    df= df/normalized #apply n. coeficient to price colums
    return df


def dataset(data: pd.DataFrame, batch_size: int = 50) -> tf.data.Dataset:
    dataset = tf.data.Dataset.from_tensor_slices(data)
    dataset = dataset.window(WIN_SIZE + 5, shift = 1, drop_remainder=True)
    dataset = dataset.flat_map(lambda x: x.batch(WIN_SIZE+10))
    dataset = dataset.shuffle(1000)
    
    dataset = dataset.map(lambda x: (x[:-5], sum([x[-5][3], x[-4][3], x[-3][3], x[-2][3], x[-1][3]])/5))
    dataset = dataset.batch(batch_size).prefetch(1)
    return dataset


def split_data(data: pd.DataFrame, size: int) -> pd.DataFrame:
    
    train_set = dataset(data[:int(size*0.9)]) 
    validation_set = dataset(data[int(size*0.9):size])
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


def plot_loss(model: tf.keras.models.Sequential) -> None:
    plt.figure(figsize=(10, 6))
    #ax.set_xlim(xmin=0)
    plt.plot(model.history['mse'], label='MSE')
    plt.plot(model.history['loss'], label='HUBER')
    plt.legend()
    plt.show()


def model_forecast(model: tf.keras.models.Sequential, data: pd.DataFrame) -> pd.DataFrame:
    ds = tf.data.Dataset.from_tensor_slices(data)
    ds = ds.window(WIN_SIZE, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(WIN_SIZE))
    ds = ds.batch(32).prefetch(1)
    forecast = model.predict(ds)
    df = data.copy()
    
    df = df.append(pd.Series(name = max(df.index) + pd.Timedelta('15 min')))  
    empty_rows = np.array([[np.NAN] for _ in range(WIN_SIZE)])
    forecast = np.concatenate((empty_rows, forecast))
    df['Predicted_close'] = forecast
    df = df*normalized
    df.to_csv('data_with_predictions.csv')
    return df


def main():
    print('loading data')
    data = get_data(f'Data\RTS\SPFB.RTS_200115_230322(15).txt') #get data from given csv file
    size = int(len(data)*SPLIT)
    try:
        print('Trying to load predictions')
        data_with_predictions = pd.read_csv('data_with_predictions.csv', index_col=0, parse_dates=True )
    except Exception as e:
        print('No predictions found')
        #plot_chart(data, start = 0, end = None, volume = True)
        
        try:
            print('Loading trained model')
            model = tf.keras.models.load_model('model.keras.128nn.15min_average')
            print(f'Loaded successfully')
            
        except Exception as e:
            print('No saved model')
            train_set, validation_set, test_set = split_data(data, size) #split data to train, validation and test parts
            model = create_model() #create model
            history = model.fit(train_set, epochs=15, validation_data = validation_set) #fit model
            
            model.save('model.keras.128nn.15min_average')
            model.evaluate(test_set, batch_size=50)
            plot_loss(history)

        data_with_predictions = model_forecast(model, data[size:])
    print('plotting...')

    apdict = mpf.make_addplot((data_with_predictions['Predicted_close']))
    mpf.plot(data_with_predictions.iloc[:,:-1],type='candle', volume=False, addplot=apdict)
    mpf.show()


if __name__ == "__main__":
    main()


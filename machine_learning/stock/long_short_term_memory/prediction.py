import os
import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
import tensorflow as tf

#path and filenames
PATH = f'Data{os.sep}SI{os.sep}SPFB.Si_200115_230322_15min.csv'
KERAS_MODEL_NAME = 'SI_model.keras.128x5nn.15min'
PREDICTION_NAME = 'SI_data_with_predictions_15min.csv'

#options
SPLIT = 0.8 #size of training set
WIN_SIZE = 25 #length of candles sequence to analize


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
    return df


def split_and_normalize_data(data: pd.DataFrame, size: int) -> pd.DataFrame:   
    train_df = data[:int(size*0.8)]
    val_df = data[int(size*0.8):size]
    test_df = data[size:]
    #count mean ans std for tarin_df and save it
    train_mean = train_df.mean()
    train_std = train_df.std()
    norm_coeff = pd.DataFrame({
        "train_mean": train_mean,
        "train_std": train_std
        })
    norm_coeff.to_csv('normalisation_coefficient.csv')

    #nornalize data
    train_df = (train_df-train_mean)/train_std
    val_df = (val_df-train_mean)/train_std
    test_df = (test_df-train_mean)/train_std

    return train_df, val_df, test_df


def dataset(data: pd.DataFrame, batch_size: int = 50) -> tf.data.Dataset:
    dataset = tf.data.Dataset.from_tensor_slices(data)
    dataset = dataset.window(WIN_SIZE + 1, shift = 1, drop_remainder=True)
    dataset = dataset.flat_map(lambda x: x.batch(WIN_SIZE + 1))
    dataset = dataset.shuffle(1000)
    
    dataset = dataset.map(lambda x: (x[:-1], x[-1][3]))
    dataset = dataset.batch(batch_size).prefetch(1)
    return dataset

def create_uncompiled_model() -> tf.keras.models.Sequential:
    # define a sequential model
    model = tf.keras.models.Sequential([ 
        #tf.keras.layers.Lambda(lambda x: tf.expand_dims(x, axis=-1, input_shape=[None])),
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
        tf.keras.layers.Dense(1)
    ]) 
  
    return model


def create_model() -> tf.keras.models.Sequential:    
    tf.random.set_seed(51)
    model = create_uncompiled_model()
    model.compile(loss=tf.keras.losses.Huber(),
                  optimizer=tf.keras.optimizers.Adam(learning_rate=0.003),
                  metrics=tf.keras.metrics.MeanAbsoluteError())
    
    return model 


def plot_loss(model: tf.keras.models.Sequential) -> None:
    plt.figure(figsize=(10, 6))
    #ax.set_xlim(xmin=0)
    plt.plot(model.history['mean_absolute_error'], label='MAE')
    plt.plot(model.history['loss'], label='HUBER')
    plt.legend()
    plt.show()


def model_forecast(model: tf.keras.models.Sequential, data: pd.DataFrame) -> pd.DataFrame:
    normalisation_df  = pd.read_csv('normalisation_coefficient.csv', index_col=0)
    train_mean = normalisation_df['train_mean']
    train_std = normalisation_df['train_std']
    norm_data = (data-train_mean)/train_std
    ds = tf.data.Dataset.from_tensor_slices(norm_data)
    ds = ds.window(WIN_SIZE, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(WIN_SIZE))
    ds = ds.batch(32).prefetch(1)
    forecast = model.predict(ds)
    forecast = forecast*train_std.loc['Close'] + train_mean.loc['Close']
    df = data.copy()
    df = df.append(pd.Series(name = max(df.index) + pd.Timedelta('15 min')))  
    empty_rows = np.array([[np.NAN] for _ in range(WIN_SIZE)])
    forecast = np.concatenate((empty_rows, forecast))
    df['Predicted_close'] = forecast
    
    df.to_csv(PREDICTION_NAME)
    return df


def main():
    print('loading data')
    data = get_data(PATH)  #get data from given csv file
    size = int(len(data)*SPLIT)
    try:
        print('Trying to load predictions')
        data_with_predictions = pd.read_csv(PREDICTION_NAME, index_col=0, parse_dates=True )
    except Exception as e:
        print('No predictions found')
        #plot_chart(data, start = 0, end = None, volume = True)
        
        try:
            print('Loading trained model')
            model = tf.keras.models.load_model(KERAS_MODEL_NAME)
            print(f'Loaded successfully')
            
        except Exception as e:
            print('No saved model')
            train_set, validation_set, test_set = map(dataset, split_and_normalize_data(data, size)) 
            model = create_model() #create model
            history = model.fit(train_set, epochs=15, validation_data = validation_set) #fit model
            #model.summary()
            model.save(KERAS_MODEL_NAME)
            model.evaluate(test_set, batch_size=50)
            plot_loss(history)

        data_with_predictions = model_forecast(model, data)
    print('plotting...')

    apdict = mpf.make_addplot((data_with_predictions['Predicted_close']))
    mpf.plot(data_with_predictions.iloc[:,:-1],type='candle', volume=False, addplot=apdict)
    mpf.show()


if __name__ == "__main__":
    main()


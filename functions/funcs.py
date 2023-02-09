import yfinance as yf
import pandas as pd
import numpy as np



def generate_data(stocks: dict, start: str, end: str) -> pd.DataFrame: 
    '''This functions takes in 3 argument
    
            stocks: A dictionary of stock names and their listed tickers
            start: A date to for start of data, format 'YYYY-MM-DD'
            end: A date for end of date, format 'YYYY-MM-DD'

        returns a: 
            pandas dataframe
    '''

    #Create an empty list for dataframes
    dfs = []
    for stock,ticker in stocks.items():
        print(f"Getting data from {stock} : '{ticker}'")

        df = yf.download(tickers=ticker, start=start,end=end).reset_index()
        df.columns = df.columns.str.lower()
        df['stock'] = stock
        df['ticker'] = ticker

        df['5_day_ma_close'] = df['close'].rolling(5,min_periods=1).mean()
        df['10_day_ma_close'] = df['close'].rolling(10,min_periods=1).mean()

        df['5_day_ma_volume'] = df['volume'].rolling(5,min_periods=1).mean()
        df['10_day_ma_volume'] = df['volume'].rolling(10,min_periods=1).mean()

        df['daily_return'] = np.log(df['close']/df['open'])
        df['cum_return'] = df['daily_return'].cumsum()
        
        df['5_day_return'] = df['daily_return'].rolling(5,min_periods=1).sum()
        df['10_day_return'] = df['daily_return'].rolling(10,min_periods=1).sum()
        
        df['5_day_ma_return'] = df['daily_return'].rolling(5,min_periods=1).mean()
        df['10_day_ma_return'] = df['daily_return'].rolling(10,min_periods=1).mean()
        

        df = df[['date','stock','ticker','open',
                 'close','5_day_ma_close','10_day_ma_close',
                 'volume','5_day_ma_volume','10_day_ma_volume',
                 'daily_return','cum_return','5_day_return','10_day_return',
                 '5_day_ma_return', '10_day_ma_return']]

        dfs.append(df)

    df = pd.concat(dfs,axis=0)
    
    return df


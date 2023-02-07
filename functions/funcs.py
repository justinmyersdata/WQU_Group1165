import yfinance as yf
import pandas as pd
import numpy as np



def generate_data(stocks, start, end):
    '''This functions takes in 3 argument
    
            stocks: A dictionary of stock names and their listed tickers
            start: A date to for start of data, format 'YYYY-MM-DD'
            end: A date for end of date, format 'YYYY-MM-DD'
    '''

    #Create an empty list for dataframes
    dfs = []
    for stock,ticker in stocks.items():
        print(f"Getting data from {stock} : '{ticker}'")

        df = yf.download(tickers=ticker, start=start,end=end).reset_index()
        df.columns = df.columns.str.lower()
        df['stock'] = stock
        df['ticker'] = ticker
        df = df[['date','stock','ticker','open','close','volume']]
        df['return'] = np.log(df['close']/df['open'])


        dfs.append(df)

    df = pd.concat(dfs,axis=0)
    
    return df


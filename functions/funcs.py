import yfinance as yf
import pandas as pd
import numpy as np
from .pandas_funcs import buy_or_sell






def generate_data(stocks: dict, start: str, end: str, band:int, windows: list, initial: float) -> pd.DataFrame: 
    '''This functions takes in 3 argument
    
            stocks: A dictionary of stock names and their listed tickers
            start: A date to for start of data, format 'YYYY-MM-DD'
            end: A date for end of date, format 'YYYY-MM-DD'
            band: size of standard deviations to compare buy or sell signal
            windos: A list of windows used to calculate moving averages and std

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

        df['initial'] = initial

        df['cash'] = df['initial']
        df['shares'] = 0
        df['shares_value'] = 0

        df['daily_price_change'] = df['close'] - df['open']

        df['5_day_ma_close'] = df['close'].rolling(5,min_periods=1).mean()
        df['10_day_ma_close'] = df['close'].rolling(10,min_periods=1).mean()

        df['5_day_ma_volume'] = df['volume'].rolling(5,min_periods=1).mean()
        df['10_day_ma_volume'] = df['volume'].rolling(10,min_periods=1).mean()

        df['daily_return'] = np.log(df['close']/df['open'])
        df['cum_return'] = df['daily_return'].cumsum()
        
        df['5_day_return'] = df['daily_return'].rolling(5,min_periods=1).sum()
        df['10_day_return'] = df['daily_return'].rolling(10,min_periods=1).sum()
        
        df['5_day_ma_return'] = df['daily_return'].rolling(5,min_periods=1).mean()
        df['5_day_ma_return_std'] = df['daily_return'].rolling(5,min_periods=1).std()

        df['10_day_ma_return'] = df['daily_return'].rolling(10,min_periods=1).mean()
        df['10_day_ma_return_std'] = df['daily_return'].rolling(10,min_periods=1).std()

        df['30_day_ma_return'] = df['daily_return'].rolling(30,min_periods=1).mean()
        df['30_day_ma_return_std'] = df['daily_return'].rolling(30,min_periods=1).std()
        
        df['60_day_ma_return'] = df['daily_return'].rolling(60,min_periods=1).mean()
        df['60_day_ma_return_std'] = df['daily_return'].rolling(60,min_periods=1).std()

        df['90_day_ma_return'] = df['daily_return'].rolling(90,min_periods=1).mean()
        df['90_day_ma_return_std'] = df['daily_return'].rolling(90,min_periods=1).std()

        for window in windows:
            df[f'buy_or_sell_next_day_{window}'] = df.apply(buy_or_sell,size=window,band=band,axis=1)
            df[f'buy_or_sell_{window}'] = df[f'buy_or_sell_next_day_{window}'].shift(1)

        df['return_flag'] = 0
        df.loc[df['daily_return']>0, 'return_flag'] = 1
        

        df = df[['date','stock','ticker','open','close'
                 ,'5_day_ma_close','10_day_ma_close'
                 ,'volume','5_day_ma_volume','10_day_ma_volume'
                 ,'daily_return','cum_return'
                 ,'5_day_return','10_day_return'
                 ,'5_day_ma_return', '5_day_ma_return_std'
                 ,'10_day_ma_return', '10_day_ma_return_std'
                 ,'30_day_ma_return','30_day_ma_return_std'
                 ,'60_day_ma_return','60_day_ma_return_std'
                 ,'90_day_ma_return','90_day_ma_return_std','return_flag'
                 ,'buy_or_sell_5'
                 ,'buy_or_sell_10','buy_or_sell_30'
                 ,'buy_or_sell_60','buy_or_sell_90'
                 ,'daily_price_change', 'initial'
                 , 'shares', 'shares_values']]

        dfs.append(df)

    df = pd.concat(dfs,axis=0)
    
    return df

def agg_stats(df,windows):

    for window in windows:
        print('---------------------------------------')
        print(pd.pivot_table(df, values='stock', 
                                index=f'buy_or_sell_{window}', 
                                columns='return_flag', 
                                aggfunc=np.count_nonzero))
        
        print('---------------------------------------')
        
        print(pd.pivot_table(df, values='daily_return', 
                                index=f'buy_or_sell_{window}', 
                                columns='return_flag', 
                                aggfunc=np.sum))
        
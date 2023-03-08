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
            windows: A list of windows used to calculate moving averages and std
            initial: Initial dollar amount of portfolio


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

        df['initial'] = 0
        df.loc[0,'initial'] = initial

        df['daily_price_change'] = df['close'] - df['open']

        df['5_day_ma_close'] = df['close'].rolling(5,min_periods=1).mean()
        df['10_day_ma_close'] = df['close'].rolling(10,min_periods=1).mean()

        df['5_day_ma_volume'] = df['volume'].rolling(5,min_periods=1).mean()
        df['10_day_ma_volume'] = df['volume'].rolling(10,min_periods=1).mean()

        df['daily_return'] = np.log(df['close']/df['open'])
        df['cum_return'] = df['daily_return'].cumsum()

        df['5_day_return'] = df['daily_return'].rolling(5,min_periods=1).sum()
        df['10_day_return'] = df['daily_return'].rolling(10,min_periods=1).sum()

        df['return_flag'] = 0
        df.loc[df['daily_return']>0, 'return_flag'] = 1


        for window in windows:
            df[f'cash_{window}'] = df['initial']
            df[f'shares_{window}'] = 0
            df[f'shares_value_{window}'] = 0

            df[f'{window}_day_ma_return'] = df['daily_return'].rolling(window,min_periods=1).mean()
            df[f'{window}_day_ma_return_std'] = df['daily_return'].rolling(window,min_periods=1).std()

            df[f'buy_or_sell_next_day_{window}'] = df.apply(buy_or_sell,size=window,band=band,axis=1)
            df[f'buy_or_sell_{window}'] = df[f'buy_or_sell_next_day_{window}'].shift(1)

        
        for i in range(1, len(df)):

            for window in windows:
                if df.loc[i, f'buy_or_sell_{window}'] == 1:
                    df.loc[i, f'shares_{window}'] = df.loc[i-1, f'cash_{window}']/df.loc[i, 'open'] + df.loc[i-1, f'shares_{window}']
                    df.loc[i, f'cash_{window}'] = 0
                    df.loc[i, f'shares_value_{window}'] = df.loc[i-1, f'cash_{window}'] + df.loc[i-1, f'shares_{window}']*df.loc[i, 'open']
                
                elif df.loc[i, f'buy_or_sell_{window}'] == -1:
                    df.loc[i, f'cash_{window}'] = df.loc[i-1, f'shares_{window}']*df.loc[i, 'open'] + df.loc[i-1, f'cash_{window}']
                    df.loc[i, f'shares_{window}'] = 0
                    df.loc[i, f'shares_value_{window}'] = 0
            
                else:
                    df.loc[i, f'cash_{window}'] = df.loc[i-1, f'cash_{window}']
                    df.loc[i, f'shares_{window}'] = df.loc[i-1, f'shares_{window}']
                    df.loc[i, f'shares_value_{window}'] = df.loc[i, f'shares_{window}']*df.loc[i, 'open']

            
            
        for window in windows:
            df[f'portfolio_value_{window}'] = df[[f'cash_{window}',f'shares_value_{window}']].max(axis=1)
        
        fixed_columns = ['date','stock','ticker','open','close'
                        ,'5_day_ma_close','10_day_ma_close'
                        ,'volume','5_day_ma_volume','10_day_ma_volume'
                        ,'daily_return','cum_return'
                        ,'5_day_return','10_day_return'
                        ,'daily_price_change', 'initial']
        
        gen_columns = []
        for window in windows:
            gen_columns += [f'{window}_day_ma_return', f'{window}_day_ma_return_std'
                            , f'buy_or_sell_{window}', f'buy_or_sell_next_day_{window}'
                            , f'cash_{window}',f'shares_{window}', f'shares_value_{window}'
                            , f'portfolio_value_{window}']


        df = df[fixed_columns+gen_columns]

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
        
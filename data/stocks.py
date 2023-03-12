#Needs these to run file individually
#import sys
#sys.path.append("C:/Users/JustinMyers/Documents/WQU_Group1165")


from functions.funcs import generate_data
from matplotlib import pyplot as plt
import sys

def main(tickers,start='2017-01-01',end='2022-12-31',band=2,windows=[5,10,30,60,90],initial=1000):
    #Stocks we will be looking at
    # tickers = {'Apple':'AAPL',
    #             'Coca-Cola':'KO',
    #             'J&J':'JNJ',
    #             'American Express':'AXP',
    #             'Nike':'NKE',
    #             'JP Morgan':'JPM',
    #             'Starbucks':'SBUX',
    #             'S&P': 'SPY'}
    if len(tickers)<1:
        tickers = ['AAPL','SPY']


    df = generate_data(tickers=tickers,start=start,end=end,band=band, windows=windows,initial=initial)

    df.to_csv("C:/Users/JustinMyers/Desktop/Justin.csv")

    print(df.head())


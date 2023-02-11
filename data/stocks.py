from functions.funcs import generate_data
from matplotlib import pyplot as plt

#Stocks we will be looking at
stocks = {'Apple':'AAPL',
            'Coca-Coke':'KO',
            'J&J':'JNJ',
            'American Express':'AXP',
            'Nike':'NKE',
            'JP Morgan':'JPM',
            'Starbucks':'SBUX',
            'S&P': 'SPY'}


df = generate_data(stocks=stocks,start='2017-01-01',end='2022-12-31')

apple_df = df[df['stock']=='Apple']

plt.plot(apple_df['date'],apple_df['open'])
plt.plot(apple_df['date'],apple_df['close'])
plt.show()


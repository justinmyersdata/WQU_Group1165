from functions.funcs import generate_data

#Stocks we will be looking at
stocks = {'Apple':'AAPL',
            'Coca-Coke':'KO',
            'J&J':'JNJ',
            'American Express':'AXP',
            'Nike':'NKE',
            'JP Morgan':'JPM',
            'Starbucks':'SBUX'}

df = generate_data(stocks=stocks,start='2017-01-01',end='2022-12-31')
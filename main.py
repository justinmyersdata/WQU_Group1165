from data.stocks import main
import sys


"""Example call of main function
python main.py AAPL,SPY,VOO 2020-01-01 2021-01-01 2 30,60,90 1000 /data.csv
OR
python main.py
"""
if __name__=='__main__':

    if len(sys.argv)==1:
        main()
    
    else:
        tickers = sys.argv[1].split(',')
        start = sys.argv[2]
        end = sys.argv[3]
        band = 4
        windows = [int(x) for x in sys.argv[5].split(',')]
        initial = float(sys.argv[6])

        path = sys.argv[7] if len(sys.argv) > 7 else None
        
        main(tickers=tickers
            ,start=start
            ,end=end
            ,band=band
            ,windows=windows
            ,initial=initial
            ,path=path)
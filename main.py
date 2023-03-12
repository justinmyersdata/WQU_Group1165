from data.stocks import main
import sys

if __name__=='__main__':

    tickers = sys.argv[1].split(',')
    start = sys.argv[2]
    end = sys.argv[3]
    band = 4
    windows = [int(x) for x in sys.argv[5].split(',')]
    initial = float(sys.argv[6])
    
    main(tickers=tickers
        ,start=start
        ,end=end
        ,band=band
        ,windows=windows
        ,initial=initial)
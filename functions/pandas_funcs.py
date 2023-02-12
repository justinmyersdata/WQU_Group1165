

def buy_or_sell(row,size,band):
    if row[f'{size}_day_ma_return'] + band*row[f'{size}_day_ma_return_std'] < row['daily_return']:
        return 1
    elif row[f'{size}_day_ma_return'] - band*row[f'{size}_day_ma_return_std'] > row['daily_return']:
        return -1
    else:
        return 0
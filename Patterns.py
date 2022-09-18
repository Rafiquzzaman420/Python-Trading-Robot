"""
Patterns don't work in stock market and this is the proof
May be some patterns will form after some period of time but
that doesn't have any significant effect on the market direction
"""

import MetaTrader5 as mt
import pandas as pd
import CandleStick as cs
import matplotlib.pylab as plt


def initialization_check():
    if not mt.initialize():
        print('Initialization failed.\nError code : ', mt.last_error())
        quit()


def patterns():
    asset = 'EURUSDm'
    total_bar = 1000
    price_rates = pd.DataFrame(mt.copy_rates_from_pos(asset, mt.TIMEFRAME_M1, 0, total_bar))
    price_rates['time'] = pd.to_datetime(price_rates['time'], unit='s')
    open_price = []
    close_price = []
    high_price = []
    low_price = []

    # Reading the last 10 elements from the dataframe
    for i in reversed(range(0, 999)):
        open_price.append(price_rates.at[i, 'open'])
        close_price.append(price_rates.at[i, 'close'])
        high_price.append(price_rates.at[i, 'high'])
        low_price.append(price_rates.at[i, 'low'])

    position = 0
    times = 0
    pattern = []
    # with open('patterns.txt', mode='w') as writer:
    while position < 999:
        if open_price[position - 1] > close_price[position - 1] \
                and open_price[position] < close_price[position] \
                and open_price[position - 1] >= open_price[position] \
                and close_price[position - 1] <= close_price[position]:
            print('Inside Bar Pattern Detected.\nTime : ', price_rates.at[position, 'time'])
            times += 1
            # writer.write(str(cs.candlestickpatterncode(open_price[position],
            #                                            high_price[position],
            #                                            low_price[position],
            #                                            close_price[position])) + '\n')
            #
            # pattern.append(cs.candlestickpatterncode(open_price[position],
            #                                          high_price[position],
            #                                          low_price[position],
            #                                          close_price[position]))
            position += 1
        else:
            position = position + 1
    print('Inside bar found : '+str(times)+' times')


    # plt.figure(figsize=(50, 30))
    # plt.plot(pattern)
    # plt.show()


initialization_check()
patterns()

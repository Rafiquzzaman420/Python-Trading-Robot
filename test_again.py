from time import sleep
from matplotlib import pyplot as plt
from Functions import exponential_moving_average, price_data_frame, speaker, stochastic_crossover, time_converter
import MetaTrader5 as meta
from ta.momentum import rsi

while True:
    bars = 1000
    dataframe = price_data_frame('GBPUSDm', meta.TIMEFRAME_M1, bars)
    very_fast_ma, fast_ma, slow_ma, current_time = ([] for i in range(4))
    exponential_moving_average(dataframe)
    stoch_list = stochastic_crossover(dataframe, bars)
    for i in reversed(range(bars)):
        very_fast_ma.append(dataframe.at[i, 'Vfast_EMA'])
        fast_ma.append(dataframe.at[i, 'Fast_EMA'])
        slow_ma.append(dataframe.at[i, 'Slow_EMA'])
        current_time.append(dataframe.at[i, 'time'])

    time_difference = int(abs(current_time[1] - stoch_list[0][1]) / 60)

    if  very_fast_ma[0] > fast_ma[0] > slow_ma[0] and stoch_list[0][0] == 'buy' and time_difference <= 2:
        print('==================================')
        print('BUY   : ', time_converter(stoch_list[0][1]))
        print('==================================')
        speaker('UP', 10)
    if  very_fast_ma[0] < fast_ma[0] and fast_ma[0] > slow_ma[0] and stoch_list[0][0] == 'buy' and time_difference <= 2:
        print('==================================')
        print('Buy   : ', time_converter(stoch_list[0][1]))
        print('==================================')
        speaker('Short up', 5)
    if very_fast_ma[0] < fast_ma[0] < slow_ma[0] and stoch_list[0][0] == 'sell' and time_difference <= 2:
        print('==================================')
        print('SELL  : ', time_converter(stoch_list[0][1]))
        print('==================================')
        speaker('DOWN', 10)
    if very_fast_ma[0] > fast_ma[0] and fast_ma[0] < slow_ma[0] and stoch_list[0][0] == 'sell' and time_difference <= 2:
        print('==================================')
        print('Sell  : ', time_converter(stoch_list[0][1]))
        print('==================================')
        speaker('Short down', 5)
        

    sleep(30)
from matplotlib import pyplot as plt
from Functions import price_data_frame, time_converter, stochastic_crossover, rsi_crossover, speaker
import MetaTrader5 as meta
import numpy as np
from ta.utils import _sma
from time import sleep
import time as tm

while True:
# Use 5 minutes timeframe to identify the proper trend
    bars = 100
    dataframe = price_data_frame('GBPUSD', meta.TIMEFRAME_M1, bars)
    open = dataframe['open']
    close = dataframe['close']
    high = dataframe['high']
    low = dataframe['low']
    volume = dataframe['tick_volume']
    time = dataframe['time']
    rsi_list = rsi_crossover(close, time)
    stoch_list = stochastic_crossover(high, low, close, time)
    rsi_np_list = np.array(rsi_list)
    stoch_np_list = np.array(stoch_list)
    rsi_size = np.shape(rsi_np_list)
    stoch_size = np.shape(stoch_np_list)
    time_difference = abs(rsi_list[0][1] - stoch_list[0][1]) / 60
    line_graph_sma = _sma(close, 14)
    # Change time difference to 10 minutes for 5 minute charts
    if ((tm.time()+7200) - rsi_list[0][1]) <= 120:
        if rsi_list[0][0] == 'buy' and stoch_list[0][0] == 'buy' and time_difference <= 2:
            
            print('===============================================')
            print('BUY  : ', time_converter(rsi_list[0][1]))
            print('===============================================')
            speaker('BUY', 10)
        if rsi_list[0][0] == 'sell' and stoch_list[0][0] == 'sell' and time_difference <= 2:
            print('===============================================')
            print('SELL : ', time_converter(rsi_list[0][1]))
            print('===============================================')
            speaker('SELL', 10)

    sleep(30)    

'''
TODO:
1. Create an MACD Line crossover function (Though it works without MACD)
2. Create a Line chart crossover function using 14 simple moving average
3. Combine MACD and Line chart system with RSI and Stochastic (MACD: Optional)
'''
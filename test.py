from matplotlib import pyplot as plt
from functions import price_data_frame, time_converter, stochastic_crossover, rsi_crossover
import MetaTrader5 as meta
import numpy as np
# Use 5 minutes timeframe to identify the proper trend
bars = 100
dataframe = price_data_frame('GBPUSDm', meta.TIMEFRAME_M1, bars)
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
for i in range(rsi_size[0]):
    for j in range(stoch_size[0]):
        time_difference = abs(rsi_list[i][1] - stoch_list[j][1]) / 60
        # Change time difference to 10 minutes for 5 minute charts
        if rsi_list[i][0] == 'buy' and stoch_list[j][0] == 'buy' and time_difference <= 10:
            print('BUY  : ', time_converter(rsi_list[i][1]))
        if rsi_list[i][0] == 'sell' and stoch_list[j][0] == 'sell' and time_difference <= 10:
            print('SELL : ', time_converter(rsi_list[i][1]))

#=========================Hard Work=============================
# TODO : Need to determine the RSI divergence (Trend detection)
# TODO : RSI_line - MA_line <= 7 and cross_over <= 50 >=
# TODO : Need to determine the slope or divergence of EMA (Both)
#===============================================================
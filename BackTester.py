from matplotlib import pyplot as plt
from Functions import price_data_frame, time_converter, line_graph_crossover
import MetaTrader5 as meta
import numpy as np

bars = 50
dataframe = price_data_frame('GBPUSD', meta.TIMEFRAME_M1, bars)
close = dataframe['close']
time = dataframe['time']
cross = line_graph_crossover(close, time)
cross_array = np.array(cross)
cross_size = np.shape(cross_array)
for i in range(cross_size[0]):
    print(f'{cross[i][0]} : {time_converter(cross[i][1])}')
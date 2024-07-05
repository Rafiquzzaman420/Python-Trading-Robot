from matplotlib import pyplot as plt
from functions import price_data_frame, time_converter
import MetaTrader5 as meta
from ta.utils import _sma
import numpy as np
import pandas as pd

bars = 1440
dataframe = price_data_frame('GBPUSDm', meta.TIMEFRAME_M1, bars)
open = dataframe['open'].tolist()
high = dataframe['high'].tolist()
low = dataframe['low'].tolist()
close = dataframe['close'].tolist()
time = dataframe['time'].tolist()
info = []
for i in range(bars-1):
    if open[i+1] - close[i+1] == 0 or high[i+1] - low[i+1] == 0:
        info.append(50)
    else:
        calc = ((open[i+1] - close[i+1]) / (high[i+1] - low[i+1])) * 100
        info.append(calc)
        
info = pd.DataFrame(info)
info_sma = _sma(info, 14)
info_sma_sma = _sma(info_sma, 14)

plt.plot(info_sma, color='green')
# plt.plot(info_sma_sma, color='red')
plt.hlines([0, 40], [0, 1440], [1440, 0], color='lightgray')
plt.hlines([0, -40], [0, 1440], [1440, 0], color='lightgray')
plt.show()
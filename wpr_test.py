from matplotlib import pyplot as plt
from Functions import price_data_frame, time_converter
import MetaTrader5 as meta
from pandas_ta import stoch, willr
from ta.trend import macd, macd_signal
from ta.utils import _sma
import numpy as np

bars = 200
dataframe = price_data_frame('GBPUSDm', meta.TIMEFRAME_M1, bars)
high = dataframe['high']
low = dataframe['low']
close = dataframe['close']
time = dataframe['time']
wpr = willr(high, low, close, 200)
wpr_sma = _sma(wpr, 14)
plt.plot(wpr, color='green')
plt.plot(wpr_sma, color='red')
plt.show()
from matplotlib import pyplot as plt
from Functions import price_data_frame, stochastic_crossover, RSI_Divergence
import MetaTrader5 as meta
import numpy as np
from pandas_ta import tema, dema, ema, rsi

bars = 500
dataframe = price_data_frame('GBPUSDm', meta.TIMEFRAME_M1, bars)
open = dataframe['open']
close = dataframe['close']
high = dataframe['high']
low = dataframe['low']
# TEMA = tema(close, 200).tolist()
# DEMA = dema(close, 50).tolist()
# EMA = ema(close, 200).tolist()
peaks = RSI_Divergence(close)
print(peaks)

# TEMA.reverse()
# DEMA.reverse()
# EMA.reverse()
# print(TEMA)
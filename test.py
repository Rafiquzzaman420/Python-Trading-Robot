from matplotlib import pyplot as plt
from Functions import DEMA, TEMA, exponential_moving_average, price_data_frame
import MetaTrader5 as meta
import numpy as np


bars = 1440
dataframe = price_data_frame('GBPUSDm', meta.TIMEFRAME_M1, bars)
tema = TEMA(dataframe)
dema = DEMA(dataframe)
exponential_moving_average(dataframe)
ema = []
for i in range(bars):
    ema.append(dataframe.at[i, 'Slow_EMA'])

plt.plot(tema, color='dodgerblue')
plt.plot(dema, color='green')
plt.plot(ema, color='red')
plt.show()

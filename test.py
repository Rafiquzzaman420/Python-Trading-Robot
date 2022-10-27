from Functions import price_data_frame, store_levels
import MetaTrader5 as meta
import numpy as np

bars = 1200
dataframe = price_data_frame('GBPUSDm', meta.TIMEFRAME_H1, bars)
levels = store_levels(dataframe, .01)
print(levels)

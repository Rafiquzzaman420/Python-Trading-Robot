from Functions import initialization_check, price_data_frame, williams_R
import MetaTrader5 as meta

total_bars = 100
initialization_check()

dataframe = price_data_frame('EURUSDm', meta.TIMEFRAME_H1, total_bars)
signal = williams_R(14, dataframe, total_bars)
print(signal)

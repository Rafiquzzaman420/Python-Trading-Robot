from Functions import exponential_moving_average, initialization_check, price_data_frame
import MetaTrader5 as meta
from matplotlib import pyplot as plt

bars = 1000
initialization_check()
dataframe = price_data_frame('EURUSD', meta.TIMEFRAME_M1, bars)
exponential_moving_average(dataframe)
fast = []
slow = []
diff = []
for i in reversed(range(bars - 1)):
    fast.append(dataframe.at[i, 'Fast_EMA'])
    slow.append(dataframe.at[i, 'Slow_EMA'])

for i in range(len(fast) - 1):
    diff.append(abs(fast[i] - slow[i]))

plt.figure(figsize=(12,6))
plt.plot(diff)
plt.show()
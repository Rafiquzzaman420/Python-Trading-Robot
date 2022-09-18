"""
This program calculates the difference between stochastic line values and adds that into dataframe
"""
# It is a very sad things to say but this program really doesn't work the way I thought it might :(
# Waste of most valuable thing in the world and that it "TIME"
import matplotlib.pyplot as plt
import pandas as pd
import MetaTrader5 as meta


def initialization_check():
    if not meta.initialize():
        print('Initialization failed.\nError code : ', meta.last_error())
        quit()


def stochastic_indicator(dataframe, k, d, slow):
    close = dataframe['close']
    low = dataframe['low'].rolling(k).min()
    high = dataframe['high'].rolling(k).max()
    dataframe['%K_Fast'] = (close - low) * 100 / (high - low)
    dataframe['%K'] = dataframe['%K_Fast'].rolling(slow).mean()
    dataframe['%D'] = dataframe['%K'].rolling(d).mean()
    # axis = dataframe[['%K', '%D']].plot()
    # axis.axhline(20, linestyle='--', color="r")
    # axis.axhline(80, linestyle="--", color="r")
    # plt.show()
    return dataframe['%K'], dataframe['%D']


def exponential_moving_average(dataframe, fast=21, slow=300):
    dataframe['Fast_EMA'] = dataframe['close'].ewm(span=fast, adjust=False).mean()
    dataframe['Slow_EMA'] = dataframe['close'].ewm(span=slow, adjust=False).mean()
    return dataframe['Fast_EMA'], dataframe['Slow_EMA']


total_bars = 2000
initialization_check()
data_frame = pd.DataFrame(meta.copy_rates_from_pos('EURUSDm', meta.TIMEFRAME_M1, 0, total_bars))
data_frame['time'] = pd.to_datetime(data_frame['time'], unit='s')
stochastic_indicator(data_frame, 21, 3, 7)
exponential_moving_average(data_frame)
stoch_difference = []
difference = []
price_difference = []
fast_close_dif = []
fast_open_dif = []
slow_close_dif = []
slow_open_dif = []
for data in reversed(range(2000)):
    k_value = data_frame.at[data, '%K']
    d_value = data_frame.at[data, '%D']
    close_price = data_frame.at[data, 'close']
    fast_ema = data_frame.at[data, 'Fast_EMA']
    slow_ema = data_frame.at[data, 'Slow_EMA']
    open_price = data_frame.at[data, 'open']
    difference.append(abs(fast_ema - slow_ema))
    fast_close_dif.append(abs(close_price - fast_ema))
    fast_open_dif.append(abs(open_price - fast_ema))
    slow_close_dif.append(abs(close_price - slow_ema))
    slow_open_dif.append(abs(open_price - slow_ema))
    price_difference.append(abs(close_price - open_price))
    stoch_difference.append(abs(k_value - d_value))

data_frame['Stoch_Difference'] = list(reversed(stoch_difference))
data_frame['EMA_Difference'] = list(reversed(difference))
data_frame['Fast_Close'] = list(reversed(fast_close_dif))
data_frame['Fast_Open'] = list(reversed(fast_open_dif))
data_frame['Slow_Close'] = list(reversed(slow_close_dif))
data_frame['Price_Difference'] = list(reversed(price_difference))
data_frame['Slow_Open'] = list(reversed(slow_open_dif))

figure, axis = plt.subplots(2)
axis[1].plot(data_frame['time'], data_frame['Slow_Close'])
axis[0].plot(data_frame['time'], data_frame['Fast_Close'])
axis[1].grid()
axis[0].grid()
# data_frame.plot(x='time', y=['close', 'Fast_Close'])
plt.show()
# print(ma_and_close_difference)

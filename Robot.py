from datetime import datetime
from time import sleep
import MetaTrader5 as meta
import pandas as pd

import matplotlib.pyplot as plt
# import CandleStick

Total_bars = 1000


# ===================================================================================
def initialization_check():
    if not meta.initialize():
        print('Initialization failed.\nError code : ', meta.last_error())
        quit()


# ===================================================================================

# ===================================================================================
# For long term indication use (200, 20, 100)
# For short term indication use (21, 3, 7)
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


# ===================================================================================
# ===================================================================================
def exponential_moving_average(dataframe, fast=21, slow=200):
    dataframe['Fast_EMA'] = dataframe['close'].ewm(span=fast, adjust=False).mean()
    dataframe['Slow_EMA'] = dataframe['close'].ewm(span=slow, adjust=False).mean()
    return dataframe['Fast_EMA'], dataframe['Slow_EMA']


# ===================================================================================
# ===================================================================================
def ema_crossover_detection(dataframe):
    exponential_moving_average(dataframe)
    fast_ema = []
    slow_ema = []
    for info in reversed(range(799, 999)):
        fast_ema.append(dataframe.at[info, 'Fast_EMA'])
        slow_ema.append(dataframe.at[info, 'Slow_EMA'])


# ===================================================================================
# ===================================================================================
def stochastic_crossover_detection(dataframe):
    stochastic_indicator(dataframe, 21, 3, 7)
    k_line = []  # Fast Line
    d_line = []  # Slow Line
    for info in reversed(range(799, 999)):
        k_line.append(dataframe.at[info, '%K'])
        d_line.append(dataframe.at[info, '%D'])
    if k_line[1] > d_line[1] and k_line[0] < d_line[0]:
        return 'Crossover Detected. BUY'
    if k_line[1] < d_line[1] and k_line[0] > d_line[0]:
        return 'Crossover Detected. SELL'
    if k_line[0] < d_line[0] and k_line[1] <= 25 or d_line[1] <= 25:
        return 'BUY'
    if k_line[0] > d_line[0] and k_line[1] >= 75 or d_line[1] >= 75:
        return 'SELL'


# ===================================================================================
# ===================================================================================
def price_info(dataframe):
    open_price = []
    close_price = []
    high_price = []
    low_price = []

    # Reading the last 10 elements from the dataframe
    for i in reversed(range(989, 999)):
        open_price.append(dataframe.at[i, 'open'])
        close_price.append(dataframe.at[i, 'close'])
        high_price.append(dataframe.at[i, 'high'])
        low_price.append(dataframe.at[i, 'low'])


# ===================================================================================
# ===================================================================================
while True:
    initialization_check()

    EUR_USD = "EURUSDm"
    # Retrieving previous bar positions (Open, High, Low, Close, Tick Volume)
    price_rates = meta.copy_rates_from_pos(EUR_USD, meta.TIMEFRAME_M1, 0, Total_bars)
    meta.shutdown()
    # Converting into an easy-to-read pandas data frame
    framed_price = pd.DataFrame(price_rates)
    # Converting time
    framed_price['time'] = pd.to_datetime(framed_price['time'], unit='s')

    # Stochastic_indicator(framed_price_rates, 200, 20, 100) # Steep rise and fall detection
    stochastic_indicator(framed_price, 21, 3, 7)  # Buy and Sell signal generator
    # Dropping useless information
    # Stochastic function must be called before this function call
    framed_price = framed_price.drop(columns=['real_volume', '%K_Fast'])

    K_line = framed_price.at[Total_bars - 1, '%K']
    D_line = framed_price.at[Total_bars - 1, '%D']
    # Working completely fine
    if K_line > D_line:
        print("Market is going UP")
    else:
        print("Market is going DOWN")

    # Identifying correctly
    # print(price_info(framed_price))
    # pos = 0
    # print(CandleStick.CandleStickPatternCode(open_price[pos], high_price[pos], low_price[pos], close_price[pos]))
    # print(Exponential_Moving_Average(framed_price_rates))

    framed_price.plot(x='time', y=['%K', '%D'])
    plt.show()
    print(datetime.now())
    sleep(10)

# ===================================================================================

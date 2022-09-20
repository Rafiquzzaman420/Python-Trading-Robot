import MetaTrader5 as meta
import pandas as pd
import os
from datetime import datetime
import time
from time import sleep
from Functions import play_sound, price_data_frame,\
                    horizontal_line_values,\
                    store_levels,\
                    horizontal_line_position,\
                        stochastic_indicator,\
                        exponential_moving_average,\
                            trix_indicator


total_bars = 1000
time_now = time.time()
symbol = 'EURUSDm'
df = price_data_frame(symbol, meta.TIMEFRAME_M1, total_bars)
levels, output, difference, hline_position= ([] for i in range(4))
tuner = .001
store_levels(df, levels, tuner)
## plotter(levels, df)
# df['time'] = pd.to_datetime(df['time'], unit='s')
output = horizontal_line_values(levels)
stochastic_indicator(df, 100, 20, 30)
exponential_moving_average(df)

k_value, d_value, stick_value, fast_value, slow_value, time_value, tick_volume = ([] for i in range(7))

for i in reversed(range(total_bars)):
    current_stick = df.at[i, 'close']
    stoch_k_value = df.at[i, '%K']
    stoch_d_value = df.at[i, '%D']
    fast_ema = df.at[i, 'Fast_EMA']
    slow_ema = df.at[i, 'Slow_EMA']
    current_time = df.at[i, 'time']
    all_tick_volumes = df.at[i,'tick_volume']

    stick_value.append(current_stick)
    k_value.append(stoch_k_value)
    d_value.append(stoch_d_value)
    fast_value.append(fast_ema)
    slow_value.append(slow_ema)
    time_value.append(current_time)
    tick_volume.append(all_tick_volumes)


# current_time_value = [0]
# position_number = 0
# # This code doesn't work properly. Need to change it!
# for i in range(total_bars - 3):
#     # .0002 is the standard difference between moving averages
#     # Only needed for sell positions
#     ema_difference = abs(fast_value[i+1] - slow_value[i+1])
#     v = horizontal_line_position(total_bars - i, output, df, hline_position)
#     terminal_time = datetime.utcfromtimestamp(time_value[i+1]).strftime('%Y-%m-%d %H:%M:%S')
#     # if abs(current_time_value[-1] - time_value[i+1]) > 1250:
#     if slow_value[i+1] < fast_value[i+1] and tick_volume[i+1] >= 20:
#         if d_value[i+1] >= 35 and d_value[i+2] <= 35:
#             # if abs(int(time_now) - time_value[i+1]) <= 420:
#                 print('BUY (1)  --> {0} {1}: {2}'.format(k_value[i+1], d_value[i+1], terminal_time))
#                 # play_sound('buy')
#                 current_time_value.append(time_value[i+1])
#                 position_number += 1

#         if k_value[i+2] > d_value[i+2] and k_value[i+1] < d_value[1]\
#             and d_value[i+1] >= 65 and ema_difference >= 0.0002:
#             # if abs(int(time_now) - time_value[i+1]) <= 420:
#                 print('SELL (2) --> {0} {1}: {2}'.format(k_value[i+1], d_value[i+1], terminal_time))
#                 # play_sound('sell')
#                 current_time_value.append(time_value[i+1])
#                 position_number += 1

#     if slow_value[i+1] > fast_value[i+1] and tick_volume[i+1] >= 20:
#         if d_value[i+1] <= 65 and d_value[i+2] >= 65:
#             # if abs(int(time_now) - time_value[i+1]) <= 420:
#                 print('SELL (1) --> {0} {1}: {2}'.format(k_value[i+1], d_value[i+1], terminal_time))
#                 # play_sound('sell')
#                 current_time_value.append(time_value[i+1])
#                 position_number += 1

#         if d_value[i+1] >= 35 and ema_difference >= 0.0002 and d_value[i+2] <= 35:
#             # if abs(int(time_now) - time_value[i+1]) <= 420:
#                 print('BUY (2)  --> {0} {1}: {2}'.format(k_value[i+1], d_value[i+1], terminal_time))
#                 # play_sound('buy')
#                 current_time_value.append(time_value[i+1])
#                 position_number += 1
        
# # print(levels)


# # sleep(30)
# # clear = lambda: os.system('cls')
# # clear()

# TRIX working completely fine and really good though :)
print('{0:.6f}'.format(trix_indicator(5, total_bars, df)))

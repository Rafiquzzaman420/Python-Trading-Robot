from Functions import stochastic_indicator, \
                exponential_moving_average, \
                initialization_check, \
                price_data_frame, \
                stochastic_crossover_detection
import MetaTrader5 as meta

total_bars = 10000
initialization_check()
dataframe = price_data_frame('EURUSDm', meta.TIMEFRAME_M1, total_bars)
stochastic_indicator(dataframe, 21, 3, 7)
exponential_moving_average(dataframe, 21, 200)
k_line = []  # Fast Line
d_line = []  # Slow Line
time_now = []
close_pos = []
sell_time = []
buy_time = []
fast_ema = []
slow_ema = []
start_pos = total_bars - 1
stop_pos = total_bars - 1 - 1000
for info in reversed(range(stop_pos, start_pos)):
    k_line.append(dataframe.at[info, '%K'])
    d_line.append(dataframe.at[info, '%D'])
    time_now.append(dataframe.at[info, 'time'])
    close_pos.append([dataframe.at[info, 'close'], info])
    fast_ema.append([dataframe.at[info, 'Fast_EMA']])
    slow_ema.append([dataframe.at[info, 'Slow_EMA']])

for i in range(799):
    if fast_ema[i] < slow_ema[i] and \
        k_line[i + 1] > d_line[i + 1] and k_line[i] < d_line[i]:
        sell_time.append([close_pos[i][0], close_pos[i][1]])
        # print('SELL', close_pos[i])
    if fast_ema[i] > slow_ema[i] and \
        k_line[i + 1] < d_line[i + 1] and k_line[i] > d_line[i]:
        buy_time.append([close_pos[i][0], close_pos[i][1]])
        # print('BUY', close_pos[i])

def success_function(pos_type, time_list, data_frame):
    success = 0
    failure = 0
    for i in range(len(time_list) - 1): # 199
        closing_position = time_list[i][0] # 1.04546
        stick_number = time_list[i][1] - 8 # 986
        closing_pos = data_frame.at[stick_number, 'close']

        if pos_type == 'buy':
            if closing_pos - closing_position > 0:
                success += 1
            if closing_pos - closing_position < 0:
                failure += 1

        if pos_type == 'sell':
            if closing_position - closing_pos > 0:
                success += 1
            if closing_position - closing_pos < 0:
                failure += 1
            
    return success, failure

print(success_function('buy', buy_time, dataframe))
print(success_function('sell', sell_time, dataframe))
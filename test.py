from contextlib import closing
import MetaTrader5 as meta
from datetime import datetime
from Functions import buy_sell_signal, exponential_moving_average, initialization_check, price_data_frame, stochastic_indicator, trix

total_bars = 10000

initialization_check()
dataframe = price_data_frame('EURUSD', meta.TIMEFRAME_M1, total_bars)
close_position = []
time_list = []
period = 5
buy_info = []
sell_info = []

trix(period, dataframe)
stochastic_indicator(dataframe, 21, 5, 7)
exponential_moving_average(dataframe, 21, 200)
time_now = []
close_pos = []
k_value = []
d_value = []
ema_trix = []
trix_list = []
fast_ema = []
for info in reversed(range(0,total_bars)):
    k_value.append(dataframe.at[info, '%K'])
    d_value.append(dataframe.at[info, '%D'])
    time_now.append(dataframe.at[info, 'time'])
    close_pos.append(dataframe.at[info, 'close'])
    ema_trix.append(dataframe.at[info, 'EMA_3'])
    fast_ema.append(dataframe.at[info, 'Fast_EMA'])

for i in range(total_bars - 3):
    trix_list.append((ema_trix[i +1] - ema_trix[i + 2])/ema_trix[i +2])

for i in range(total_bars - 4):
    # if k_value[i + 2] < d_value[i + 2] and k_value[i + 1] > d_value[i + 1]\
    #     and d_value[i + 1] <= 30 and fast_ema[i+1] < close_pos[i+1]:
        if trix_list[i+1] <= 0 and trix_list[i] >= 0:
            buy_info.append([time_now[i+1], close_pos[i+1], i+1, 1])
            # print('Buy  : ', datetime.utcfromtimestamp(time_now[i]).strftime('%Y-%m-%d %H:%M:%S'))
    # if k_value[i + 2] > d_value[i + 2] and k_value[i + 1] < d_value[i + 1]\
    #     and d_value[i + 1] >= 70 and fast_ema[i+1] > close_pos[i+1]:
        if trix_list[i+1] >= 0 and trix_list[i] <= 0:
            sell_info.append([time_now[i+1], close_pos[i+1], i+1, -1])
            # print('Sell : ', datetime.utcfromtimestamp(time_now[i]).strftime('%Y-%m-%d %H:%M:%S'))

# print(buy_info)
# print(sell_info[0])
# print(dataframe.at[(total_bars - sell_info[0][2]+4), 'close'])
def validator(buy_sell_list, dataframe, total_bars):
    last_close = []
    for i in range(len(buy_sell_list)-1):
        fifth_close = dataframe.at[(total_bars - buy_sell_list[i][2]) + 5 , 'close']
        current_close = buy_sell_list[i][1]
        last_close.append([fifth_close, current_close, buy_sell_list[i][3]])
    return last_close

def success(last_close):
    success = 0
    failure = 0
    for i in range(len(last_close) - 1):
        if last_close[i][2] == 1:
            if (last_close[i][0] - last_close[i][1]) > 0:
                success += 1
            if last_close[i][0] - last_close[i][1] < 0:
                failure += 1
        if last_close[i][2] == -1:
            if (last_close[i][1] - last_close[i][0]) > 0:
                success += 1
            if last_close[i][1] - last_close[i][0] < 0:
                failure += 1
    return success, failure
            
print(success(validator(buy_info, dataframe, total_bars)))
print(success(validator(sell_info, dataframe, total_bars)))



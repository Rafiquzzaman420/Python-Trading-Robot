import MetaTrader5 as meta
import pandas as pd
from Functions import price_data_frame,\
                    horizontal_line_values,\
                    store_levels,\
                    horizontal_line_position,\
                        stochastic_indicator,\
                        exponential_moving_average

total_bars = 1000
symbol = 'EURUSDm'
df = price_data_frame(symbol, meta.TIMEFRAME_M1, total_bars)
levels, output, difference, hline_position= ([] for i in range(4))
tuner = .001
store_levels(df, levels, tuner)
df['time'] = pd.to_datetime(df['time'], unit='s')
horizontal_line_values(levels, output)
stochastic_indicator(df, 100, 20, 30)
exponential_moving_average(df)

k_value, d_value, stick_value, fast_value, slow_value, time_value = ([] for i in range(6))

for i in reversed(range(1000)):
    current_stick = df.at[i, 'close']
    stoch_k_value = df.at[i, '%K']
    stoch_d_value = df.at[i, '%D']
    fast_ema = df.at[i, 'Fast_EMA']
    slow_ema = df.at[i, 'Slow_EMA']
    current_time = df.at[i, 'time']

    stick_value.append(current_stick)
    k_value.append(stoch_k_value)
    d_value.append(stoch_d_value)
    fast_value.append(fast_ema)
    slow_value.append(slow_ema)
    time_value.append(current_time)

for i in range(1000):
    # if stick_value[i] > fast_value[i] > slow_value[i]:
        if k_value[i] > d_value[i] and k_value[i + 1] < d_value[i + 1] and \
            stick_value[i] > fast_value[i] and k_value[i] <= 35:
                v = horizontal_line_position(i, output, df, difference, hline_position)
                print('BUY  --> {0}: {1}'.format(v, time_value[i]))

    # if stick_value[i] < fast_value[i] < slow_value[i]:
        if k_value[i] < d_value[i] and k_value[i + 1] > d_value[i + 1] and \
             stick_value[i] < fast_value[i] and k_value[i] >= 65:
                v = horizontal_line_position(i, output, df, difference, hline_position)
                print('SELL --> {0}: {1}'.format(v, time_value[i]))
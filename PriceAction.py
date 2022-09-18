import MetaTrader5 as meta
import pandas as pd
from Functions import initialization_check as INIT
from CandleStick import candlestickpatterncode as cs
from Functions import StockPriceDataFrame

total_bars = 100


# Working Perfectly
def patterns(time_now, open_pos, high_pos, low_pos, close_pos):
    for cur in range(total_bars - 2):
        first = cur + 2
        second = cur + 1
        last = cur

        # # Bullish Engulfing
        # if (open_pos[second] - close_pos[second]) < (close_pos[last] - open_pos[last]) \
        #         and open_pos[second] < close_pos[last] and open_pos[last] < close_pos[last] \
        #         and close_pos[second] < open_pos[second]:
        #     if (cs(open_pos[last], high_pos[last], low_pos[last], close_pos[last]) in [1, 2, 3, 4]) \
        #             and (
        #             cs(open_pos[second], high_pos[second], low_pos[second], close_pos[second]) in [-1, -2, -3, -4]):
        #         print('Bullish Engulfing :{0}  {1}'.format(time_now[second], time_now[last]))

        # # Bearish Engulfing
        # if (close_pos[second] - open_pos[second]) < (open_pos[last] - close_pos[last]) \
        #         and open_pos[second] > close_pos[last] and open_pos[last] > close_pos[last] \
        #         and close_pos[second] > open_pos[second]:
        #     if (cs(open_pos[last], high_pos[last], low_pos[last], close_pos[last]) in [-1, -2, -3, -4]) \
        #             and (
        #             cs(open_pos[second], high_pos[second], low_pos[second], close_pos[second]) in [1, 2, 3, 4]):
        #         print('Bearish Engulfing :{0}  {1}'.format(time_now[second], time_now[last]))

        # # Evening Star
        # if open_pos[second] > open_pos[first] and high_pos[second] >= close_pos[first] and \
        #     high_pos[second] >= open_pos[last] and close_pos[second] > close_pos[last] and \
        #         (close_pos[first] - open_pos[first] > abs(open_pos[second] - close_pos[second])) and \
        #         (open_pos[last] - close_pos[last] > abs(open_pos[second] - close_pos[second])):
        #     if (cs(open_pos[last], high_pos[last], low_pos[last], close_pos[last]) in [-1, -2, -3, -4]) \
        #             and (cs(open_pos[second], high_pos[second], low_pos[second], close_pos[second]) in
        #                 (range(5, 20) or range(-5,-21,-1))) \
        #             and (cs(open_pos[first], high_pos[first], low_pos[first], close_pos[first]) in [1, 2, 3, 4]):
        #         print('Evening Star : {0}  {1}'.format(time_now[first], time_now[last]))

        # # Morning Star
        # if open_pos[second] < open_pos[first] and low_pos[second] <= close_pos[first] and \
        #     low_pos[second] <= open_pos[last] and open_pos[second] < close_pos[last] and \
        #         (open_pos[first] - close_pos[first] > abs(open_pos[second] - close_pos[second])) and \
        #         (close_pos[last] - open_pos[last] > abs(open_pos[second] - close_pos[second])):
        #     if (cs(open_pos[first], high_pos[first], low_pos[first], close_pos[first]) in [-1, -2, -3, -4]) \
        #             and (cs(open_pos[second], high_pos[second], low_pos[second], close_pos[second]) in
        #                 (range(5, 20) or range(-5,-21,-1))) \
        #             and (cs(open_pos[last], high_pos[last], low_pos[last], close_pos[last]) in [1, 2, 3, 4]):
        #         print('Morning Star : {0}  {1}'.format(time_now[first], time_now[last]))
        
        # # Harami Patterns
        # if (abs(open_pos[first] - close_pos[first]) > abs(open_pos[second] - close_pos[second])) and \
        # (cs(open_pos[first], high_pos[first], low_pos[first], close_pos[first])\
        # and (cs(open_pos[second], high_pos[second], low_pos[second], close_pos[second]))) in \
        #             [-1, -2, -3, -4, 1, 2, 3, 4]:
            
        #     # Bullish Harami
        #     if open_pos[first] > close_pos[second] and close_pos[first] < open_pos[second]:
        #         print('Bullish Harami : {0}  {1}'.format(time_now[first], time_now[second]))

        #     # Bearish Harami
        #     if open_pos[first] < close_pos[second] and close_pos[first] > open_pos[second]:
        #         print('Bearish Harami : {0}  {1}'.format(time_now[first], time_now[second]))
        
        if (cs(open_pos[first], high_pos[first], low_pos[first], close_pos[first]) and
            cs(open_pos[second], high_pos[second], low_pos[second], close_pos[second]) and\
            cs(open_pos[last], high_pos[last], low_pos[last], close_pos[last]))  in \
            [1, 2, 3, 4, -1, -2, -3, -4]:
        # Three White Soldiers
            if open_pos[first] < open_pos[second] < open_pos[last] and \
                close_pos[first] < close_pos[second] < close_pos[last]:
                print('Three White Soldiers : {0}  {1}'.format(time_now[first], time_now[last]))
            
            # Three Black Crows
            if open_pos[first] > open_pos[second] > open_pos[last] and \
                close_pos[first] > close_pos[second] > close_pos[last]:
                print('Three Black Crows    : {0}  {1}'.format(time_now[first], time_now[last]))

# #####################################################
# ################## Bullish Candle ###################
# #####################################################

framed_price = StockPriceDataFrame(total_bars, meta.TIMEFRAME_H1)
open, high, low, close, time = ([] for i in range(5))
for i in reversed(range(total_bars)):
    open.append(framed_price.at[i, 'open'])
    high.append(framed_price.at[i, 'high'])
    low.append(framed_price.at[i, 'low'])
    close.append(framed_price.at[i, 'close'])
    time.append(framed_price.at[i, 'time'])

patterns(time, open, high, low, close)

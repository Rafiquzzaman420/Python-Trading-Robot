
* ======================== Key Functions ======================== *
* MetaTrader5 Initialization Checker                              *
* Stochastic Indicator {21, 3, 7}                                 *
* Stochastic Crossover Detection {21, 3, 7}                       *
* Exponential Moving Average (200, 21)                            *
* EMA Crossover Detection (200, 21)                               *
* Price Action Detection                                          *
* =============================================================== *

* ========================== Algorithm ========================== *
# Time frame : All
# Accuracy : 100%
if stochastic_21_3_7 crossed_over_above_75_and_going_down:
    if open_price > EMA_21 and close_price > EMA_21 and /
    ((EMA_21 > EMA_200 and EMA_21 is_not_too_above EMA_200) or (EMA_21 < EMA_200 and EMA_21 is_too_below EMA_200)):
        Place Market Buy Order

if stochastic_21_3_7 crossed_over_above_25_and_going_up:
    if open_price < EMA_21 and close_price < EMA_21 and /
    ((EMA_21 < EMA_200 and EMA_21 is_not_too_below EMA_200) or (EMA_21 > EMA_200 and EMA_21 is_too_above EMA_200)):
        Place Market Sell Order

BULLISH_1 = 1
BULLISH_2 = 2
BULLISH_3 = 3
BULLISH_4 = 4
BULLISH_5 = 5
BULLISH_6 = 6
BULLISH_7 = 7
BULLISH_8 = 8
BULLISH_9 = 9
BULLISH_10 = 10
BULLISH_11 = 11
BULLISH_12 = 12
BULLISH_13 = 13
BULLISH_14 = 14
BULLISH_15 = 15
BULLISH_16 = 16
BULLISH_17 = 17
BULLISH_18 = 18
BULLISH_19 = 19
BULLISH_20 = 20

BEARISH_1 = -1
BEARISH_2 = -2
BEARISH_3 = -3
BEARISH_4 = -4
BEARISH_5 = -5
BEARISH_6 = -6
BEARISH_7 = -7
BEARISH_8 = -8
BEARISH_9 = -9
BEARISH_10 = -10
BEARISH_11 = -11
BEARISH_12 = -12
BEARISH_13 = -13
BEARISH_14 = -14
BEARISH_15 = -15
BEARISH_16 = -16
BEARISH_17 = -17
BEARISH_18 = -18
BEARISH_19 = -19
BEARISH_20 = -20


# TODO: Showing wrong information
def candlestickpatterncode(open, high, low, close):
    # ||==========================================================================================||
    # ||                           Bullish Candle Stick Logic starts here!                        ||
    # ||==========================================================================================||
    if high > close > open > low and ((close - open) >= (open - low)) and ((close - open) >= (high - close)):
        return BULLISH_1

    if high == close > open > low and ((close - open) >= (open - low)):
        return BULLISH_2

    if open < close == high and open == low:
        return BULLISH_3

    if low == open < close < high and ((close - open) >= (high - close)):
        return BULLISH_4

    if high > close > open > low and ((close - open) >= (high - close)) and ((close - open) >= (open - low)):
        return BULLISH_5

    if open < close == high and ((open - low) >= (close - open)):
        return BULLISH_6

    if open < close == high and ((open - low) <= (close - open)):
        return BULLISH_7

    if open < close == high and ((high - close) <= (close - open)):
        return BULLISH_8

    if high > close > open > low and ((close - open) >= (high - close)) and ((close - open) <= (open - low)) and \
            ((high - close) <= (open - low)):
        return BULLISH_9

    if high > close > open > low and ((close - open) <= (high - close)) and ((close - open) >= (open - low)):
        return BULLISH_10

    if high > close > open == low and ((high - close) >= (close - open)):
        return BULLISH_11

    if high > close > open > low and ((close - open) <= (high - close)) and ((close - open) <= (open - low)) and \
            ((open - low) <= (high - close)):
        return BULLISH_12

    if high > close > open > low and ((close - open) <= (high - close)) and ((close - open) <= (open - low)) and \
            ((high - close) <= (open - low)):
        return BULLISH_13

    if high > close > open > low and ((close - open) <= (high - close)) and ((close - open) <= (open - low)):
        return BULLISH_14

    if close == open and high == close and open == low:
        return BULLISH_15

    if close == open and high > close and open == low and ((high - close) == (high - open)):
        return BULLISH_16

    if close == open and high == close and open > low and ((high - low) == (open - low)):
        return BULLISH_17

    if close == open and high > close and open > low and ((high - close) <= (open - low)):
        return BULLISH_18

    if close == open and high > close and open > low and ((high - close) >= (open - low)):
        return BULLISH_19

    if close == open and high > close and open > low and ((high - close) == (open - low)):
        return BULLISH_20

    # ||==========================================================================================||
    # ||                           Bearish Candle Stick Logic starts here!                        ||
    # ||==========================================================================================||
    if high > open > close > low and ((open - close) >= (high - open)) and ((open - close) >= (close - low)):
        return BEARISH_1

    if high == open > close > low and ((open - close) >= (close - low)):
        return BEARISH_2

    if close < open == high and close == low:
        return BEARISH_3

    if low == close < open < high and ((open - close) >= (high - open)):
        return BEARISH_4

    if high > open > close > low and ((open - close) >= (high - open)) and ((open - close) >= (close - low)):
        return BEARISH_5

    if close < open == high and ((close - low) >= (open - close)):
        return BEARISH_6

    if close < open == high and ((close - low) <= (open - close)):
        return BEARISH_7

    if close < open == high and ((high - open) <= (open - close)):
        return BEARISH_8

    if high > open > close > low and ((open - close) >= (high - open)) and ((open - close) <= (close - low)) and \
            ((high - open) <= (close - low)):
        return BEARISH_9

    if high > open > close > low and ((open - close) <= (high - open)) and ((open - close) >= (close - low)):
        return BEARISH_10

    if high > open > close == low and ((high - open) >= (open - close)):
        return BEARISH_11

    if high > open > close > low and ((open - close) <= (high - open)) and ((open - close) <= (close - low)) and \
            ((close - low) <= (high - open)):
        return BEARISH_12

    if high > open > close > low and ((open - close) <= (high - open)) and ((open - close) <= (close - low)) and \
            ((high - open) <= (close - low)):
        return BEARISH_13

    if high > open > close > low and ((open - close) <= (high - open)) and ((open - close) <= (close - low)):
        return BEARISH_14

    if close == open and high == open and close == low:
        return BEARISH_15

    if close == open and high > open and close == low and ((high - open) == (high - low)):
        return BEARISH_16

    if open == close and high == open and close > low and ((high - low) == (close - low)):
        return BEARISH_17

    if close == open and high > open and close > low and ((high - open) < (close - low)):
        return BEARISH_18

    if close == open and high > open and close > low and ((high - open) > (close - low)):
        return BEARISH_19

    if open == close and high > open and close > low and ((high - open) == (close - low)):
        return BEARISH_20

    return 0

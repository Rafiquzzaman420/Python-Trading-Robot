bull = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
bear = [0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20]


def candle_stick_pattern(open, high, low, close):
    # ||==========================================================================================||
    # ||                           Bullish Candle Stick Logic                                     ||
    # ||==========================================================================================||
    if (
        high > close > open > low
        and ((close - open) >= (open - low))
        and ((close - open) >= (high - close))
    ):
        return bull[1]

    if high == close > open > low and ((close - open) >= (open - low)):
        return bull[2]

    if open < close == high and open == low:
        return bull[3]

    if low == open < close < high and ((close - open) >= (high - close)):
        return bull[4]

    if (
        high > close > open > low
        and ((close - open) >= (high - close))
        and ((close - open) >= (open - low))
    ):
        return bull[5]

    if open < close == high and ((open - low) >= (close - open)):
        return bull[6]

    if open < close == high and ((open - low) <= (close - open)):
        return bull[7]

    if open < close == high and ((high - close) <= (close - open)):
        return bull[8]

    if (
        high > close > open > low
        and ((close - open) >= (high - close))
        and ((close - open) <= (open - low))
        and ((high - close) <= (open - low))
    ):
        return bull[9]

    if (
        high > close > open > low
        and ((close - open) <= (high - close))
        and ((close - open) >= (open - low))
    ):
        return bull[10]

    if high > close > open == low and ((high - close) >= (close - open)):
        return bull[11]

    if (
        high > close > open > low
        and ((close - open) <= (high - close))
        and ((close - open) <= (open - low))
        and ((open - low) <= (high - close))
    ):
        return bull[12]

    if (
        high > close > open > low
        and ((close - open) <= (high - close))
        and ((close - open) <= (open - low))
        and ((high - close) <= (open - low))
    ):
        return bull[13]

    if (
        high > close > open > low
        and ((close - open) <= (high - close))
        and ((close - open) <= (open - low))
    ):
        return bull[14]

    if close == open and high == close and open == low:
        return bull[15]

    if (
        close == open
        and high > close
        and open == low
        and ((high - close) == (high - open))
    ):
        return bull[16]

    if (
        close == open
        and high == close
        and open > low
        and ((high - low) == (open - low))
    ):
        return bull[17]

    if (
        close == open
        and high > close
        and open > low
        and ((high - close) <= (open - low))
    ):
        return bull[18]

    if (
        close == open
        and high > close
        and open > low
        and ((high - close) >= (open - low))
    ):
        return bull[19]

    if (
        close == open
        and high > close
        and open > low
        and ((high - close) == (open - low))
    ):
        return bull[20]

    # ||==========================================================================================||
    # ||                           Bearish Candle Stick Logic                                     ||
    # ||==========================================================================================||
    if (
        high > open > close > low
        and ((open - close) >= (high - open))
        and ((open - close) >= (close - low))
    ):
        return bear[1]

    if high == open > close > low and ((open - close) >= (close - low)):
        return bear[2]

    if close < open == high and close == low:
        return bear[3]

    if low == close < open < high and ((open - close) >= (high - open)):
        return bear[4]

    if (
        high > open > close > low
        and ((open - close) >= (high - open))
        and ((open - close) >= (close - low))
    ):
        return bear[5]

    if close < open == high and ((close - low) >= (open - close)):
        return bear[6]

    if close < open == high and ((close - low) <= (open - close)):
        return bear[7]

    if close < open == high and ((high - open) <= (open - close)):
        return bear[8]

    if (
        high > open > close > low
        and ((open - close) >= (high - open))
        and ((open - close) <= (close - low))
        and ((high - open) <= (close - low))
    ):
        return bear[9]

    if (
        high > open > close > low
        and ((open - close) <= (high - open))
        and ((open - close) >= (close - low))
    ):
        return bear[10]

    if high > open > close == low and ((high - open) >= (open - close)):
        return bear[11]

    if (
        high > open > close > low
        and ((open - close) <= (high - open))
        and ((open - close) <= (close - low))
        and ((close - low) <= (high - open))
    ):
        return bear[12]

    if (
        high > open > close > low
        and ((open - close) <= (high - open))
        and ((open - close) <= (close - low))
        and ((high - open) <= (close - low))
    ):
        return bear[13]

    if (
        high > open > close > low
        and ((open - close) <= (high - open))
        and ((open - close) <= (close - low))
    ):
        return bear[14]

    if close == open and high == open and close == low:
        return bear[15]

    if (
        close == open
        and high > open
        and close == low
        and ((high - open) == (high - low))
    ):
        return bear[16]

    if (
        open == close
        and high == open
        and close > low
        and ((high - low) == (close - low))
    ):
        return bear[17]

    if (
        close == open
        and high > open
        and close > low
        and ((high - open) < (close - low))
    ):
        return bear[18]

    if (
        close == open
        and high > open
        and close > low
        and ((high - open) > (close - low))
    ):
        return bear[19]

    if (
        open == close
        and high > open
        and close > low
        and ((high - open) == (close - low))
    ):
        return bear[20]

    return 0

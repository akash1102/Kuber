import pandas_ta as ta

class Supertrend:
  def __init__(self,high,low,close):
    self.high = high
    self.low = low
    self.close = close

  def calculate_supertrend(self,period,multiplier):
    return ta.supertrend(high=self.high, low=self.low, close=self.close, period=period, multiplier=multiplier)
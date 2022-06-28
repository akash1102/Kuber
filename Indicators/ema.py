import pandas_ta as ta

class EMA:
  def __init__(self,close):
    self.close = close

  def calculate_ema(self,n):
    return ta.ema(self.close,n)
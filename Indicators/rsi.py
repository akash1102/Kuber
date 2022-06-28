import pandas_ta as ta

class RSI:
  def __init__(self,close):
    self.close = close

  def calculate_rsi(self,n):
    return ta.ema(self.close,n)
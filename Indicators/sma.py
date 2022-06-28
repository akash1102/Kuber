import pandas_ta as ta

class SMA:
  def __init__(self,close):
    self.close = close

  def calculate_sma(self,n):
    return ta.sma(self.close,n)
      
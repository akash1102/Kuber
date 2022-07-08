import pandas_ta as ta

class BollingerBands:
  def __init__(self,close):
    self.close = close

  def calculate_bbands(self,n):
    return ta.bbands(self.close,n)
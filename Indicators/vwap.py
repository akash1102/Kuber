import pandas_ta as ta

class VWAP:
  def __init__(self,low,close):
    self.low = low
    self.close = close

  def calculate_vwap(self,volume):
    return ta.vwap(self.low,self.close,volume)
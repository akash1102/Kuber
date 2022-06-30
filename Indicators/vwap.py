import pandas_ta as ta

class VWAP:
  def __init__(self,low,close,volume):
    self.low = low
    self.close = close
    self.volume = volume

  def calculate_vwap(self,volume):
    return ta.vwap(self.low,self.close,volume)
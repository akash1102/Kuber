import datetime
from asyncio.windows_events import NULL
from Utilities import kuberconstants

class SignalGenerator:
  def __init__(self,dataframe):
    self.dataframe = dataframe


  def GenerateSignal(self):
    now = datetime.datetime.now()
    today945am = now.replace(hour=9, minute=45, second=0)
    today230pm = now.replace(hour=14, minute=30, second=0)
    if (now > today945am) and (now < today230pm):
        self.dataframe[kuberconstants.BUY_EMA10_EMA20_RSI14] = ""
        self.dataframe[kuberconstants.SELL_EMA10_EMA20_RSI14] = ""
        for i in range(len(self.dataframe.index)):
            if (self.dataframe["EMA_10"] is not NULL) and (self.dataframe["EMA_21"] is not NULL) :
                dataframe_close = self.dataframe["close"][i]
                if(self.validateBuy(i,dataframe_close)):
                    self.dataframe[kuberconstants.BUY_EMA10_EMA20_RSI14][i] = "BUY"
                if(self.validateSell(i)):
                    self.dataframe[kuberconstants.SELL_EMA10_EMA20_RSI14][i] = "SELL"
                
    return self.dataframe

  def validateBuy(self,i,dataframe_close):
    return (self.dataframe["EMA_10"][i]>self.dataframe["EMA_21"][i]) and (self.dataframe["RSI_14"][i] > kuberconstants.RSI_64) and (dataframe_close > self.dataframe["EMA_10"][i]) and (dataframe_close > self.dataframe["EMA_21"][i]) and (self.dataframe["RSI_14"][i]> self.dataframe["RSI_100"][i])

  def validateSell(self,i):
    return (self.dataframe["RSI_14"][i]<self.dataframe["RSI_100"][i]) and (self.dataframe["EMA_10"][i]<self.dataframe["EMA_21"][i]) and (self.dataframe["RSI_14"][i] < kuberconstants.RSI_30 )

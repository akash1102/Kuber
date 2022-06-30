import datetime
from asyncio.windows_events import NULL
from pandas import DataFrame
from Utilities import kuberconstants
import time

class SignalGenerator:
  def __init__(self,dataframe):
    self.dataframe = dataframe

  def GenerateSignal(self):
    now = datetime.datetime.now()
    buyOrderPlaced = False
    sellOrderPlaced = False
    orderPlaced = False
    position_price = NULL
    PL = NULL
    self.dataframe[kuberconstants.BUY_EMA10_EMA20_RSI14] = ""
    self.dataframe[kuberconstants.SELL_EMA10_EMA20_RSI14] = ""
    self.dataframe[kuberconstants.PROFIT] = ""
    for i in range(len(self.dataframe.index)):
        if (self.dataframe["EMA_9"][i] is not NULL) and (self.dataframe["EMA_21"][i] is not NULL):
            if orderPlaced == False:
                if buyOrderPlaced == False:
                    if (self.dataframe["EMA_9"][i] > self.dataframe["EMA_21"][i]):# and (self.dataframe["RSI_14"][i] > 60) and (self.dataframe["close"][i] > self.dataframe["EMA_10"][i]) and (self.dataframe["close"][i] > self.dataframe["EMA_21"][i]):
                        self.dataframe[kuberconstants.BUY_EMA10_EMA20_RSI14][i] = "BUY_OPEN"
                        buyOrderPlaced = True
                        sellOrderPlaced = False
                        orderPlaced = True
                        position_price = self.dataframe["close"][i]
                        #print(position_price)
                if sellOrderPlaced == False:
                    if (self.dataframe["EMA_9"][i] < self.dataframe["EMA_21"][i]):# and (self.dataframe["RSI_14"][i] < 35) and   (self.dataframe["close"][i] < self.dataframe["EMA_9"][i]) and (self.dataframe["close"][i] < self.dataframe["EMA_21"][i]):
                        self.dataframe[kuberconstants.BUY_EMA10_EMA20_RSI14][i] = "SELL_OPEN"
                        sellOrderPlaced = True
                        buyOrderPlaced = False
                        orderPlaced = True
                        position_price = self.dataframe["close"][i]
            else : # Square off logic
                if buyOrderPlaced == True:
                    if (self.dataframe["EMA_9"][i] < self.dataframe["EMA_21"][i]):
                        self.dataframe[kuberconstants.BUY_EMA10_EMA20_RSI14][i] = "BUY_CLOSE"
                        buyOrderPlaced = False
                        sellOrderPlaced = False
                        orderPlaced = False
                        PL = position_price - self.dataframe["close"][i]
                        self.dataframe[kuberconstants.PROFIT][i] = PL
                if sellOrderPlaced == True:
                    if (self.dataframe["EMA_9"][i] > self.dataframe["EMA_21"][i]):
                        self.dataframe[kuberconstants.BUY_EMA10_EMA20_RSI14][i] = "SELL_CLOSE"
                        sellOrderPlaced = False
                        buyOrderPlaced = False
                        orderPlaced = False
                        PL = self.dataframe["close"][i] - position_price 
                        self.dataframe[kuberconstants.PROFIT][i] = PL
        #time.sleep(0.01)
    '''today945am = now.replace(hour=9, minute=45, second=0)
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
                    self.dataframe[kuberconstants.SELL_EMA10_EMA20_RSI14][i] = "SELL"'''
                
    return self.dataframe

  def validateBuy(self,i,dataframe_close):
    return (self.dataframe["EMA_9"][i]>self.dataframe["EMA_9"][i]) and (self.dataframe["RSI_14"][i] > kuberconstants.RSI_64) and (dataframe_close > self.dataframe["EMA_9"][i]) and (dataframe_close > self.dataframe["EMA_21"][i]) and (self.dataframe["RSI_14"][i]> self.dataframe["RSI_100"][i])

  def validateSell(self,i):
    return (self.dataframe["RSI_14"][i]<self.dataframe["RSI_100"][i]) and (self.dataframe["EMA_9"][i]<self.dataframe["EMA_21"][i]) and (self.dataframe["RSI_14"][i] < kuberconstants.RSI_30 )

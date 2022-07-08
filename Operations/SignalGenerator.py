from ast import If
#from copy import PyStringMap
import datetime
from asyncio.windows_events import NULL
from tkinter.tix import MAX
from numpy import greater_equal
from pandas import DataFrame
from pyparsing import null_debug_action
import pytz
from zmq import EVENT_CLOSED, PROTOCOL_ERROR_ZAP_BAD_REQUEST_ID
from Utilities import kuberconstants
import time

class SignalGenerator:

  def __init__(self,dataframe):
    self.dataframe = dataframe
 
  def GenerateSignal(self):
    now = datetime.datetime.now()
# using now() to get current time
    current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    buyOrderPlaced = False
    sellOrderPlaced = False
    orderPlaced = False
    position_price = NULL
    PL = NULL
    buy_signal_count = NULL
    sell_signal_count = NULL
    total_signal = NULL
    P_trade = NULL
    cummulative_loss = NULL
    cummulative_profit = NULL
    L_trade = NULL
    Profit_Max = NULL
    self.dataframe[kuberconstants.Status] = ""
    self.dataframe[kuberconstants.SELL_EMA10_EMA20_RSI14] = ""
    self.dataframe[kuberconstants.RESONCODE] = ""
    self.dataframe[kuberconstants.PROFIT] = ""
    self.dataframe[kuberconstants.PL_POSITION] = ""
    
    RSI_ARRAY = []
    print(self.dataframe.columns)
    for i in range(len(self.dataframe.index)):
        if int(str(self.dataframe["TIME"][i])[-8:].replace(":","")) >= 93000 and int(str(self.dataframe["TIME"][i])[-8:].replace(":","")) < 152500:
            previousEMA_9 = self.dataframe["EMA_9"][i-1]
            previuosEMA_18 = self.dataframe["EMA_18"][i-1]
            currentEMA_9 = self.dataframe["EMA_9"][i]
            currentEMA_18 = self.dataframe["EMA_18"][i]
            currentRSI_14 = self.dataframe["RSI_14"][i]
            previousRSI_14 = self.dataframe["RSI_14"][i-1]
            currentEMA_51 = self.dataframe["EMA_51"][i]
            if (self.dataframe["EMA_9"][i] is not NULL) and (currentEMA_18 is not NULL) and (currentEMA_51 is not NULL):
                if orderPlaced == False:
                    if buyOrderPlaced == False:
                         if ((previousEMA_9 < previuosEMA_18) and (currentEMA_9 > currentEMA_18)) and (currentRSI_14 > previousRSI_14*1.05):
                            self.dataframe[kuberconstants.Status][i] = "BUY_OPEN"
                            buyOrderPlaced = True
                            sellOrderPlaced = False
                            orderPlaced = True
                            position_price = self.dataframe["close"][i]
                            buy_signal_count = buy_signal_count +1
                            RSI_ARRAY.append(currentRSI_14)
                    if sellOrderPlaced == False:
                        if  (previousEMA_9 > previuosEMA_18 and (currentEMA_9 < currentEMA_18)) and (currentRSI_14 < previousRSI_14*0.95):
                            self.dataframe[kuberconstants.Status][i] = "SELL_OPEN"
                            sellOrderPlaced = True
                            buyOrderPlaced = False
                            orderPlaced = True
                            position_price = self.dataframe["close"][i]
                            sell_signal_count = sell_signal_count +1
                            RSI_ARRAY.append(currentRSI_14)
                else : # Square off logic
                    if buyOrderPlaced == True:
                        PL = self.dataframe["close"][i] - position_price
                        Profit_Max = max(Profit_Max, PL)
                        self.dataframe[kuberconstants.PL_POSITION][i] = PL
                        if ((currentEMA_9 < currentEMA_18) and (previousEMA_9 > previuosEMA_18)) or (((PL < Profit_Max*.8) and (currentRSI_14 < previousRSI_14*0.95))) or PL<(-50):
                            self.dataframe[kuberconstants.Status][i] = "BUY_CLOSE"
                            self.dataframe[kuberconstants.RESONCODE][i] = "EMA 9 Close Below with HA Low -2 Candle- Squareoff"
                            if(PL<-100):
                              PL=-100
                            self.dataframe[kuberconstants.PROFIT][i] = PL
                            buyOrderPlaced = False
                            sellOrderPlaced = False
                            orderPlaced = False
                            PL=0
                        if (int(str(self.dataframe["TIME"][i])[-8:].replace(":","")) > 152000):
                                self.dataframe[kuberconstants.RESONCODE][i] = str("Harsh closed - intraday call validity")    
                                self.dataframe[kuberconstants.Status][i] = "BUY_CLOSE"
                                buyOrderPlaced = False
                                sellOrderPlaced = False
                                orderPlaced = False    
                                if(PL<-100):
                                  PL=-100
                                self.dataframe[kuberconstants.PROFIT][i] = PL
                                PL=0
                        elif (int(str(self.dataframe["TIME"][i])[-8:].replace(":","")) > 152000) and buyOrderPlaced == True:
                            self.dataframe[kuberconstants.RESONCODE][i] = str("Harsh closed - intraday call validity")    
                            self.dataframe[kuberconstants.Status][i] = "BUY_CLOSE"
                            buyOrderPlaced = False
                            sellOrderPlaced = False
                            orderPlaced = False
                            if(PL<-100):
                              PL=-100
                            self.dataframe[kuberconstants.PROFIT][i] = PL  
                            PL=0
                    if sellOrderPlaced == True:
                        PL = position_price - self.dataframe["close"][i] 
                        Profit_Max = max(Profit_Max, PL)
                        self.dataframe[kuberconstants.PL_POSITION][i] = PL
                        if (currentEMA_9 > currentEMA_18) and (previousEMA_9 < previuosEMA_18) or ((PL < Profit_Max*.8) and (currentRSI_14 > previousRSI_14*1.05)) or (PL<(-50)):
                            self.dataframe[kuberconstants.Status][i] = "SELL_CLOSE"
                            self.dataframe[kuberconstants.RESONCODE][i] = "9 EMA Crosses above 18 EMA--Srqeoff"
                            sellOrderPlaced = False
                            buyOrderPlaced = False
                            orderPlaced = False 
                            if(PL<-100):
                              PL=-100
                            self.dataframe[kuberconstants.PROFIT][i] = PL 
                            PL = 0 
                        if (int(str(self.dataframe["TIME"][i])[-8:].replace(":","")) > 152000) :
                            self.dataframe[kuberconstants.RESONCODE][i] = str("Harsh closed - intraday call validity") 
                            self.dataframe[kuberconstants.Status][i] = "SELL_CLOSE"  
                            sellOrderPlaced = False 
                            buyOrderPlaced = False
                            orderPlaced = False
                            if(PL<-100):
                              PL=-100
                            self.dataframe[kuberconstants.PROFIT][i] = PL 
                            PL = 0       
        if int(str(self.dataframe["TIME"][i])[-8:].replace(":","")) >= 152500:
            if buyOrderPlaced == True:
                PL = self.dataframe["close"][i] - position_price
                self.dataframe[kuberconstants.PL_POSITION][i] = PL
                self.dataframe[kuberconstants.Status][i] = "BUY_CLOSE"
                self.dataframe[kuberconstants.RESONCODE][i] = "Dukaan Band"
                if(PL<-100):
                    PL=-100
                self.dataframe[kuberconstants.PROFIT][i] = PL    
                buyOrderPlaced = False
                sellOrderPlaced = False
                orderPlaced = False
            if sellOrderPlaced == True:
                PL = position_price - self.dataframe["close"][i] 
                Profit_Max = max(Profit_Max, PL)
                self.dataframe[kuberconstants.PL_POSITION][i] = PL
                self.dataframe[kuberconstants.Status][i] = "SELL_CLOSE"
                self.dataframe[kuberconstants.RESONCODE][i] = "Dukaan Band"
                sellOrderPlaced = False
                buyOrderPlaced = False
                orderPlaced = False
                if(PL<-100):
                    PL=-100
                self.dataframe[kuberconstants.PROFIT][i] = PL
            PL=0

    return self.dataframe

  def validateBuy(self,i,dataframe_close):
    return (self.dataframe["EMA_9"][i]>self.dataframe["EMA_9"][i]) and (self.dataframe["RSI_14"][i] > kuberconstants.RSI_64) and (dataframe_close > self.dataframe["EMA_9"][i]) and (dataframe_close > self.dataframe["EMA_21"][i]) and (self.dataframe["RSI_14"][i]> self.dataframe["RSI_100"][i])

  def validateSell(self,i):
    return (self.dataframe["RSI_14"][i]<self.dataframe["RSI_100"][i]) and (self.dataframe["EMA_9"][i]<self.dataframe["EMA_21"][i]) and (self.dataframe["RSI_14"][i] < kuberconstants.RSI_30 )

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
        if int(str(self.dataframe["TIME"][i])[-8:].replace(":","")) >= 93000 and int(str(self.dataframe["TIME"][i])[-8:].replace(":","")) <= 150000:
            if (self.dataframe["EMA_9"][i] is not NULL) and (self.dataframe["EMA_18"][i] is not NULL) and (self.dataframe["EMA_51"][i] is not NULL):
                if orderPlaced == False:
                    if buyOrderPlaced == False:
                        #if (self.dataframe["RSI_14"][i] > self.dataframe["RSI_14"][i-1]) and (self.dataframe["RSI_14"][i-1] > self.dataframe["RSI_14"][i-2]) and (self.dataframe["RSI_14"][i-2] > self.dataframe["RSI_14"][i-3]) and  (self.dataframe["RSI_14"][i-2] > self.dataframe["RSI_14"][i]) > 55 :(self.dataframe["RSI_14"][i] > self.dataframe["RSI_14"][i-1]*1.12) and
                         if ((self.dataframe["EMA_9"][i-1] < self.dataframe["EMA_18"][i-1]) and (self.dataframe["EMA_9"][i] > self.dataframe["EMA_18"][i])) and (self.dataframe["RSI_14"][i] > self.dataframe["RSI_14"][i-1]*1.05): # and (self.dataframe["RSI_14"][i] > self.dataframe["RSI_100"][i]) and (self.dataframe["RSI_14"][i] > 55):#and (self.dataframe["RSI_14"][i-1] < self.dataframe["RSI_100"][i-1]))  and ((self.dataframe["close"][i] > self.dataframe["HA_High"][i-2])):
                            self.dataframe[kuberconstants.Status][i] = "BUY_OPEN"
                            buyOrderPlaced = True
                            sellOrderPlaced = False
                            orderPlaced = True
                            position_price = self.dataframe["close"][i]
                            buy_signal_count = buy_signal_count +1
                            RSI_ARRAY.append(self.dataframe["RSI_14"][i])
                    if sellOrderPlaced == False:
                        #if (self.dataframe["EMA_9"][i] < self.dataframe["EMA_21"][i]) and (self.dataframe["RSI_14"][i] < 35) and (self.dataframe["close"][i] < self.dataframe["EMA_9"][i]) and (self.dataframe["close"][i] < self.dataframe["EMA_21"][i]) and (self.dataframe["close"][i] < self.dataframe["EMA_200"][i]) and (self.dataframe["close"][i] < self.dataframe["ST_1"][i]) and (self.dataframe["close"][i] < self.dataframe["ST_2"][i]) and (self.dataframe["close"][i] < self.dataframe["ST_3"][i]):
                        if  (self.dataframe["EMA_9"][i-1] > self.dataframe["EMA_18"][i-1] and (self.dataframe["EMA_9"][i] < self.dataframe["EMA_18"][i])) and (self.dataframe["RSI_14"][i] < self.dataframe["RSI_14"][i-1]*0.95):# and self.dataframe["RSI_14"][i] < 40 and (self.dataframe["RSI_14"][i] < self.dataframe["RSI_100"][i]) and (self.dataframe["RSI_14"][i] < 40 ): # and (self.dataframe["RSI_100"][i] > self.dataframe["RSI_14"][i]) and (self.dataframe["close"][i] < self.dataframe["EMA_51"][i]). and self.dataframe["close"][i] < self.dataframe["HA_Low"][i-2] :
                            self.dataframe[kuberconstants.Status][i] = "SELL_OPEN"
                            sellOrderPlaced = True
                            buyOrderPlaced = False
                            orderPlaced = True
                            position_price = self.dataframe["close"][i]
                            sell_signal_count = sell_signal_count +1
                            RSI_ARRAY.append(self.dataframe["RSI_14"][i])
                else : # Square off logic
                    if buyOrderPlaced == True:
                        PL = self.dataframe["close"][i] - position_price
                        Profit_Max = max(Profit_Max, PL)
                        self.dataframe[kuberconstants.PL_POSITION][i] = PL
                        if ((self.dataframe["EMA_9"][i] < self.dataframe["EMA_18"][i]) and (self.dataframe["EMA_9"][i-1] > self.dataframe["EMA_18"][i-1])) or (((PL < Profit_Max*.8) and (self.dataframe["RSI_14"][i] < self.dataframe["RSI_14"][i-1]*0.95))) or PL<(-50):
                            #if  self.dataframe["HA_Low"][i] < self.dataframe["HA_Low"][i-2]:# and self.dataframe["HA_Low"][i] < self.dataframe["HA_Low"][i-2]): #fast fignal Priot
                            self.dataframe[kuberconstants.Status][i] = "BUY_CLOSE"
                            self.dataframe[kuberconstants.RESONCODE][i] = "EMA 9 Close Below with HA Low -2 Candle- Squareoff"
                            self.dataframe[kuberconstants.PROFIT][i] = PL    
                            buyOrderPlaced = False
                            sellOrderPlaced = False
                            orderPlaced = False
                            if PL > 0: 
                                 P_trade =  P_trade +1
                            else:
                                 L_trade =  L_trade +1
                            #    cummulative_loss = cummulative_loss + PL     
                            #    cummulative_profit = cummulative_profit + PL
                        if (int(str(self.dataframe["TIME"][i])[-8:].replace(":","")) > 152500):
                                self.dataframe[kuberconstants.RESONCODE][i] = str("Harsh closed - intraday call validity")    
                                self.dataframe[kuberconstants.Status][i] = "BUY_CLOSE"
                                buyOrderPlaced = False
                                sellOrderPlaced = False
                                orderPlaced = False    
                                self.dataframe[kuberconstants.PROFIT][i] = PL
                                if PL > 0: 
                                    P_trade =  P_trade +1
                                else: 
                                    L_trade =  L_trade +1
                        #cummulative_loss = cummulative_loss + PL 
                        #cummulative_profit = cummulative_profit + PL    
                        elif (int(str(self.dataframe["TIME"][i])[-8:].replace(":","")) >= 152500) and buyOrderPlaced == True:
                            self.dataframe[kuberconstants.RESONCODE][i] = str("Harsh closed - intraday call validity")    
                            self.dataframe[kuberconstants.Status][i] = "BUY_CLOSE"
                            buyOrderPlaced = False
                            sellOrderPlaced = False
                            orderPlaced = False
                            self.dataframe[kuberconstants.PROFIT][i] = PL
                            if PL > 0:
                                P_trade =  P_trade +1
                            else: 
                                L_trade =  L_trade +1
                        cummulative_loss = cummulative_loss + PL 
                        cummulative_profit = cummulative_profit + PL    
                    if sellOrderPlaced == True:
                        PL = position_price - self.dataframe["close"][i] 
                        Profit_Max = max(Profit_Max, PL)
                        self.dataframe[kuberconstants.PL_POSITION][i] = PL
                        if (self.dataframe["EMA_9"][i] > self.dataframe["EMA_18"][i]) and (self.dataframe["EMA_9"][i-1] < self.dataframe["EMA_18"][i-1]) or ((PL < Profit_Max*.8) and (self.dataframe["RSI_14"][i] > self.dataframe["RSI_14"][i-1]*1.05)) or (PL<(-50)):
                            #if (self.dataframe["close"][i] < self.dataframe["HA_High"][i-2] ): #fast fignal Priot
                            self.dataframe[kuberconstants.Status][i] = "SELL_CLOSE"
                            self.dataframe[kuberconstants.RESONCODE][i] = "9 EMA Crosses above 18 EMA--Srqeoff"
                            sellOrderPlaced = False
                            buyOrderPlaced = False
                            orderPlaced = False 
                            self.dataframe[kuberconstants.PROFIT][i] = PL 
                            if PL > 0:
                                P_trade =  P_trade +1
                            else:
                                L_trade =  L_trade +1
                                cummulative_loss = cummulative_loss + PL 
                            PL = 0 
                            cummulative_profit = cummulative_profit + PL
                        if (int(str(self.dataframe["TIME"][i])[-8:].replace(":","")) > 152500) :
                            self.dataframe[kuberconstants.RESONCODE][i] = str("Harsh closed - intraday call validity") 
                            self.dataframe[kuberconstants.Status][i] = "SELL_CLOSE"  
                            sellOrderPlaced = False 
                            buyOrderPlaced = False
                            orderPlaced = False
                            self.dataframe[kuberconstants.PROFIT][i] = PL   
                            if PL > 0: 
                                P_trade =  P_trade +1
                            else:
                                L_trade =  L_trade +1 
                                cummulative_loss = cummulative_loss + PL 
                            PL = 0       
                            cummulative_profit = cummulative_profit + PL
    total_signal = (sell_signal_count+buy_signal_count)
    win_rate = P_trade/total_signal*100
    #max_point_gain = DataFrame.groupby(['PROFIT'])['Value'].max()
    #max_point_gain = DataFrame['PROFIT'].max()
    #min_point_gain = DataFrame['PROFIT'].min()
    #max_profit = max_point_gain*25
    print("change in --->")
    print("%Win Rate ---------------------------------------:"+str(win_rate))
    print("total singal catched 99 days---------------------:"+str(total_signal))
    print("total loss singal catched 99 days----------------:"+str(L_trade))
    print("total Win singal catched 99 days-----------------:"+str(P_trade))
    #print("Max   profit catched 99 days---------------------:"+str(max_profit))
    #print("Max   point gain catched 99 days-----------------:"+str(max_point_gain))
    print(("Cumalative profit   point gain catched 99 days-----------------:"+str(cummulative_profit)))
    print(("Cumalative loss   point gain catched 99 days-----------------:"+str(cummulative_loss)))
    #print(("final profit   point gain catched 99 days-----------------:"+max_point_gain))
    #print(DataFrame["PROFIT"].max())
    #print(DataFrame["PROFIT"].min())
    #print(DataFrame["PROFIT"].median())

    return self.dataframe

  def validateBuy(self,i,dataframe_close):
    return (self.dataframe["EMA_9"][i]>self.dataframe["EMA_9"][i]) and (self.dataframe["RSI_14"][i] > kuberconstants.RSI_64) and (dataframe_close > self.dataframe["EMA_9"][i]) and (dataframe_close > self.dataframe["EMA_21"][i]) and (self.dataframe["RSI_14"][i]> self.dataframe["RSI_100"][i])

  def validateSell(self,i):
    return (self.dataframe["RSI_14"][i]<self.dataframe["RSI_100"][i]) and (self.dataframe["EMA_9"][i]<self.dataframe["EMA_21"][i]) and (self.dataframe["RSI_14"][i] < kuberconstants.RSI_30 )

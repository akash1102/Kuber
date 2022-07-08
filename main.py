from asyncio.windows_events import NULL
import imp
from symtable import Symbol
from Indicators.bollinger_band import BollingerBands
from Indicators.ema import EMA
from Indicators.rsi import RSI
from Indicators.Heikin_Ashi import Heikin_Ashi
from Indicators.vwap import VWAP
from Indicators.sma import SMA
from Indicators.Heikin_Ashi import Heikin_Ashi
from Indicators.supertrend import Supertrend
from Indicators.vwap import VWAP
from Operations.HistoricalDataGenerator import HistoricalDataGenerator
from Operations.SignalGenerator import SignalGenerator
from Operations.TokenGenerator import TokenGenrator
from Utilities import kuberconstants
from datetime import date, datetime, timedelta
import os
import os.path
from os import path
import pandas as pd

#NSE:NIFTY50 "NSE:SBIN-EQ"
def main():
    #script = "NSE:NIFTY50" "NSE:NIFTYBANK-INDEX"
    # This is test
    access_token = TokenGenrator(kuberconstants.CLIENT_ID).save_accessToken()
    startdate = date(2020,1,1)
    enddate = (startdate + timedelta(days= 99)).strftime("%Y-%m-%d")
    
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    enddate = date(currentYear, currentMonth, currentDay)
    delta = abs(enddate - startdate).days

    dataframe_main = pd.DataFrame()
    ab = None
    while ab == None:
        sd = enddate - timedelta(days=delta)
        ed = (sd + timedelta(days=99 if delta>100 else delta)).strftime("%Y-%m-%d")
        sd = sd.strftime("%Y-%m-%d")        
        dataframe = HistoricalDataGenerator(access_token=access_token,logPath="/",symbol="NSE:NIFTYBANK-INDEX",startDate=sd,endDate=ed,interval=5).historical_bydate()
        dataframe_high = dataframe['high']
        dataframe_low = dataframe['low']
        dataframe_close = dataframe['close']
        dataframe_open =  dataframe['open']
        dataframe_volume = dataframe['volume']
    
        supertrendObj = Supertrend(dataframe_high,dataframe_low,dataframe_close)
        for i in kuberconstants.SUPERTREND_MULTIPLIERS:
            dataframe['ST_'+str(i)] = supertrendObj.calculate_supertrend(kuberconstants.SUPERTREND_PERIOD,i)['SUPERT_7_'+str(i)+'.0']
    
        emaObj = EMA(dataframe_close)
        for i in kuberconstants.EMA_LENGTHS:
            dataframe['EMA_'+str(i)] = emaObj.calculate_ema(i)

        smaObj = SMA(dataframe_close)
        for i in kuberconstants.SMA_LENGTHS:
            dataframe['SMA_'+str(i)] = smaObj.calculate_sma(i)

        rsiObj = RSI(dataframe_close)
        for i in kuberconstants.RSI_LENGTHS:
            dataframe['RSI_'+str(i)] = rsiObj.calculate_rsi(i)

        bbObj = BollingerBands(dataframe_close)
        dataframe_bb = bbObj.calculate_bbands(20)
        dataframe['BB_U'] = dataframe_bb['BBU_20_2.0']
        dataframe['BB_L'] = dataframe_bb['BBL_20_2.0']
        dataframe['BB_M'] = dataframe_bb['BBM_20_2.0']

        # HAObj = Heikin_Ashi()
        # dataframe = HAObj.calculate_Heikin_Ashi(dataframe)

        #dataframe = Heikin_Ashi.#cal(dataframe,dataframe['open'],dataframe['high'],dataframe['low'],dataframe['close'])
        dataframe["TIME"] = dataframe.index
        signalGeneration = SignalGenerator(dataframe)
        dataframe = signalGeneration.GenerateSignal()

        dataframe_main = dataframe_main.append(dataframe)
        delta = delta - 100 if delta > 100 else delta - delta
        if(delta == 0):
            ab = "done"


    bhavcopy_savePath = os.path.dirname(os.path.abspath('main.py')) + "\Bhavcopy_files\\"+str(datetime.now().strftime('%d%m%Y%H%M%S%M'))+".csv"    
    
    dataframe_main.to_csv(bhavcopy_savePath)

main()



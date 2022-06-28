from asyncio.windows_events import NULL
from Indicators.ema import EMA
from Indicators.rsi import RSI
from Indicators.sma import SMA
from Indicators.supertrend import Supertrend
from Operations.HistoricalDataGenerator import HistoricalDataGenerator
from Operations.SignalGenerator import SignalGenerator
from Operations.TokenGenerator import TokenGenrator
from Utilities import kuberconstants
import datetime
import os
import os.path
from os import path 

def main():
    access_token = TokenGenrator(kuberconstants.CLIENT_ID).save_accessToken()
    startdate = datetime.date(2021,3,1)
    enddate = (startdate + datetime.timedelta(days= 99)).strftime("%Y-%m-%d")
    dataframe = HistoricalDataGenerator(access_token=access_token,logPath="/",symbol="NSE:SBIN-EQ",startDate=startdate,endDate=enddate,interval=5).historical_bydate()

    dataframe_high = dataframe['high']
    dataframe_low = dataframe['low']
    dataframe_close = dataframe['close']

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

    signalGeneration = SignalGenerator(dataframe)
    dataframe = signalGeneration.GenerateSignal()

    bhavcopy_savePath = os.path.dirname(os.path.abspath('main.py')) + "\Bhavcopy_files\\banknifty_"+str(datetime.datetime.now().strftime('%d%m%Y%H%M%S%M'))+".csv"    
    dataframe.to_csv(bhavcopy_savePath)

main()



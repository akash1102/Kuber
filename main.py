from asyncio.windows_events import NULL
from sqlite3 import Row
import time
import pytz 
from selenium import webdriver
from fyers_api import accessToken
from Utilities import kuberconstants
from urllib.parse import urlparse, parse_qs
import pandas as pd
from fyers_api import fyersModel
import datetime
import os
import os.path
from os import path
import pandas_ta as ta

def generate_auth_code():
    url = kuberconstants.GENERATE_AUTH_CODE_URL
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(1)

    driver.execute_script(f"document.querySelector('[id={kuberconstants.FYERS_CLIENTID}]').value = '{kuberconstants.USERNAME}'")
    driver.execute_script(f"document.querySelector('[id={kuberconstants.CLIENTID_SUBMIT}]').click()")
    time.sleep(1)

    driver.execute_script(f"document.querySelector('[id={kuberconstants.FYERS_CLIENT_PASSWORD}]').value = '{kuberconstants.PASSWORD}'")
    driver.execute_script(f"document.querySelector('[id={kuberconstants.LOGIN_SUBMIT}]').click()")
    time.sleep(1)

    driver.find_element_by_id(kuberconstants.VERIFY_PIN).find_element_by_id("first").send_keys(kuberconstants.PIN1)
    driver.find_element_by_id(kuberconstants.VERIFY_PIN).find_element_by_id("second").send_keys(kuberconstants.PIN2)
    driver.find_element_by_id(kuberconstants.VERIFY_PIN).find_element_by_id("third").send_keys(kuberconstants.PIN3)
    driver.find_element_by_id(kuberconstants.VERIFY_PIN).find_element_by_id("fourth").send_keys(kuberconstants.PIN4)
    time.sleep(1)
    driver.execute_script(f"document.querySelector('[id={kuberconstants.VERIFY_PIN_SUBMIT}]').click()")
    time.sleep(2)

    newurl = driver.current_url
    parsed = urlparse(newurl)
    parsedlist = parse_qs(parsed.query)['auth_code']
    auth_code = parsedlist[0]
    driver.quit()
    return auth_code

#def super_trend(df['high'], df['low'], df['close'], period, multiplier, ta):
#    SP = ta.supertrend(df['high'], df['low'], df['close'], period, multiplier)
#    return SP,ta, df

def calculate_ema(close, n):
    return ta.ema(close, n)

def calculate_sma(close, n):
    return ta.sma(close, n)    

def calculate_vwap(low, close, volume):
    return ta.vwap(low , close, volume)

def calculate_rsi(close,length):
    return ta.rsi(close, length )   

def Calculate_macd(DF,len1, len2, len3):
    #Function to calculate MACD
    #Typical Values a (fast Moving Avg) = 12;
    #               b (slow Moving Avg) = 26;
    #               c (signal line Ma Window):
    df = DF.copy()
    df["MA_Fast"]=df["close"].ewm(span=len1,min_periods=len1).mean() 
    df["MA_Slow"]=df["close"].ewm(span=len2,min_periods=len2).mean() 
    df["MACD"]=df["MA_Fast"]-df["MA_Slow"]
    df["Signal"]=df["MACD"].ewm(span=len3,min_periods=len3).mean()
    df.dropna(inplace=True)

def generate_access_token(auth_code):
    session = accessToken.SessionModel(client_id=kuberconstants.CLIENT_ID, secret_key=kuberconstants.SECRET_KEY, redirect_uri=kuberconstants.REDIRECT_URL, response_type="code", grant_type="authorization_code", state="private", nonce="private")
    session.set_token(auth_code)
    access_token = session.generate_token()['access_token']
    return access_token

def historical_bydate(symbol,sd,ed, interval = 5):
    data = {"symbol":symbol, "resolution": str(interval),"date_format":"1","range_from":str(sd),"range_to":str(ed),"cont_flag":"1"}
    nx = fyers.history(data)
    cols = ['datetime','open','high','low','close','volume']
    df = pd.DataFrame.from_dict(nx['candles'])
    df.columns = cols
    df['datetime'] = pd.to_datetime(df['datetime'],unit = "s")
    df['datetime'] = df['datetime'].dt.tz_localize('utc').dt.tz_convert('Asia/Kolkata')
    df['datetime'] = df['datetime'].dt.tz_localize(None)
    df = df.set_index('datetime')
    return df

def save_accessToken(clientId):
    save_path = os.path.abspath('tokens')
    name_of_file = "token_"+clientId
    complete_file_path = os.path.join(save_path, name_of_file+".txt")
    access_token = ""
    if not path.exists(complete_file_path):
        auth_code = generate_auth_code()
        access_token = generate_access_token(auth_code)
        token_file = open(complete_file_path, "w")
        token_file.write(access_token)
        token_file.close()
    else:
        access_token = open(complete_file_path, "r").read()
    return access_token


def main():
    global fyers
    access_token = save_accessToken(kuberconstants.CLIENT_ID)
    fyers = fyersModel.FyersModel(client_id=kuberconstants.CLIENT_ID, token=access_token, log_path="/")
    startdate = datetime.date(2021,3,1)
    enddate = (startdate + datetime.timedelta(days= 99)).strftime("%Y-%m-%d")
    dataframe = historical_bydate("NSE:SBIN-EQ", startdate, enddate)#("NSE:NIFTYBANK-INDEX", startdate, enddate)
    df = ta.supertrend(high=dataframe['high'], low=dataframe['low'], close=dataframe['close'], period=14, multiplier= 3)
    dataframe['ST_3'] = df['SUPERT_7_3.0']
    df = ta.supertrend(high=dataframe['high'], low=dataframe['low'], close=dataframe['close'], period=14, multiplier= 2)
    dataframe['ST_2'] = df['SUPERT_7_2.0']
    df = ta.supertrend(high=dataframe['high'], low=dataframe['low'], close=dataframe['close'], period=14, multiplier= 1)
    dataframe['ST_1'] = df['SUPERT_7_1.0']
    ema_10 = calculate_ema(dataframe['close'], 10)
    ema_21 = calculate_ema(dataframe['close'], 21)
    ema_51 = calculate_ema(dataframe['close'], 51)
    ema_101 = calculate_ema(dataframe['close'], 101)
    ema_151 = calculate_ema(dataframe['close'], 151)
    ema_200 = calculate_ema(dataframe['close'], 200)
    sma_10 = calculate_sma(dataframe['close'], 10)
    sma_20 = calculate_sma(dataframe['close'], 20)
    sma_30 = calculate_sma(dataframe['close'], 30)
    sma_40 = calculate_sma(dataframe['close'], 40)
    sma_50 = calculate_sma(dataframe['close'], 50)
    rsi_14 = calculate_rsi(dataframe['close'], 14)
    rsi_100 = calculate_rsi(dataframe['close'], 100)
    #vwap    = calculate_vwap(dataframe['low'], dataframe['close'], dataframe['volume'])
    dataframe['EMA_10'] = ema_10
    dataframe['EMA_21'] = ema_21
    dataframe['EMA_51'] = ema_51
    dataframe['EMA_101'] = ema_101
    dataframe['EMA_151'] = ema_151
    dataframe['EMA_200'] = ema_200
    dataframe['SMA_10'] = sma_10
    dataframe['SMA_20'] = sma_20
    dataframe['SMA_30'] = sma_30
    dataframe['SMA_40'] = sma_40
    dataframe['SMA_50'] = sma_50
    dataframe['RSI_14'] = rsi_14
    dataframe['RSI_100'] = rsi_100
    # for index, row in dataframe.iterrows():
    #     ema_10 = calculate_ema(row['close'])  
    #for i in range(n,len(dataframe)):,
    #    if dataframe['close']

    now = datetime.datetime.now()
    today945am = now.replace(hour=9, minute=45, second=0)
    today230pm = now.replace(hour=14, minute=30, second=0)
    if (now > today945am) and (now < today230pm):
        dataframe["BUY_EMA10_EMA20_RSI14"] = ""
        dataframe["SELL_EMA10_EMA20_RSI14"] = ""
        for i in range(len(dataframe.index)):
            if (dataframe["EMA_10"] is not NULL) and (dataframe["EMA_21"] is not NULL) :
                if (dataframe["EMA_10"][i]>dataframe["EMA_21"][i]) and (dataframe["RSI_14"][i] > 64) and (dataframe["close"][i] > dataframe["EMA_10"][i]) and (dataframe["close"][i] > dataframe["EMA_21"][i]):
                    if(dataframe["RSI_14"][i]>dataframe["RSI_100"][i]):
                        dataframe["BUY_EMA10_EMA20_RSI14"][i] = "BUY"
                else:
                    if(dataframe["RSI_14"][i]<dataframe["RSI_100"][i]) and ( dataframe["EMA_10"][i]<dataframe["EMA_21"][i]) and (dataframe["RSI_14"][i] < 30 ):
                        #if (dataframe["EMA_10"][i]<dataframe["EMA_21"][i]) and (dataframe["RSI_14"][i] < 30):
                            dataframe["SELL_EMA10_EMA20_RSI14"][i] = "SELL"
        bhavcopy_savePath = os.path.dirname(os.path.abspath('main.py')) + "\Bhavcopy_files\\banknifty_"+str(datetime.datetime.now().strftime('%d%m%Y%H%M%S%M'))+".csv"    
        dataframe.to_csv(bhavcopy_savePath)

main()



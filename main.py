import time 
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

def generate_access_token(auth_code):
    session = accessToken.SessionModel(client_id=kuberconstants.CLIENT_ID, secret_key=kuberconstants.SECRET_KEY, redirect_uri=kuberconstants.REDIRECT_URL, response_type="code", grant_type="authorization_code", state="private", nonce="private")
    session.set_token(auth_code)
    access_token = session.generate_token()['access_token']
    return access_token

def historical_bydate(symbol,sd,ed, interval = 15):
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
    startdate = datetime.date(2021,1,1)
    enddate = (startdate + datetime.timedelta(days= 99)).strftime("%Y-%m-%d")
    dataframe = historical_bydate("NSE:NIFTYBANK-INDEX", startdate, enddate)
    bhavcopy_savePath = os.path.dirname(os.path.abspath('main.py')) + "\Bhavcopy_files\\banknifty_"+str(datetime.datetime.now().strftime('%d%m%Y%H%M%S%M'))+".csv"    
    dataframe.to_csv(bhavcopy_savePath)

main()
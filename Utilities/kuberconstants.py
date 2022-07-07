import os

LOGPATH = os.getcwd()
CLIENT_ID = '3N84K19TK0-100'
SECRET_KEY = 'TQ14VZQ0RI'
REDIRECT_URL = 'https://www.google.com'
RESPONSE_TYPE = ''
GRANT_TYPE = ''
USERNAME = 'XH00748'
PASSWORD = 'Geeta@2022'
PIN1 = '5'
PIN2 = '6'
PIN3 = '3'
PIN4 = '3'
FYERS_CLIENTID = 'fy_client_id'
CLIENTID_SUBMIT = 'clientIdSubmit'
FYERS_CLIENT_PASSWORD = 'fy_client_pwd'
LOGIN_SUBMIT = 'loginSubmit'
VERIFY_PIN = 'verify-pin-page'
VERIFY_PIN_SUBMIT = 'verifyPinSubmit'
SMA_LENGTHS = [10,20,30,40,50]
EMA_LENGTHS = [9,18,51,101,151,200]
RSI_LENGTHS = [14,100]
SUPERTREND_MULTIPLIERS = [1,2,3]
SUPERTREND_PERIOD = 14
Status = 'Status'
SELL_EMA10_EMA20_RSI14 = 'SELL_EMA10_EMA20_RSI14'
RESONCODE = 'RESONCODE'
VWAP = 'VWAP'
PROFIT = 'PROFIT'
RSI_30 = 30
RSI_64 = 64
PL_POSITION = 'PL_POSITION'
'''
'''
GENERATE_AUTH_CODE_URL = f'https://api.fyers.in/api/v2/generate-authcode?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URL}&response_type=code&state=private'
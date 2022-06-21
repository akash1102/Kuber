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

GENERATE_AUTH_CODE_URL = f'https://api.fyers.in/api/v2/generate-authcode?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URL}&response_type=code&state=private'
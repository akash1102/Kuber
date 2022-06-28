import time
from urllib.parse import urlparse, parse_qs
from Utilities import kuberconstants
from selenium import webdriver
from fyers_api import accessToken
import os
import os.path
from os import path 

class TokenGenrator:
    def __init__(self,clientId):
        self.clientId = clientId

    @staticmethod
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

    @staticmethod
    def generate_access_token(auth_code):
        session = accessToken.SessionModel(client_id=kuberconstants.CLIENT_ID, secret_key=kuberconstants.SECRET_KEY, redirect_uri=kuberconstants.REDIRECT_URL, response_type="code", grant_type="authorization_code", state="private", nonce="private")
        session.set_token(auth_code)
        access_token = session.generate_token()['access_token']
        return access_token 

    def save_accessToken(self):
        save_path = os.path.abspath('tokens')
        name_of_file = "token_"+self.clientId
        complete_file_path = os.path.join(save_path, name_of_file+".txt")
        access_token = ""
        if not path.exists(complete_file_path):
            auth_code = self.generate_auth_code()
            access_token = self.generate_access_token(auth_code)
            token_file = open(complete_file_path, "w")
            token_file.write(access_token)
            token_file.close()
        else:
            access_token = open(complete_file_path, "r").read()
        return access_token


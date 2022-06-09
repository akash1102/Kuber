import datetime
import time
from selenium import webdriver
import document_file
from webdriver_manager.chrome import ChromeDriverManager

# this is test45555
log_path = document_file.logpath
client_id = document_file.client_id
secret_key = document_file.secret_key
redirect_url = document_file.redirect_url
response_type = document_file.response_type
grant_type = document_file.grant_type
username = document_file.username
password = document_file.password
pin1 = document_file.pin1
pin2 = document_file.pin2
pin3 = document_file.pin3
pin4 = document_file.pin4

def generate_auth_code():
    url = f"https://api.fyers.in/api/v2/generate-authcode?client_id={client_id}&redirect_uri={redirect_url}&response_type=code&state=private"
    driver = webdriver.Chrome(ChromeDriverManager().install())
    #driver = webdriver
    driver.get(url)
    x = url
    print(x)
    time.sleep(3)

    driver.execute_script(f"document.querySelector('[id=fy_client_id]').value = '{username}'")
    driver.execute_script("document.querySelector('[id=clientIdSubmit]').click()")
    time.sleep(3)

    driver.execute_script(f"document.querySelector('[id=fy_client_pwd]').value = '{password}'")
    driver.execute_script("document.querySelector('[id=loginSubmit]').click()")
    time.sleep(3)

    driver.find_element_by_id("verify-pin-page").find_element_by_id("first").send_keys(pin1)
    driver.find_element_by_id("verify-pin-page").find_element_by_id("second").send_keys(pin2)
    driver.find_element_by_id("verify-pin-page").find_element_by_id("third").send_keys(pin3)
    driver.find_element_by_id("verify-pin-page").find_element_by_id("fourth").send_keys(pin4)
    time.sleep(8)
    #driver.excute_script("document.querySelector('[id=verifyPinSubmit]').click()")

    newurl = driver.current_url
    auth_code = newurl[newurl.index('client_id='):newurl.index('&state')][len('client_id'):]
    driver.quit()
    return auth_code

def main():
    global fyers
    auth_code = generate_auth_code()
    #auth_code = "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"

main()
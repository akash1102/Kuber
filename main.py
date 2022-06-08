
from fyers_api.Websocket import ws
from fyers_api import fyersModel
from fyers_api import accessToken
import datetime
import time
import document_file
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
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

open_position = []

def getTime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def custom_message(msg):
    script = msg[0]['symbol']
    ltp = msg[0]['ltp']
    high = msg[0]['high_price']
    low = msg[0]['low_price']
    opn = msg[0]['open_price']
    close = msg[0]['close_price']
    ltt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(msg[0]['timestamp']))
    print(f"Script:{script}, ltp:{ltp}, High:{high}, Low:{low}, ltt:{ltt}")

#*************** Strategy checking started from Here *************
    if((script not in open_position) and (ltt[-8] < "12:00:00")):
        if (ltp <= low) :
            open_position.append(script)
            placeOrder("SELL", script, ltp)
        if (ltp >= high) :
            open_position.append(script)
            placeOrder("BUY", script, ltp)


def placeOrder(order, script, ltp):
    ltp = ltp
    if order =="BUY" :
            quantity = int(100)
            target_price = int(ltp*0.02)
            stop_loss_price = int(ltp * 0.01)
            order = fyers.placeOrder({"symbol":script, "quantity": quantity, "type": "2", "side": "1", "product_type":"BO", "limitPrice":"0", "stopPrice": stop_loss_price,  "validity":"DAY","disclosedQty": 0, "offlineOrder":"False", "takeProfit": target_price})
            print(f"Buy order placed for ",script, "at price", ltp, "for quantity", quantity, "with order id ",order['id'], "at time ", getTime())
            print(open_position)
    else :
            ltp = ltp
            quantity = int(100)
            target_price = int(ltp*0.02)
            stop_loss_price = int(ltp* 0.01)
            order = fyers.placeOrder({"symbol":script, "quantity": quantity , "type": "2", "side": "-1", "product_type":"BO",
                                       "limitPrice":"0", "stopPrice": stop_loss_price,  "validity":"DAY","disclosedQty": 0,
                                       "offlineOrder":"False", "takeProfit": target_price})
            print(f"SELL order placed for ",script, "at price", ltp, "for quantity ", quantity, "with order id", order['id'], "at time ", getTime())
            print(open_position)

def generate_access_token(auth_code, appId, scrt_key):
    appSession = accessToken.SessionModel(client_id=appId, secret_key=scrt_key, grant_type="authorization_code")
    appSession.set_token(auth_code)
    response = appSession.generate_token()["access_token"]
    return response

def generate_auth_code():
    url = f"https://api.fyers.in/api/v2/generate-authcode?client_id={client_id}&redirect_uri={redirect_url}&response_type=code&state"
    driver = webdriver.firefox(executable_path=GeckoDriverManager().install())
    #driver = webdriver.
    driver.get(url)
    time.sleep(3)

    driver.excute_script(f"document.querySelector('[id=fy_client_id]').value = '{username}'")
    driver.excute_script("document.querySelector('[id=clientIdSubmit]').click()")
    time.sleep(3)

    driver.excute_script(f"document.querySelector('[id=fy_client_pwd]').value = '{password}'")
    driver.excute_script("document.querySelector('[id=loginSubmit]').click()")
    time.sleep(3)

    driver.find_element_by_id("verify-pin-page").find_element_by_id("first").send_keys(pin1)
    driver.find_element_by_id("verify-pin-page").find_element_by_id("second").send_keys(pin2)
    driver.find_element_by_id("verify-pin-page").find_element_by_id("third").send_keys(pin3)
    driver.find_element_by_id("verify-pin-page").find_element_by_id("fourth").send_keys(pin4)
    time.sleep(8)

    newurl = driver.current_url
    auth_code = newurl[newurl.index('auth_code=')+10:newurl.index('&state')]
    driver.quit()
    return auth_code

def main():
    global fyers
    # auth_code = generate_auth_code()
    auth_code = "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"
    access_Token = generate_access_token(auth_code, client_id, secret_key)
    fyers = fyersModel.FyersModel(token= access_Token, log_path=log_path, client_id=client_id)
    fyers.token = access_Token
    newtoken = f"{client_id}:{access_Token}"
    data_type = "symbolData"

    symbol =["NSE:SBIN-EQ", "NSE:DLF-EQ"]
    orderplacetime = int(9) * 60 + int(20)
    closingtime = int(13) * 60 + int(35)
    timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)
    print((f"waiting for 9.20 AM , time now:{getTime()}"))

    while timenow < orderplacetime:
        time.sleep(0.2)
        timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().min)
        print(f"Ready for trading, TimeNow:{getTime()}")

    fs = ws.FyersSocket(access_Token=newtoken, run_background=False, log_path=log_path)
    fs.subscribe(symbol=symbol, data_type=data_type)
    fs.keep_running()

main()



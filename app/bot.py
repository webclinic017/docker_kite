from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import urllib.parse as urlparse
from selenium.webdriver.chrome.options import Options
from kiteconnect import KiteConnect
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
import pyrebase
import schedule


def data_push(token):

    config = {
        "apiKey": "AIzaSyC--anxL74t3h78q7ZSVPMPipv2m244kBg",
        "authDomain": "kitetoken-ca4cb.firebaseapp.com",
        "databaseURL": "https://kitetoken-ca4cb-default-rtdb.firebaseio.com",
        "projectId": "kitetoken-ca4cb",
        "storageBucket": "kitetoken-ca4cb.appspot.com",
        "messagingSenderId": "369939516780",
        "appId": "1:369939516780:web:17b2f6a31a6a802a453749",
        "measurementId": "G-DCVB5QCJ1Q"
    }
    firebase = pyrebase.initialize_app(config)

    db = firebase.database()

    data = {"token":token}

    db.child("tokens").set(data)
    return  print("Data added to real time database ")



def api_token():
    api_key='0yvny102khsjlnpr'
    api_seceret='0zp3tp2bhxzamg8ph4q2s1ys7l5paunv'
    accountUserName = "ZB8746"
    accountPassword = "@KKR357"
    securityPin = "050991"

    kite=KiteConnect(api_key,api_seceret)

    url=kite.login_url()
    options = Options()
    options.add_argument('--no-sandbox')
    # options.headless = True
    driver = webdriver.Remote('http://selenium:4444/wd/hub',desired_capabilities=DesiredCapabilities.CHROME,options=options)
    sam=driver.get(url)
    wait = WebDriverWait(driver, 20)

    wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="text"]')))\
                    .send_keys(accountUserName)

    ## Find password field and set user password
    wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"]')))\
        .send_keys(accountPassword)

    ## Find submit button and click
    wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))\
        .submit()

    ## Find pin field and set  pin value
    wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"]'))).click()
    time.sleep(5)
    driver.find_element_by_xpath('//input[@type="password"]').send_keys(securityPin)

    ## Final Submit
    wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))).submit()



    wait.until(EC.url_contains('status=success'))

                ## get the token url after success
    tokenurl = driver.current_url
    parsed = urlparse.urlparse(tokenurl)

    token=urlparse.parse_qs(parsed.query)['request_token'][0]
    print(token)
    kite = KiteConnect(api_key)
    #kite.access_token()
    data=kite.generate_session(token,api_seceret)
    #data = kite.access_token(token, api_seceret)
    # driver.close()
    data['access_token']
    kite.set_access_token(data['access_token'])
    print("done")
    data_push(data['access_token'])
    print(data['access_token'])
    driver.quit()
    return data['access_token']

# print(api_token())



schedule.every(60).seconds.do(api_token)

while True:
    schedule.run_pending()
    time.sleep(1)

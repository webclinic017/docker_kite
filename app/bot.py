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


api_key='0yvny102khsjlnpr'
api_seceret='0zp3tp2bhxzamg8ph4q2s1ys7l5paunv'
accountUserName = "ZB8746"
accountPassword = "@KKR357"
securityPin = "050991"

kite=KiteConnect(api_key,api_seceret)

url=kite.login_url()
# options = Options()
# options.headless = True
driver = webdriver.Remote('http://selenium:4444/wd/hub',desired_capabilities=DesiredCapabilities.CHROME)
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
driver.close()
token=urlparse.parse_qs(parsed.query)['request_token'][0]
print(token)
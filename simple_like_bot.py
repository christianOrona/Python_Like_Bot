from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType

import time
import warnings
warnings.filterwarnings("ignore")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("log-level=3")
chrome_options.add_argument("--incognito")
timeout=40
while True:
    driver = webdriver.Chrome(chrome_options=chrome_options)
    print("--------------------------------------")
    print("Loading page")
    #Change the URL below to whatever you need
    driver.get('URL HERE')
    try:
        #Waiting for the page to load
        element_present = EC.presence_of_element_located((By.TAG_NAME, 'html'))
        WebDriverWait(driver, timeout).until(element_present)
        print("Page loaded")
        likeButton=driver.find_element_by_id('voteBtn')
        likeButton.click()
        print("Clicked on Like")
        print("Waiting for response")
        time.sleep(2)
    except TimeoutException:
        print("Timed out waiting for page to load")
    print("Good,closing browser")
    driver.close()
    print("Closed")

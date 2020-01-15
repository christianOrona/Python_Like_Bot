from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType

co = webdriver.ChromeOptions()
co2 = webdriver.ChromeOptions()
co.add_argument("log-level=3")
co.add_argument("--headless")
co2.add_argument("--headless")
co2.add_argument('--ignore-certificate-errors')
co.add_argument("--incognito")
import time
def get_proxies(co=co):
    driver = webdriver.Chrome(chrome_options=co)
    print("Getting proxy server list")
    #Use whatever proxy list you want
    driver.get("https://free-proxy-list.net/")
    #driver.get("https://www.us-proxy.org/")
    PROXIES = []
    proxies = driver.find_elements_by_css_selector("tr[role='row']")
    for p in proxies:
        result = p.text.split(" ")
        print(result[-1])
        #if result[-1] == "yes": #set to yes to get only https ones
        PROXIES.append(result[0]+":"+result[1])

    driver.close()
    print("List prepared")
    return PROXIES


ALL_PROXIES = get_proxies()


def proxy_driver(PROXIES, index, co=co):
    prox = Proxy()

    if PROXIES:
        pxy = PROXIES[index]
        print("pxy:"+str(pxy))
    else:
        print("--- Proxies used up (%s)" % len(PROXIES))
        PROXIES = get_proxies()

    prox.proxy_type = ProxyType.MANUAL
    prox.http_proxy = pxy
    prox.socks_proxy = pxy
    prox.ssl_proxy = pxy

    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)

    driver = webdriver.Chrome(chrome_options=co2, desired_capabilities=capabilities)

    return driver

timeout=40
totalProxies=len(ALL_PROXIES)
index=1
while True:
    if index <= totalProxies:
        print("index: "+str(index))
        print("using proxy: "+ALL_PROXIES[index])
        driver = proxy_driver(ALL_PROXIES,index)
    driver.get('URL HERE')
    try:
        print("page loading...")
        element_present = EC.presence_of_element_located((By.TAG_NAME, 'html'))
        WebDriverWait(driver, timeout).until(element_present)
        print("page loaded")
        totalLikes=driver.find_element_by_id('count_votes')
        print("total likes"+totalLikes.text)
        likeButton=driver.find_element_by_id('voteBtn')
        likeButton.click()
        print("clicked")
        print("waited")
        time.sleep(2)
    except TimeoutException:
        print("Timed out waiting for page to load")
        index+=1
    print("closing browser")
    driver.close()
    print("closed")

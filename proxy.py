import time

import requests
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from decouple import config
from selenium.webdriver.common.by import By
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager


def checkConnection():
    try:
        s = requests.Session()
        s.headers.update({"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"})
        r = s.get(f'https://api.mouser.com/', timeout=8)
        if '<title>mouser.com</title>' in r.text:
            return True
        else:
            return False
    except Exception as e:
        return False


def checkProxy(prx):
    try:
        s = requests.Session()
        proxies = {
            'https': f"{prx}",
        }
        s.proxies.update(proxies)
        s.headers.update({"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"})
        r = s.get(f'https://api.mouser.com/', timeout=8)
        if '<title>mouser.com</title>' in r.text:
            return prx
        else:
            return False
    except Exception as e:
        # traceback.print_exc()
        return False


def getProxies():
    browser = uc.Chrome(driver_executable_path=ChromeDriverManager().install(), headless=bool(int(config('headless'))))
    browser.get('http://free-proxy.cz/ru/')
    time.sleep(4)
    browser.find_element(By.XPATH, '//*[@id="frmsearchFilter-protocol-2"]').click()
    browser.find_element(By.XPATH, '//*[@id="frmsearchFilter-send"]').click()
    time.sleep(1.5)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find_all('tbody')[1].find_all('tr')
    proxies = []
    for row in table:
        try:
            proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
            proxies.append(proxy)
        except IndexError:
            continue
    return proxies


def findProxy(prxs):
    for pr in tqdm(prxs):
        res = checkProxy(pr)
        if res is not False:
            return res
    return None


if __name__ == '__main__':
    # proxies2 = getProxies()
    # proxy = findProxy(proxies2)
    # working_proxy = findProxy(proxies2)
    # print(working_proxy)
    print(checkConnection())

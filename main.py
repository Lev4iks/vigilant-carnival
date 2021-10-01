import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import asyncio
import random
import csv


proxy_servers = [
    "31.7.148.70:3128",
    "181.209.82.154:23500",
    "201.249.161.51:999",
    "20.76.164.205:3128",
    "45.76.174.251:1088",
    "18.220.20.81:8080",
    "193.226.199.106:9090",
    "195.53.49.11:3128",
    "210.14.104.230:8080",
    "113.160.206.37:55138",
    "156.200.110.116:1981",
    "178.134.155.82:48146",
    "118.99.96.59:8080",
    "14.207.26.235:8080",
    "103.102.14.8:3127",
    "195.158.14.118:3128",
    "117.121.211.170:8080",
    "64.124.38.140:8080",
    "64.124.38.141:8080",
    "64.124.38.139:8080",
    "64.124.38.142:8080",
    "187.92.71.154:53281",
    "41.231.54.37:8888",
    "158.177.253.24:80",
    "23.251.138.105:8080",
    "64.124.38.138:8080",
    "103.110.91.242:3128",
    "20.81.106.180:8888",
    "36.95.156.125:6969",
    "150.242.182.98:80",
    "103.22.172.49:59458",
    "207.244.227.169:443",
    "109.111.157.7:8080",
    "196.20.12.9:8080",
    "91.144.139.3:3128",
    "187.62.191.3:61456",
    "212.115.232.79:31280",
    "170.239.255.2:55443",
    "47.245.33.104:12345",
    "47.254.75.151:8181",
    "169.57.1.84:8123",
    "78.128.124.9:50246",
    "124.41.213.201:39272",
    "109.105.205.232:59152",
    "94.73.239.124:55443",
    "213.81.218.225:8080",
    "51.79.50.46:9300",
    "202.14.80.2:3128",
    "64.124.38.125:8080",
    "173.82.219.113:8118",
    "71.237.233.224:8118",
    "34.138.225.120:8888",
    "62.168.61.241:3128",
    "165.16.22.134:8080",
    "43.224.10.44:6666",
    "203.81.87.186:10443",
    "149.28.91.128:1088",
    "182.253.170.123:8080",
    "103.87.170.108:55616",
    "195.158.7.10:3128",
    "118.185.38.153:35101",
    "89.171.41.90:6969",
    "167.71.206.67:8118",
    "148.251.249.240:3128",
    "52.224.11.76:49205",
    "101.109.255.18:50538",
    "160.16.104.81:3128",
    "109.86.152.78:55443",
    "65.18.114.254:55443",
    "66.42.63.152:8081",
    "64.124.38.26:8080",
    "115.75.1.184:8118",
    "169.57.1.85:8123",
    "177.184.182.247:3128",
    "118.70.109.148:55443",
    "202.62.67.209:53281",
    "85.234.126.107:55555",
    "85.196.133.98:8080",
    "79.110.196.66:45673",
    "88.132.34.230:53281",
    "103.66.196.218:23500",
    "154.72.199.202:41201",
    "5.190.29.161:8080",
    "118.99.100.2:8080",
    "109.173.102.90:8000",
    "190.7.141.66:47576",
    "115.77.191.180:53281",
    "177.91.111.253:8080",
    "182.23.79.162:39902",
    "41.164.68.194:8080",
    "103.250.156.24:6666",
    "158.46.127.222:52574",
    "101.53.158.48:9300",
    "190.152.5.126:53040",
    "51.15.8.75:3738",
    "13.114.160.78:80",
    "103.96.79.73:8080",
    "167.71.199.228:8080",
    "190.8.46.90:6969",
    "31.173.94.93:43539"
]

options = uc.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-extensions")
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = uc.Chrome()
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
URL = 'http://onlyfinder.com'


async def main():
    with driver:
        driver.get(URL)
        print(driver.title)
        driver.get('https://onlyfinder.com/profiles?q=free')
        await asyncio.sleep(random.randint(2, 5))
        driver.reconnect()
        await asyncio.sleep(random.randint(2, 5))
        print(driver.title)
        await asyncio.sleep(random.randint(2, 5))
        search = driver.find_element_by_css_selector('#navbar-input')
        search.send_keys(' location:37.3590,-96.1328,500km')
        search.send_keys(Keys.ENTER)
        await asyncio.sleep(random.randint(2, 5))

        page = driver.find_element_by_css_selector('body')
        print(driver.current_url)
        page_url = driver.current_url
        while driver.current_url != page_url + "&c=984":
            page.send_keys(Keys.PAGE_DOWN)
            await asyncio.sleep(0.5)

        print(driver.current_url)

        results = driver.find_elements_by_class_name('result')
        urls = [result.find_element_by_class_name('divLink').get_attribute('href') for result in results]

        my_file = open('models.csv', 'w')
        with my_file:
            writer = csv.writer(my_file)
            writer.writerows(urls)
            print(8*urls)
        my_file.close()

asyncio.run(main())

import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import cfscrape
import time
import random


options = uc.ChromeOptions()
bot_email = "bukharkinavip.vanessa@yahoo.com"
bot_pasw = "Swnessa70135632"

# задаес профиль
options.user_data_dir = "c:\\temp\\profile"

# задаем настройки для обхода cloudflare
options.add_argument('--user-data-dir=c:\\temp\\profile2')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-setuid-sandbox")

# чтобы не вылазили окна на старте
options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
browser = uc.Chrome(keep_alive=True)

with browser:
    # Переход к списку модолей (FREE)
    browser.get('https://hubite.com/ru/onlyfans-female-accounts/?page=1')
    ip = browser.find_element_by_tag_name('p')
    print(ip.text)
    name = ip.text[1:]
    url = "https://onlyfans.com/" + name

    # Заходим на онли фанс...
    browser.get('https://onlyfans.com/')
    time.sleep(random.randint(5, 10))
    
    email = browser.find_element_by_id('input-27')
    pasw = browser.find_element_by_id('input-29')
    email.send_keys(bot_email)
    time.sleep(1)
    pasw.send_keys(bot_pasw, Keys.ENTER)

    # Переходим к модели
    # browser.get(url)
    # time.sleep(5)
    # browser.implicitly_wait(20)
    # sub_button = browser.find_element_by_tag_name('main')
    # p = sub_button.find_element_by_css_selector('#content > div.l-wrapper.m-content-one-column > div > div.l-profile-container.m-parent-sticky-header > div > div.b-profile-section-btns > div.list-offers.m-offer-bottom-gap-reset.m-main-details > div > div.b-offer-join > div')
    # p.click()
    # print(p.tag_name, p.text)
    #
    # print(BeautifulSoup(sub_button, 'html5'))



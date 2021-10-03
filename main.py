import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import captcha_resolver
import requests
import asyncio
import random
import csv


# Натсройка веб - драйвера

options = uc.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-extensions")
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = uc.Chrome()
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.delete_all_cookies()
driver.clear_cdp_listeners()


only_finder_url = 'http://onlyfinder.com'
only_fans_url = 'http://onlyfans.com'

bot_username = 'bukharkinavip.vanessa@yahoo.com'
bot_password = 'Swnessa70135632'

models = []
with open('models.csv') as File:
    reader = csv.reader(File)
    for row in reader:
        if row:
            models.append(''.join(row)[21:])


async def parse_models():
    with driver:
        print("Переходим на сайт : ", only_finder_url)
        driver.get(only_finder_url)
        driver.get(only_finder_url + '/profiles?q=free')  # Обходим cloudflare и сразу переходим на
        await asyncio.sleep(random.randint(2, 5))  # сайт : http://onlyfinder.com//profiles?q=free
        driver.reconnect()
        await asyncio.sleep(random.randint(2, 5))

        # Вбиваем в строку происка локацию
        search = driver.find_element_by_css_selector('#navbar-input')
        search.send_keys(' location:37.3590,-96.1328,500km')
        # Отправляем ENTER
        search.send_keys(Keys.ENTER)
        await asyncio.sleep(random.randint(2, 5))

        page = driver.find_element_by_css_selector('body')
        page_url = driver.current_url
        # Скролим вниз пока не дойдем до самого низа
        while driver.current_url != page_url + "&c=984":
            page.send_keys(Keys.PAGE_DOWN)
            await asyncio.sleep(0.5)

        # Находим все результаты о моделях и потом записываем все ссылки на профили моделей
        results = driver.find_elements_by_class_name('result')
        urls = [result.find_element_by_class_name('divLink').get_attribute('href') for result in results]

        # Записываем данные (ссылки) в models.csv
        my_file = open('models.csv', 'w')
        with my_file:
            writer = csv.writer(my_file)
            writer.writerows(urls)
        my_file.close()

        print("Полученные ссылки : ", *urls)


async def main():
    driver.get(only_fans_url)
    await asyncio.sleep(random.randint(2, 5))

    username = driver.find_elements_by_class_name('v-text-field__slot')[0].find_element_by_tag_name('input')
    password = driver.find_elements_by_class_name('v-text-field__slot')[1].find_element_by_tag_name('input')

    # Отправляем в поля username и password и нажимаем ENTER
    username.send_keys(bot_username)
    await asyncio.sleep(random.randint(2, 5))
    password.send_keys(bot_password)
    await asyncio.sleep(random.randint(1, 3))
    password.send_keys(Keys.ENTER)
    await asyncio.sleep(random.randint(3, 5))

    captcha = driver.find_element_by_css_selector('body > div:nth-child(7) > div:nth-child(1) > iframe')
    print(captcha.get_attribute('outerHTML'))

    if "hcaptcha" in driver.page_source.lower():
        print("На сайте используется hCaptcha")
        # Находим sitekey для решения капчи
        src = str(captcha.get_attribute('src'))
        i = src.find("sitekey") + 8
        sitekey = src[i:-27]

        print("Sitekey нашей капчи : ", sitekey)

        # Отправляем нешему резолверу sitekey
        token = captcha_resolver.bypass_captcha(sitekey)
        print("Наш токен : ", token, "\n----------------------------------------------------------------")
        await asyncio.sleep(3)
        text = driver.find_elements_by_css_selector('#hcap-script > textarea')[0]
        button_login = driver.find_element_by_css_selector('body > div.main-wrapper > '
                                                           'div.login_content > div > div > '
                                                           'div:nth-child(2) > div > form > button')

        # Делаем видимой область для вставки решенного токена для нашей капчи
        driver.execute_script("arguments[0].setAttribute('style','')", text)
        print("До : ", button_login.get_attribute('outerHTML'))
        await asyncio.sleep(random.randint(1, 3))
        #
        driver.execute_script("document.querySelector('[type^=submit]').removeAttribute('disabled')")
        print("После : ", button_login.get_attribute('outerHTML'))
        await asyncio.sleep(random.randint(1, 3))
        text.send_keys(token)
        await asyncio.sleep(random.randint(1, 3))
        button_login.click()
        await asyncio.sleep(5)

    elif "recaptcha" in driver.page_source.lower():
        print("На сайте используется reCAPTCHA")

    print("Капчи нет")

    # try:
    #     captcha = driver.find_element_by_css_selector('#hcap-script > iframe')
    #     print("hcaptcha" in driver.page_source.lower())
    #
    #     if "hcaptcha" in driver.page_source.lower():
    #         src = str(captcha.get_attribute('src'))
    #         i = src.find("sitekey") + 8
    #         sitekey = src[i:-12]
    #         print("Sitekey нашей капчи : ", sitekey)
    #
    #         # token = captcha_resolver.bypass_captcha(sitekey)
    #         text = driver.find_element_by_css_selector('#hcap-script > textarea')
    #         await asyncio.sleep(2)
    #         driver.execute_script("arguments[0].setAttribute('style','')", text)
    #         await asyncio.sleep(2)
    #         text.send_keys("PIZDEC")
    #         check = driver.find_element_by_css_selector('#checkbox')
    #         print(check.text)
    #         await asyncio.sleep(5)
    #     elif "recaptcha" in driver.page_source.lower():
    #         pass
    #
    # except NoSuchElementException as err:
    #     print(err.stacktrace)
    #     print("На стринце нет капчи")


    # for model in models:
    #     driver.get(only_fans_url + '/' + model)
    #     await asyncio.sleep(random.randint(2, 5))
    #     sub_button = driver.find_element_by_css_selector('#content > div.l-wrapper.m-content-one-column > div > '
    #                                                      'div.l-profile-container > div > div.b-profile-section-btns > '
    #                                                      'div.list-offers.m-offer-bottom-gap-reset.m-main-details > div > '
    #                                                      'div.b-offer-join > div')
    #     sub_button.click()
    #     await asyncio.sleep(random.randint(2, 5))
    #

asyncio.run(main())


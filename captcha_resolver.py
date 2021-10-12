from twocaptcha import TwoCaptcha
import time
import random


API_KEY = '5b17bb93300061f21bad9578fe9fe88f'
solver = TwoCaptcha(API_KEY)


def bypass_captcha(sitekey):
    print("Капча решается...")
    result = solver.hcaptcha(sitekey=sitekey,
                             url='https://onlyfans.com/',
                             param1=...)
    print("Получен токен : ", result)
    return result['code']

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


async def capcha_solver(bot):
    captcha = bot.find_element_by_css_selector('body > div:nth-child(7) > div:nth-child(1) > iframe')
    print(captcha.get_attribute('outerHTML'))

    if "hcaptcha" in bot.page_source.lower():
        print("На сайте используется hCaptcha")
        # Находим sitekey для решения капчи
        src = str(captcha.get_attribute('src'))
        i = src.find("sitekey") + 8
        sitekey = src[i: - 27]

        print("Sitekey нашей капчи : ", sitekey)

        # Отправляем нешему резолверу sitekey
        token = bypass_captcha(sitekey)
        time.sleep(3)
        print("Наш токен #1 : ", token, "\n----------------------------------------------------------------")
        time.sleep(3)
        text = bot.find_elements_by_css_selector('#hcap-script > textarea')[0]
        button_login = bot.find_element_by_css_selector('body > div.main-wrapper > '
                                                           'div.login_content > div > div > '
                                                           'div:nth-child(2) > div > form > button')

        # Делаем видимой область для вставки решенного токена для нашей капчи
        bot.execute_script("arguments[0].setAttribute('style','')", text)
        time.sleep(random.randint(1, 3))
        # Делаем видимым кнопку Login
        bot.execute_script("document.querySelector('[type^=submit]').removeAttribute('disabled')")
        time.sleep(random.randint(1, 3))
        button_login.click()
        time.sleep(random.randint(1, 3))
        text.send_keys(token)
        button_login.click()
        time.sleep(5)

    elif "recaptcha" in bot.page_source.lower():
        print("На сайте используется reCAPTCHA")

from twocaptcha import TwoCaptcha


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

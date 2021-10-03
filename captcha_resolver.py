from twocaptcha import TwoCaptcha


API_KEY = '5b17bb93300061f21bad9578fe9fe88f'
solver = TwoCaptcha(API_KEY)


def bypass_captcha(sitekey):
    print("Капча решается...")
    result = solver.hcaptcha(sitekey=sitekey,
                             url='https://www.site.com/page/',
                             param1=...)
    print("Получен токен : ", result)
    return result['code']


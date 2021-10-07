import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import captcha_resolver
import time
import asyncio
import random
import csv

# Натсройка веб - драйвера
options = uc.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-extensions")
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_extension('C:/Users/LevSo/Downloads')
driver = uc.Chrome()
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.delete_all_cookies()
driver.clear_cdp_listeners()

only_fans_url = 'http://onlyfans.com'

bot_username = 'bukharkinavip.vanessa@yahoo.com'
bot_password = 'Swnessa70135632'

prev_comment = ""

comments = [
    "loved it",
    "mmm gorgeous ",
    "What a naughty beauty",
    "Sexy babe",
    "U make me horny",
    "sexy beauty!! ",
    "What a gorgeous baby",
    "Kiss ",
    "I feel turned on now... ",
    "Sooo hot! ",
    "The most beautiful ",
    "Precious",
    "So nice",
    "Always beautiful! ",
    "My favorite babe",
    "The best ",
    "My naughty beautiful friend ",
    "Wow",
    "Babe",
    "Million kissess",
    "Mmm sensual",
    "I am melting...  like you",
    "U make me feel horny ",
    "U look gorgeous, dear ",
    "U are so sexy",
    "Fantastic baby",
    "Sweet baby",
    "Sexy and sweet",
    "Sweet and hot"
]

# получаем модели
models = []
with open('models.csv') as File:
    reader = csv.reader(File)
    for row in reader:
        if row:
            models.append(''.join(row)[21:])

# получаем последнюю модель, на которой остановились
with open('last_model.txt') as f:
    last_model = int(f.readline())
    print("Индекс модели, с которой закончили : ", last_model)


async def capcha_solver():
    captcha = driver.find_element_by_css_selector('body > div:nth-child(7) > div:nth-child(1) > iframe')
    print(captcha.get_attribute('outerHTML'))

    if "hcaptcha" in driver.page_source.lower():
        print("На сайте используется hCaptcha")
        # Находим sitekey для решения капчи
        src = str(captcha.get_attribute('src'))
        i = src.find("sitekey") + 8
        sitekey = src[i: - 27]

        print("Sitekey нашей капчи : ", sitekey)

        # Отправляем нешему резолверу sitekey
        token = captcha_resolver.bypass_captcha(sitekey)
        await asyncio.sleep(3)
        print("Наш токен #1 : ", token, "\n----------------------------------------------------------------")
        await asyncio.sleep(3)
        text = driver.find_elements_by_css_selector('#hcap-script > textarea')[0]
        button_login = driver.find_element_by_css_selector('body > div.main-wrapper > '
                                                           'div.login_content > div > div > '
                                                           'div:nth-child(2) > div > form > button')

        # Делаем видимой область для вставки решенного токена для нашей капчи
        driver.execute_script("arguments[0].setAttribute('style','')", text)
        await asyncio.sleep(random.randint(1, 3))
        # Делаем видимым кнопку Login
        driver.execute_script("document.querySelector('[type^=submit]').removeAttribute('disabled')")
        await asyncio.sleep(random.randint(1, 3))
        button_login.click()
        await asyncio.sleep(random.randint(1, 3))
        text.send_keys(token)
        button_login.click()
        await asyncio.sleep(5)

    elif "recaptcha" in driver.page_source.lower():
        print("На сайте используется reCAPTCHA")


def subscribed(sub_txt):
    return "подписной" in sub_txt.text.lower()


def liked(post):
    like = post.find_element_by_class_name('b-post__tools').find_element_by_tag_name('button')
    return "m-active" in like.get_attribute('class')


def commented(post):
    comment = post.find_element_by_class_name('b-post__tools').find_elements_by_tag_name('button')[1]
    if not comment.is_enabled():
        print("Коменты отключены")
        return True

    comment.click()
    time.sleep(3)

    if "/u119709885" in post.find_element_by_class_name('b-comments').get_attribute('innerHTML'):
        print("Коментарий уже есть")
        time.sleep(3)
        return True

    print("Коментария нет")
    return False


async def main():
    global prev_comment
    global last_model
    driver.get(only_fans_url)
    await asyncio.sleep(random.randint(2, 5))

    username = driver.find_elements_by_class_name('v-text-field__slot')[0].find_element_by_tag_name('input')
    password = driver.find_elements_by_class_name('v-text-field__slot')[1].find_element_by_tag_name('input')

    # Отправляем в поля username и password и нажимаем ENTER
    username.send_keys(bot_username)
    await asyncio.sleep(random.randint(2, 3))
    password.send_keys(bot_password)
    await asyncio.sleep(random.randint(1, 3))
    password.send_keys(Keys.ENTER)
    await asyncio.sleep(random.randint(2, 5))
    # await asyncio.sleep(10)
    # password.send_keys(Keys.ENTER)
    # await asyncio.sleep(3)

    # Начинаем проходиться по списку модолей (ссылок)
    for _ in range(100):
        await asyncio.sleep(random.randint(2, 5))
        driver.get(only_fans_url + '/' + models[last_model])
        print("----------------------------------------------")
        print("Переходим к модели : ", models[last_model])
        await asyncio.sleep(5)
        sub_txt = driver.find_element_by_class_name('b-btn-text')

        # Подписываемся если не подписались
        if not subscribed(sub_txt):
            print("Подписываемся на модель : ", models[last_model])
            sub_txt.click()
            await asyncio.sleep(random.randint(3, 6))

        posts = driver.find_elements_by_class_name('b-post__wrapper')
        await asyncio.sleep(random.randint(2, 4))

        # Проверяем посты на лайки и коменты
        print("Лайкаем и коментируем посты...")
        i = 0
        for post in posts:
            if i == 2:
                break

            try:
                if post.find_element_by_tag_name('div').get_attribute('class') == "b-post m-stream-post is-not-post-page":
                    print("Первый пост - стрим")
                    continue
                post.find_elements_by_tag_name('div')
            except Exception as err:
                print("[ОШИБКА] : ", err.args)
                continue

            if not liked(post) and post.find_element_by_class_name('b-post__tools').find_element_by_tag_name(
                    'button').is_enabled():
                post.find_element_by_class_name('b-post__tools').find_element_by_tag_name('button').click()
                print("Лайк !")

            await asyncio.sleep(random.randint(3, 5))

            if not commented(post):
                print("Пишем коментарий...")
                driver.execute_script("window.scrollBy(0,250)")
                await asyncio.sleep(2)

                text_area = post.find_element_by_class_name('b-comments__form').find_element_by_tag_name('textarea')
                current_comment = comments[random.randint(0, len(comments))]

                while current_comment == prev_comment:
                    current_comment = comments[random.randint(0, len(comments))]

                await asyncio.sleep(2)

                text_area.send_keys(current_comment)
                await asyncio.sleep(2)
                prev_comment = current_comment

                # Отправляем коментарий...
                post.find_element_by_class_name('b-comments__form').find_element_by_class_name(
                    'g-btn.m-rounded.m-icon.m-icon-only.m-colored.m-sm-size.b-comments__btn-submit').click()
                await asyncio.sleep(random.randint(2, 5))

            i += 1

        # Передвигаем индекс последней модели
        last_model += 1
        with open('last_model.txt', 'w') as f:
            f.write(str(last_model))

        await asyncio.sleep(random.randint(2, 5))


# Запускаем бота
if __name__ == '__main__':
    asyncio.run(main())

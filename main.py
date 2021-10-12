# Импорт нужных библиотек и скриптов
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import captcha_resolver
import time
import asyncio
import random
import datetime
import csv
import data_base_connector as db
from bot import set_up_bot


only_fans_url = 'http://onlyfans.com'
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


# --------------------------- Работа с БД ---------------------------

# Получаем аккаунты
accounts = db.get_accounts()

# Получаем модели
models = db.get_models()

# --------------------------- Работа с БД ---------------------------


def exist(elem, name="div", by="selector"):
    try:
        if by == "selector":
            elem.find_element_by_css_selector(name)
        elif by == "id":
            elem.find_element_by_id(name)
        elif by == "class":
            elem.find_element_by_class_name(name)
        elif by == "tag":
            elem.find_element_by_tag_name(name)
    except NoSuchElementException:
        return False
    return True


# Проверка на рекламу
def has_adv(post):
    if exist(post, "b-post__text-el", "class"):
        if exist(post.find_element_by_class_name("b-post__text-el"), "a", "tag"):
            return True
        return False


# Проверка на подписку
def subscribed(sub_txt):
    return "подписной" in sub_txt[0].text.lower()


# Провекра что подписка бесплатная
def free(sub_txt):
    return "бесплатно" in sub_txt[1].text.lower()


# Проверка что лайк поставлен
def liked(post):
    like = post.find_element_by_class_name('b-post__tools').find_element_by_tag_name('button')
    return "m-active" in like.get_attribute('class')


# Проверка что комент есть
def commented(post):
    comment = post.find_element_by_class_name('b-post__tools').find_elements_by_tag_name('button')[1]

    comment.click()
    time.sleep(3)

    if "/u119709885" in post.find_element_by_class_name('b-comments').get_attribute('innerHTML'):
        print("Коментарий уже есть")
        time.sleep(2)
        return True

    print("Коментария нет")
    return False


def restrict(bot):
    bot.find_element_by_class_name("b-dropdown-text").click()
    print(bot.find_element_by_class_name("b-dropdown-text").text)
    print("Рестрикт !")


async def main():
    global prev_comment
    for account in accounts:
        print(f"Аккаунт : {account[0]}")
        bot = set_up_bot(account)
        # time.sleep(5)
        # last_sub_time = datetime.datetime.strptime(db.get_subs(accounts[0], last=True)[1], '%Y-%m-%d %H:%M:%S.%f')

        if not db.get_subs(account):
            last_model = 0
        else:
            last_model = models.index(db.get_model(db.get_subs(account, last=True)[0]))
        print("Индекс модели с которой законяили на этом аккаунте : ", last_model)

        if db.get_today_subs(account) == 0:
            print("Кол-во подписок на сегодня : ", db.get_today_subs(account))
            # print("Делаем проверку на прохождение 24 часов...")
            # if (datetime.datetime.now() - last_sub_time).days >= 1:
            #     print("24 часа прошли можно начинать подписываться")
            # else:
            #     print("24 часа ещё не прошли подписываться нельзя, переходим к следующему аккаунту...")
            #     continue
        if db.get_today_subs(account) == 100:
            print("100 подписок есть на аккаунте : ", account[0])
            bot.close()
            bot.quit()
            continue

        # Переходим на стартовую страницу
        bot.get(only_fans_url)
        time.sleep(random.randint(4, 6))

        username = bot.find_elements_by_class_name('v-text-field__slot')[0].find_element_by_tag_name('input')
        password = bot.find_elements_by_class_name('v-text-field__slot')[1].find_element_by_tag_name('input')

        # Отправляем в поля username и password и нажимаем ENTER
        username.send_keys(account[0])
        await asyncio.sleep(random.randint(2, 3))
        password.send_keys(account[1])
        await asyncio.sleep(random.randint(1, 3))
        time.sleep(20)

        # Начинаем проходиться по списку модолей (ссылок)
        while db.get_today_subs(account) < 100:
            await asyncio.sleep(random.randint(2, 5))
            bot.get(only_fans_url + '/' + models[last_model])
            print("----------------------------------------------")
            print("Переходим к модели : ", models[last_model])

            await asyncio.sleep(5)
            if exist(bot, "b-404", "class"):
                last_model += 1
                continue
            time.sleep(5)

            # Проверка на то что подписка бесплатная
            sub_txt = bot.find_elements_by_class_name('b-btn-text')[:2]
            if not free(sub_txt):
                print("Это платная модель")
                last_model += 1
                # TODO: удалить из БД эту платную модель
                continue

            # Подписываемся если не подписались
            if not subscribed(sub_txt):
                print("Подписываемся на модель : ", models[last_model])
                sub_txt[0].click()
                time.sleep(random.randint(5, 8))
            else:
                print(f"Мы уже подписаны на {models[last_model]}")

            # Записываем подписку в БД
            if db.get_model_id(models[last_model]) not in db.get_subs(account):
                db.add_sub(models[last_model], account, datetime.datetime.now())
            else:
                print("Такая модель уже есть в БД")

            time.sleep(3)
            print(f"Кол-во подписок за этот день : {db.get_today_subs(account)}")

            # Находим посты
            print("Находим посты...")
            posts = bot.find_elements_by_class_name('b-post__wrapper')
            time.sleep(random.randint(3, 5))

            # Фильтруем невидимые посты
            posts = list(filter(lambda x: exist(x, "div", "tag"), posts))

            # Делаем проверку на рестрикт (нельзя коментить посты)
            if not list(filter(lambda x: x.find_element_by_class_name(
                    'b-post__tools').find_elements_by_tag_name('button')[1].is_enabled(), posts)):
                print("Нельзя комментировать посты")

                restrict_txt = ""
                bot.find_element_by_class_name("g-icon.has-tooltip").click()
                if exist(name="b-dropdown-text", by="class"):
                    restrict_txt = bot.find_element_by_class_name("b-dropdown-text").text

                if restrict_txt == "Ограничить":
                    restrict(bot)
            else:
                print("Комментировать посты можно")

            # Фильтруем посты без рекламы
            print("Фильтруем посты с рекламой")
            posts = list(filter(lambda x: not has_adv(x), posts))

            # Проверяем посты на лайки и коменты
            print("Лайкаем и коментируем посты...")
            i = 0
            for post in posts:
                if i == 2:
                    break

                if post.find_element_by_tag_name('div').get_attribute(
                        'class') == "b-post m-stream-post is-not-post-page":
                    print("Пост - стрим")
                    continue

                # Если нет лайка и можно лайкать, то лайкаем пост
                if post.find_element_by_class_name('b-post__tools').find_element_by_tag_name(
                        'button').is_enabled() and not liked(post):
                    post.find_element_by_class_name('b-post__tools').find_element_by_tag_name('button').click()
                    print("Лайк !")

                time.sleep(random.randint(2, 4))

                # Коменты
                if post.find_element_by_class_name('b-post__tools').find_elements_by_tag_name(
                        'button')[1].is_enabled() and not commented(post):
                    print("Пишем коментарий...")
                    bot.execute_script("window.scrollBy(0, 300)")
                    time.sleep(1)

                    # Находим поле для ввода комента
                    text_area = post.find_element_by_class_name('b-comments__form').find_element_by_tag_name('textarea')
                    current_comment = comments[random.randint(0, len(comments) - 1)]

                    while current_comment == prev_comment:
                        current_comment = comments[random.randint(0, len(comments) - 1)]

                    time.sleep(1)

                    text_area.send_keys(current_comment)
                    await asyncio.sleep(1.5)
                    prev_comment = current_comment

                    # Отправляем коментарий...
                    post.find_element_by_class_name('b-comments__form').find_element_by_class_name(
                        'g-btn.m-rounded.m-icon.m-icon-only.m-colored.m-sm-size.b-comments__btn-submit').click()
                    await asyncio.sleep(random.randint(2, 4))

                i += 1
            last_model += 1
            await asyncio.sleep(random.randint(2, 4))
        print(f"100 подписок на аккаунте {account[0]}, сделаны")
        bot.close()
        bot.quit()


# Запускаем бота
if __name__ == '__main__':
    asyncio.run(main())

from selenium.common.exceptions import NoSuchElementException
from models_parser import parse_models, set_up_parser
from selenium.webdriver.common.keys import Keys
from seleniumwire import webdriver
import data_base_connector as db
import datetime
import random
import time

only_fans_url = 'http://onlyfans.com'
prev_comment = ""
models = []
comments = []
accounts = []
start_acc = 0


# Натсройка веб - драйвера
def set_up_bot(account):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-extensions")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    proxy_options = {
        "proxy": {
            "https": f"https://{account[4]}:{account[5]}@{account[2]}:{account[3]}"
        }
    }
    driver = webdriver.Chrome(options=options, seleniumwire_options=proxy_options)
    driver.set_window_rect(980, 10)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.delete_all_cookies()
    return driver


def new_models():
    global prev_comment
    for account in accounts[start_acc:]:
        nickname = account[6]
        print(f"Аккаунт : {account[0]} | {nickname}")
        bot = set_up_bot(account)
        time.sleep(2)

        if not db.get_subs(account):
            last_model = 0
        else:
            last_model = models.index(db.get_model(db.get_subs(account, last=True)[0]))
            last_sub_time = datetime.datetime.strptime(db.get_subs(account, last=True)[1], '%Y-%m-%d %H:%M:%S.%f')
            if db.get_today_subs(account) == 0:
                print("Кол-во подписок на сегодня : ", db.get_today_subs(account))
                print("Делаем проверку на прохождение 24 часов...")
                if (datetime.datetime.now() - last_sub_time).days >= 1:
                    print("24 часа прошли можно начинать подписываться")
                else:
                    print("24 часа ещё не прошли подписываться нельзя, переходим к следующему аккаунту...")
                    bot.close()
                    bot.quit()
                    continue

            elif db.get_today_subs(account) == 100:
                print("100 подписок есть на аккаунте : ", account[0])
                bot.close()
                bot.quit()
                continue
            print(
                f"Модель с которой закончили на этом аккаунте : [Индекс] {last_model} | [Никнейм] {models[last_model]}")

        if last_model == len(models) - 1:
            print("Это последняя модель, нужно спарсить новые...")
            parse_models(set_up_parser())
            return

        # Переходим на стартовую страницу
        bot.get(only_fans_url)
        time.sleep(random.randint(4, 6))

        username = bot.find_elements_by_class_name('v-text-field__slot')[0].find_element_by_tag_name('input')
        password = bot.find_elements_by_class_name('v-text-field__slot')[1].find_element_by_tag_name('input')

        # Отправляем в поля username и password и нажимаем ENTER
        username.send_keys(account[0])
        time.sleep(random.randint(2, 3))
        password.send_keys(account[1])
        time.sleep(random.randint(1, 3))
        password.send_keys(Keys.ENTER)
        time.sleep(30)

        # Начинаем проходиться по списку модолей (ссылок)
        while db.get_today_subs(account) < 100:
            try:
                time.sleep(random.randint(2, 5))
                bot.get(only_fans_url + '/' + models[last_model])
                print("----------------------------------------------")
                print("Переходим к модели : ", models[last_model])

                time.sleep(6)
                if exist(bot, "b-404", "class"):
                    db.delete_model(models[last_model])
                    time.sleep(1)
                    last_model += 1
                    continue
                time.sleep(2)

                if banned(bot):
                    print("Модель забанена")
                    last_model += 1
                    continue

                sub_txt = bot.find_element_by_class_name('b-btn-text')
                # Проверка на то что подписка бесплатная
                if not free(bot):
                    print("Это платная модель")
                    db.delete_model(models[last_model])
                    time.sleep(1)
                    last_model += 1
                    continue

                # Подписываемся если не подписались
                if not subscribed(sub_txt):
                    print("Подписываемся на модель : ", models[last_model])
                    sub_txt.click()
                    time.sleep(random.randint(6, 8))
                else:
                    print(f"Мы уже подписаны на {models[last_model]}")

                # Записываем подписку в БД
                if db.get_model_id(models[last_model]) not in db.get_subs(account):
                    print("Записываем модель в БД...")
                    db.add_sub(models[last_model], account, datetime.datetime.now())
                else:
                    print("Такая модель уже есть в БД")

                time.sleep(2)
                print(f"Кол-во подписок за этот день : {db.get_today_subs(account)}")

                # Находим посты
                print("Находим посты...")
                time.sleep(random.randint(2, 4))
                bot.execute_script("window.scrollBy(0, 300)")
                time.sleep(random.randint(3, 5))
                posts = bot.find_elements_by_class_name('b-post__wrapper')
                time.sleep(1)

                # Фильтруем невидимые посты
                posts = list(filter(lambda x: exist(x, "div", "tag"), posts))

                print("Количество постов : ", len(posts))

                # Делаем проверку на рестрикт (нельзя коментить посты)
                posts = list(filter(lambda x: x.find_element_by_class_name(
                    'b-post__tools').find_elements_by_tag_name('button')[1].is_enabled(), posts))
                print("Количество постов, которые можно комментировать : ", len(posts))
                if not posts:
                    print("Нельзя комментировать посты")

                    restrict_txt = ""
                    if exist(bot, name="b-dropdown-wrapper", by="class"):
                        if not exist(bot, name="b-dropdown-text", by="class"):
                            print("Мы в бане у этой модели")
                            last_model += 1
                            continue
                        else:
                            restrict_txt = bot.find_element_by_class_name("b-dropdown-text").text
                    else:
                        bot.find_element_by_class_name("g-icon.has-tooltip").click()
                        if not exist(bot, name="b-dropdown-text", by="class"):
                            print("Мы в бане у этой модели")
                            last_model += 1
                            continue
                        else:
                            restrict_txt = bot.find_element_by_class_name("b-dropdown-text").text

                    if restrict_txt == "Ограничить":
                        restrict(bot)
                    elif restrict_txt == "Неограниченный":
                        print("Модель уже в рестрикте")
                    print("Переходим к следующей моделе")
                    last_model += 1
                    continue
                else:
                    print("Комментировать посты можно")

                # Фильтруем посты без рекламы
                print("Фильтруем посты с рекламой")
                posts = list(filter(lambda x: not has_adv(x), posts))
                print("Количество постов без рекламы : ", len(posts))

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
                            'button')[1].is_enabled() and not commented(post, nickname):
                        print("Пишем коментарий...")
                        bot.execute_script("window.scrollBy(0, 300)")
                        time.sleep(1)

                        JS_ADD_TEXT_TO_INPUT = """
                                                  var elm = arguments[0], txt = arguments[1];
                                                  elm.value += txt;
                                                  elm.dispatchEvent(new Event('change'));
                                                  """

                        # Находим поле для ввода комента
                        text_area = post.find_element_by_class_name('b-comments__form').find_element_by_tag_name(
                            'textarea')
                        current_comment = comments[random.randint(0, len(comments) - 1)]

                        while current_comment == prev_comment:
                            current_comment = comments[random.randint(0, len(comments) - 1)]

                        time.sleep(1)

                        text_area.send_keys(" ")
                        time.sleep(0.5)
                        bot.execute_script(JS_ADD_TEXT_TO_INPUT, text_area, current_comment)
                        time.sleep(0.5)
                        text_area.send_keys(" ")
                        time.sleep(0.5)
                        prev_comment = current_comment

                        # Отправляем коментарий...
                        post.find_element_by_class_name('b-comments__form').find_element_by_class_name(
                            'g-btn.m-rounded.m-icon.m-icon-only.m-colored.m-sm-size.b-comments__btn-submit').click()
                        time.sleep(random.randint(2, 4))

                    i += 1
                last_model += 1
                time.sleep(random.randint(2, 4))
            except Exception as err:
                with open('log_new_models.txt', 'w') as f:
                    f.write(f"Ошибка - {err} {type(err)=}, {err.args}, {datetime.datetime.now()}")
                    f.close()
                print("Какая-то ошибка...")
                print("Переходим к следующей моделе")
                last_model += 1
                continue
        print(f"100 подписок на аккаунте {account[0]}, сделаны")
        bot.close()
        bot.quit()


def old_models():
    global prev_comment
    for account in accounts[start_acc:]:
        nickname = account[6]
        print(f"Аккаунт : {account[0]} | {nickname}")
        sub_models = [db.get_model(value) for value in db.get_subs(account)]
        sub_models = list(filter(lambda x: x is not None, sub_models))
        bot = set_up_bot(account)
        last_model = 0
        time.sleep(2)

        # Переходим на стартовую страницу
        bot.get(only_fans_url)
        time.sleep(random.randint(4, 6))

        username = bot.find_elements_by_class_name('v-text-field__slot')[0].find_element_by_tag_name('input')
        password = bot.find_elements_by_class_name('v-text-field__slot')[1].find_element_by_tag_name('input')

        # Отправляем в поля username и password и нажимаем ENTER
        username.send_keys(account[0])
        time.sleep(random.randint(2, 3))
        password.send_keys(account[1])
        time.sleep(random.randint(1, 3))
        password.send_keys(Keys.ENTER)
        time.sleep(30)

        # Начинаем проходиться по списку модолей (ссылок)
        for i, model in enumerate(sub_models):
            try:
                time.sleep(random.randint(2, 5))
                bot.get(only_fans_url + '/' + model)
                print("----------------------------------------------")
                print("Переходим к модели : ", model)
                time.sleep(5)

                # Находим посты
                print("Находим посты...")
                time.sleep(random.randint(2, 4))
                bot.execute_script("window.scrollBy(0, 300)")
                time.sleep(random.randint(3, 5))
                posts = bot.find_elements_by_class_name('b-post__wrapper')
                time.sleep(2)

                # Фильтруем невидимые посты
                posts = list(filter(lambda x: exist(x, "div", "tag"), posts))
                time.sleep(1)

                print("Количество постов : ", len(posts))

                # Делаем проверку на рестрикт (нельзя коментить посты)
                posts = list(filter(lambda x: x.find_element_by_class_name(
                    'b-post__tools').find_elements_by_tag_name('button')[1].is_enabled(), posts))
                print("Количество постов, которые можно комментировать : ", len(posts))
                if not posts:
                    print("Нельзя комментировать посты")

                    restrict_txt = ""
                    if exist(bot, name="b-dropdown-wrapper", by="class"):
                        if not exist(bot, name="b-dropdown-text", by="class"):
                            print("Мы в бане у этой модели")
                            last_model += 1
                            continue
                        else:
                            restrict_txt = bot.find_element_by_class_name("b-dropdown-text").text
                    else:
                        bot.find_element_by_class_name("g-icon.has-tooltip").click()
                        if not exist(bot, name="b-dropdown-text", by="class"):
                            print("Мы в бане у этой модели")
                            last_model += 1
                            continue
                        else:
                            restrict_txt = bot.find_element_by_class_name("b-dropdown-text").text

                    if restrict_txt == "Ограничить":
                        restrict(bot)
                    elif restrict_txt == "Неограниченный":
                        print("Модель уже в рестрикте")
                    print("Переходим к следующей моделе")
                    last_model += 1
                    continue
                else:
                    print("Комментировать посты можно")

                # Фильтруем посты без рекламы
                print("Фильтруем посты с рекламой")
                posts = list(filter(lambda x: not has_adv(x), posts))
                print("Количество постов без рекламы : ", len(posts))

                # Проверяем посты на лайки и коменты
                print("Лайкаем и коментируем посты...")
                i = 0
                for post in posts:
                    if i == 3:
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
                            'button')[1].is_enabled() and not commented(post, nickname):
                        print("Пишем коментарий...")
                        bot.execute_script("window.scrollBy(0, 300)")
                        time.sleep(1)

                        JS_ADD_TEXT_TO_INPUT = """
                        var elm = arguments[0], txt = arguments[1];
                        elm.value += txt;
                        elm.dispatchEvent(new Event('change'));
                        """

                        # Находим поле для ввода комента
                        text_area = post.find_element_by_class_name('b-comments__form').find_element_by_tag_name(
                            'textarea')
                        current_comment = comments[random.randint(0, len(comments) - 1)]

                        while current_comment == prev_comment:
                            current_comment = comments[random.randint(0, len(comments) - 1)]

                        time.sleep(1)

                        text_area.send_keys(" ")
                        time.sleep(0.5)
                        bot.execute_script(JS_ADD_TEXT_TO_INPUT, text_area, current_comment)
                        time.sleep(0.5)
                        text_area.send_keys(" ")
                        time.sleep(0.5)
                        prev_comment = current_comment

                        # Отправляем коментарий...
                        post.find_element_by_class_name('b-comments__form').find_element_by_class_name(
                            'g-btn.m-rounded.m-icon.m-icon-only.m-colored.m-sm-size.b-comments__btn-submit').click()
                        time.sleep(random.randint(2, 4))

                    i += 1
                last_model += 1
                time.sleep(random.randint(1, 3))
            except Exception as err:
                with open('log_old_models.txt', 'w') as f:
                    f.write(f"Ошибка - {err} {type(err)=}, {datetime.datetime.now()}")
                    f.close()
                print("Какая-то ошибка...")
                print("Переходим к следующей моделе")
                # raise
                last_model += 1
                continue
        bot.close()
        bot.quit()


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
    return "подписной" in sub_txt.text.lower()


# Провекра что подписка бесплатная
def free(bot):
    return not exist(bot, "b-btn-text__small", "class")


# Проверка что лайк поставлен
def liked(post):
    like = post.find_element_by_class_name('b-post__tools').find_element_by_tag_name('button')
    return "m-active" in like.get_attribute('class')


# Проверка что комент есть
def commented(post, nickname):
    comment = post.find_element_by_class_name('b-post__tools').find_elements_by_tag_name('button')[1]

    comment.click()
    time.sleep(3)
    comments = post.find_element_by_class_name('b-comments').get_attribute('innerHTML')
    if nickname in comments:
        print("Коментарий уже есть")
        time.sleep(2)
        return True

    print("Коментария нет")
    return False


def restrict(bot):
    bot.find_element_by_class_name("b-dropdown-text").click()
    print("Рестрикт !")


def banned(bot):
    if exist(bot, "g-icon.has-tooltip", "class"):
        bot.find_element_by_class_name("g-icon.has-tooltip").click()
        time.sleep(1)
        text = bot.find_element_by_class_name("m-danger").find_element_by_class_name("dropdown-item").text
        if text == "Разблокировать":
            return True
    return False

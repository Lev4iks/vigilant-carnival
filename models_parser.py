from selenium.webdriver.common.keys import Keys
import undetected_chromedriver.v2 as uc
import data_base_connector as db
import datetime
import random
import time


only_finder_url = 'http://onlyfinder.com'
only_finder_free_url = 'https://onlyfinder.com/female-free/profiles/'


def set_up_parser():
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
    return driver


def parse_models(driver):
    location = db.get_locations()[0]
    if not location:
        print("Нет новых локаций, нужно добавить новые...")
        return
    try:

        print("Переходим на сайт : ", only_finder_url)
        driver.get(only_finder_url)
        driver.reconnect()
        driver.get(only_finder_free_url)
        time.sleep(random.randint(3, 6))

        # Вбиваем в строку происка локацию
        search = driver.find_element_by_css_selector('#navbar-input')
        search.send_keys(f' {location}')
        # Отправляем ENTER
        search.send_keys(Keys.ENTER)
        time.sleep(random.randint(2, 5))

        page = driver.find_element_by_css_selector('body')
        page_url = driver.current_url
        # Скролим вниз пока не дойдем до самого низа
        for i in range(200):
            page.send_keys(Keys.PAGE_DOWN)
            page.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)

        print("Страница прокручена, получаем данные...")

    except Exception as err:
        with open('log_old_models.txt', 'w') as f:
            f.write(f"Ошибка - {err} {type(err)=}, {datetime.datetime.now()}")
            f.close()
        print("Какая-то ошибка в работе парсера")
        return

    # Находим все результаты о моделях и потом записываем все ссылки на профили моделей
    results = driver.find_elements_by_class_name('result')
    models = [result.find_element_by_class_name('divLink').get_attribute('href')[21:] for result in results]

    # Записываем данные (ссылки) в БД
    db.add_models(models)
    db.cursor.execute("UPDATE locations SET IsUsed = ?, UsageDate = ? WHERE Location = ? ",
                      [1, datetime.datetime.today(), location])
    db.db.commit()

    print("Полученные модели : ", *models)

    driver.quit()

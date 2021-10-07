from selenium.webdriver.common.keys import Keys
import random
import asyncio
import csv


only_finder_url = 'http://onlyfinder.com'


async def parse_models(driver):
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

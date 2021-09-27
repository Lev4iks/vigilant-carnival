from selenium import webdriver
import time


def main():

    driver = webdriver.Chrome(executable_path="chromedriver/chromedriver.exe")
    driver.get('https://dtf.ru/indie/845827-rogues-tales-poltora-goda-v-odnoy-state')
    time.sleep(5)


if __name__ == '__main__':
    main()

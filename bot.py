from seleniumwire import webdriver


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
    # driver.clear_cdp_listeners()
    return driver

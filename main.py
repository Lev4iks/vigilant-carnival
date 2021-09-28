import undetected_chromedriver.v2 as uc
from bs4 import BeautifulSoup
import time


options = uc.ChromeOptions()

# задаес профиль
options.user_data_dir = "c:\\temp\\profile"

# задаем настройки для обхода cloudflare
options.add_argument('--user-data-dir=c:\\temp\\profile2')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-setuid-sandbox")

# чтобы не вылазили окна на старте
options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
browser = uc.Chrome()
with browser:
    # Переход к списку модолей (FREE)
    browser.get('https://onlyfinder.com/free-accounts')
    html = browser.page_source
    soup = BeautifulSoup(html, 'html5lib')
    print(soup)

import logging
import random
import time

import requests
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='out.log',
    filemode='a',
    encoding='utf-8'
)

logger = logging.getLogger('Loger')


def load_proxies(filename="proxies.txt"):
    try:
        with open(filename, 'r') as file:
            proxies = [line.strip() for line in file.readlines()]
        return proxies
    except FileNotFoundError:
        logger.error(f"Файл {filename} не знайден")
        return []



def get_random_proxy(proxies):
    if not proxies:
        logger.error("Список проксі порожній")
        return None
    return random.choice(proxies)



def init_browser(proxies):
    options = uc.ChromeOptions()
    options.page_load_strategy = 'eager'
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument("--detach")
    options.add_argument('--disable-popup-blocking')


    proxy = get_random_proxy(proxies)
    if proxy:
        options.add_argument(f'--proxy-server=socks5://{proxy}')
        logger.info(f'Встановлено проксі: {proxy}')
    else:
        logger.warning("Проксі не встановлено")


    driver = uc.Chrome(options=options)
    return driver


def account_login(driver, login, password):
    driver.get('https://www.linkedin.com/login')

    email_elem = driver.find_element(By.ID, 'username')
    password_elem = driver.find_element(By.ID, 'password')

    email_elem.send_keys(login)
    password_elem.send_keys(password)

    password_elem.send_keys(Keys.RETURN)
    time.sleep(3)



def parse_profile_picture(driver, username):

    driver.get(f'https://www.linkedin.com/in/{username}')
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    profile_pic_tag = soup.find('img', {'class': 'evi-image ember-view profile-photo-edit__preview'})

    if profile_pic_tag:
        profile_pic_url = profile_pic_tag['src']
        return profile_pic_url
    else:
        return None


def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
            print(f'Фото профілю збережено як {filename}')
            logger.info(f'Фото профілю збережено як {filename}')
    else:
        print('Не вдалось скачати фото')
        logger.info(f'Не вдалось скачати фото')




def check_for_captcha(driver):
    captcha_classes = ['captcha', 'g-recaptcha', 'captcha-container']

    for captcha_class in captcha_classes:
        try:
            captcha_element = driver.find_element(By.CLASS_NAME, captcha_class)
            if captcha_element:
                return True
        except Exception as e:
            pass

    return False


def handle_captcha(driver, proxies):
    if check_for_captcha(driver):
        logger.warning('Вилізла капча, міняємо проксі')
        driver.quit()
        driver = init_browser(proxies)
        logger.info('Браузер перезапущено з новими проксі')
    return driver



def main():
    login = input('Введіть логін')
    password = input('Введіть пароль')
    username = input("Введить ендпоінт аккаунту, приклад: denis-holovkin-3a2139339")

    proxies = load_proxies("proxies.txt")
    driver = init_browser(proxies)

    logger.info(f'Запускаємо браузер')

    try:
        account_login(driver, login, password)
        logger.info(f'Вводимо данні: Логін: {login} , Пароль: {password}')


        driver = handle_captcha(driver, proxies)

        profile_pic_url = parse_profile_picture(driver, username)
        logger.info(f'Пробуєм отримати посилання на фото профілю')

        if profile_pic_url:
            download_image(profile_pic_url, 'profile_picture.jpg')
        else:
            print('Не вдалось знайти фото профілю')
            logger.info(f'Не вдалось знайти фото профілю')
    finally:
        driver.quit()


if __name__ == '__main__':
    main()

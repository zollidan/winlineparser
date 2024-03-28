import datetime
import logging
import time
import typing
import uuid

import chromedriver_autoinstaller
import xlsxwriter
from art import tprint
from bs4 import BeautifulSoup
from colorama import Fore
from colorama import init
from colorama import just_fix_windows_console
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm

from config import PARSER_URL, COUNTRY_CLICK_XPATH, LEAGUE_BLOCK_XPATH, LEAGUE_NAME_CLASS, \
    MATCHES_BLOCK_CLASS, EXCEL_HEADERS, BOTTOM_SIGN, ITERATIONS_TO_BOTTOM, CATEGORY_CONTAINER, \
    BG_COUPON_ROW, change_month, change_date, DEBUG_MODE
from schemas import FootballRow


class MainDriver:
    @staticmethod
    def init_driver() -> WebDriver:
        chromedriver_autoinstaller.install()

        try:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--ignore-certificate-errors")
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            prefs = {"profile.default_content_settings.popups": 0,
                     "download.prompt_for_download": False,
                     "download.directory_upgrade": True,
                     "credentials_enable_service": False}
            options.add_experimental_option("prefs", prefs)
            options.add_argument('log-level=3')
            return webdriver.Chrome(options=options)
        except Exception:
            return None

    def __init__(self):
        self.driver = self.init_driver()

        logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
        logger.setLevel(logging.WARNING)
        if self.driver is None:
            print(Fore.RED + "Chromedriver initialization error(#1)")
            raise Exception("Chromedriver initialization error(#1)")

    def close(self):
        self.driver.quit()

    def open_page(self, url):
        self.driver.get(url)

    def find_element(self, xpath) -> WebElement | None:
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return self.driver.find_element(By.XPATH, xpath)
        except TimeoutException:
            return None

    def find_elements(self, xpath) -> list[WebElement]:
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return self.driver.find_elements(By.XPATH, xpath)
        except TimeoutException:
            return []

    def click(self, element: WebElement) -> typing.NoReturn:
        self.driver.execute_script('arguments[0].click()', element)

    def scroll_into_view(self, element: WebElement) -> typing.NoReturn:
        self.driver.execute_script('arguments[0].scrollIntoView(true)', element)

print(Fore.GREEN + "собираю дату")

main_driver = MainDriver()

main_driver.open_page(PARSER_URL)

bottom_sign = main_driver.find_element(BOTTOM_SIGN)

for i in tqdm(range(ITERATIONS_TO_BOTTOM), desc='обрабатываю сайт секундочку'):
    main_driver.scroll_into_view(bottom_sign)
    time.sleep(0.5)

leagues = main_driver.find_elements(CATEGORY_CONTAINER)

leagues_list = []

for league in leagues:
    leagues_list.append(league)


def games_counter():
    games = main_driver.find_elements(BG_COUPON_ROW)

    games_list = []

    for game in games:
        games_list.append(game)
    return games_list


print(f"я нашел {len(games_counter())} игры за 24 часа, работаем...")

"""
ДОБАВИТЬ TQDM НА ПРОГРЕСС БАР МАТЧЕЙ ЧТОБЫ ДОБАВЛЯЛ ***len(games_in_league)***
"""

# main_pbar = tqdm(desc="собираю матчи", total=len(games_counter()))

for one_league in leagues_list:
    games_in_league = one_league.find_elements(By.CLASS_NAME, 'bg')

    league_name = one_league.find_element(By.CLASS_NAME, "category-label").text

    if DEBUG_MODE:
        print(f"название лиги: {league_name}, матчей в лиге: {len(games_in_league)}")

    for one_game in games_in_league:
        # game_dict = []

        team1 = one_game.find_elements(By.CLASS_NAME, 'member-link')[0].text
        team2 = one_game.find_elements(By.CLASS_NAME, 'member-link')[1].text

        class_date = one_game.find_element(By.CLASS_NAME, 'date').text

        day_of_game = change_date(class_date)[0]
        month_of_game = change_date(class_date)[1]
        year_of_game = change_date(class_date)[2]
        time_of_game = change_date(class_date)[3]

        coffi0 = one_game.find_elements(By.CLASS_NAME, "height-column-with-price")[0].text
        coffi1 = one_game.find_elements(By.CLASS_NAME, "height-column-with-price")[1].text
        coffi2 = one_game.find_elements(By.CLASS_NAME, "height-column-with-price")[2].text
        coffi3 = one_game.find_elements(By.CLASS_NAME, "height-column-with-price")[3].text
        coffi4 = one_game.find_elements(By.CLASS_NAME, "height-column-with-price")[4].text
        coffi5 = one_game.find_elements(By.CLASS_NAME, "height-column-with-price")[5].text
        coffi6 = one_game.find_elements(By.CLASS_NAME, "height-column-with-price")[6].text
        coffi7 = one_game.find_elements(By.CLASS_NAME, "height-column-with-price")[7].text
        coffi8 = one_game.find_elements(By.CLASS_NAME, "height-column-with-price")[8].text
        coffi9 = one_game.find_elements(By.CLASS_NAME, "height-column-with-price")[9].text

        print(coffi9.split())

        if coffi9.split() != '(2.5)':
            print(False)

        # print(team1,
        #       team2,
        #       day_of_game,
        #       month_of_game,
        #       year_of_game,
        #       time_of_game,
        #       coffi1,
        #       coffi2,
        #       coffi3,
        #       coffi4,
        #       coffi5,
        #       coffi6,
        #       coffi7,
        #       coffi8,
        #       coffi9)

#     main_pbar.update(len(games_in_league))
# main_pbar.close()

input(Fore.BLUE + 'Press any key...')

exit()

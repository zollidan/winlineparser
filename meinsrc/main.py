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
    MATCHES_BLOCK_CLASS, EXCEL_HEADERS, BOTTOM_SIGN, COUPON_ROW_ITEM, ITERATIONS_TO_BOTTOM
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


# def change_date(month):
#     try:
#         # day = dateTime[0]
#         # month = dateTime[1]
#         # time = dateTime[2]
#         if month == "янв": month = "01"
#         if month == "фев": month = "02"
#         if month == "мар": month = "03"
#         if month == "апр": month = "04"
#         if month == "май": month = "05"
#         if month == "июн": month = "06"
#         if month == "июл": month = "07"
#         if month == "авг": month = "08"
#         if month == "сен": month = "09"
#         if month == "окт": month = "10"
#         if month == "ноя": month = "11"
#         if month == "дек": month = "12"
#     except IndexError:
#         if month == 1: month = "01"
#         if month == 2: month = "02"
#         if month == 3: month = "03"
#         if month == 4: month = "04"
#         if month == 5: month = "05"
#         if month == 6: month = "06"
#         if month == 7: month = "07"
#         if month == 8: month = "08"
#         if month == 9: month = "09"


print(Fore.GREEN + "собираю дату")

main_driver = MainDriver()

main_driver.open_page(PARSER_URL)

bottom_sign = main_driver.find_element(BOTTOM_SIGN)

for i in tqdm(range(ITERATIONS_TO_BOTTOM), desc='обрабатываю сайт секундочку'):
    main_driver.scroll_into_view(bottom_sign)
    time.sleep(0.5)

games = main_driver.find_elements(COUPON_ROW_ITEM)

games_list = []

for game in games:
    games_list.append(game)
print(f"я нашел {len(games_list)} матча за 24 часа, работаем...")

for one_game in games_list:
    team1 = one_game.find_elements(By.CLASS_NAME, 'member-link')[0].text
    team2 = one_game.find_elements(By.CLASS_NAME, 'member-link')[1].text

    coffi0 = one_game.find_elements(By.XPATH, "//td[@data-market-type='RESULT']")[0].text

    coffi1 = one_game.find_elements(By.XPATH, "//td[@data-market-type='RESULT']")[1].text

    coffi2 = one_game.find_elements(By.XPATH, "//td[@data-market-type='RESULT']")[2].text

    # coffi3 = one_game.find_elements('td', {'data-market-type': 'DOUBLE_CHANCE'})[0]
    #
    # coffi4 = one_game.find_elements('td', {'data-market-type': 'DOUBLE_CHANCE'})[1]
    #
    # coffi5 = one_game.find_elements('td', {'data-market-type': 'DOUBLE_CHANCE'})[2]
    #
    # coffi6 = one_game.find_elements('td', {'data-market-type': 'HANDICAP'})[0]
    #
    # coffi7 = one_game.find_elements('td', {'data-market-type': 'HANDICAP'})[1]
    #
    # coffi8 = one_game.find_elements('td', {'data-market-type': 'TOTAL'})[0]
    #
    # coffi9 = one_game.find_elements('td', {'data-market-type': 'TOTAL'})[1]

    print(team1, team2, coffi0, coffi1, coffi2) #, coffi3, coffi4, coffi5, coffi6, coffi7, coffi8, coffi9)

input(Fore.BLUE + 'Press any key...')

exit()

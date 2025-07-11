import logging
import pathlib
import time
import typing

import chromedriver_autoinstaller
import pandas as pd
import selenium
from art import tprint
from colorama import Fore
from selenium import webdriver
from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm

from config import PARSER_URL, BOTTOM_SIGN, ITERATIONS_TO_BOTTOM, CATEGORY_CONTAINER, \
    change_date, DEBUG_MODE, games_counter, VERSION

tprint("marafon")
print(f'version: {VERSION}')


class MainDriver:
    @staticmethod
    def init_driver() -> WebDriver:
        chromedriver_autoinstaller.install()

        try:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument('--ignore-ssl-errors')
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            prefs = {"profile.default_content_settings.popups": 0,
                     "download.prompt_for_download": False,
                     "download.directory_upgrade": True,
                     "credentials_enable_service": False}
            options.add_experimental_option("prefs", prefs)
            options.add_argument('log-level=3')
            return webdriver.Chrome(options=options)
        except Exception as e:
            return e

    def __init__(self):
        self.driver = self.init_driver()

        logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
        logger.setLevel(logging.WARNING)
        if self.driver is None:
            print(Fore.RED + "Chromedriver initialization error(#1)")
            raise Exception("Chromedriver initialization error(#1)")

    def quit(self):
        self.driver.quit()

    def close(self):
        self.driver.close()
    

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

    def current_url(self):
        return self.driver.current_url

    def page_source(self):
        return self.driver.page_source


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

print(f"я нашел {len(games_counter(main_driver))} игры за 24 часа, работаем...")

main_pbar = tqdm(desc="собираю матчи", total=len(games_counter(main_driver)))

# with open("page.html", 'w', encoding="utf-8") as file:
#     file.write(main_driver.page_source())
if DEBUG_MODE:
    print("записал новую страницу")

matrix = []

for one_league in leagues_list:
    if DEBUG_MODE:
        print("вошел в цикл")

    games_in_league = one_league.find_elements(By.CLASS_NAME, 'bg')

    league_name = one_league.find_element(By.CLASS_NAME, "category-label").text

    if DEBUG_MODE:
        print(f"название лиги: {league_name}, матчей в лиге: {len(games_in_league)}")

    for one_game in games_in_league:
        game_dict = []

        team1 = one_game.find_elements(By.CLASS_NAME, 'member-link')[0].text
        team2 = one_game.find_elements(By.CLASS_NAME, 'member-link')[1].text

        class_date = one_game.find_element(By.CLASS_NAME, 'date').text

        day_of_game = change_date(class_date)[0]
        month_of_game = change_date(class_date)[1]
        year_of_game = change_date(class_date)[2]
        time_of_game = change_date(class_date)[3]

        """
        ищу ссылку на игру
        """
        game_href = one_game.find_elements(By.CLASS_NAME, 'member-link')[0].get_attribute('href')

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

        """
        топовая идея, можно сначала сделать весь парсинг, потом замутить проверку, главное взять все ссылки на игры
        потом проверяю если коэфф не такой как надо то просто добавляю на это строчку еще и нужный запрос там делаю
        все дела вот такая вот идея даааа))
        """

        if DEBUG_MODE:
            print(team1,
                  team2,
                  day_of_game,
                  month_of_game,
                  year_of_game,
                  time_of_game,
                  coffi1,
                  coffi2,
                  coffi3,
                  coffi4,
                  coffi5,
                  coffi6,
                  coffi7,
                  coffi8,
                  coffi9)

        game_dict.append(team1)
        game_dict.append(team2)
        game_dict.append(league_name)
        game_dict.append(game_href)
        game_dict.append(day_of_game)
        game_dict.append(month_of_game)
        game_dict.append(year_of_game)
        game_dict.append(time_of_game)
        game_dict.append(coffi0)
        game_dict.append(coffi1)
        game_dict.append(coffi2)
        game_dict.append(coffi3)
        game_dict.append(coffi4)
        game_dict.append(coffi5)
        game_dict.append(coffi6)
        game_dict.append(coffi7)
        game_dict.append(coffi8.split()[0])
        game_dict.append(coffi8.split()[1])
        game_dict.append(coffi9.split()[1])

        matrix.append(game_dict)

    main_pbar.update(len(games_in_league))
main_pbar.close()

try:
    df = pd.DataFrame(matrix)
    df.columns = ['команда1',
                  'команда2',
                  'лига',
                  'ссылка',
                  'день',
                  'месяц',
                  'год',
                  'время',
                  '1',
                  'x',
                  '2',
                  '1х',
                  '12',
                  'х2',
                  'фора1',
                  'фора2',
                  'марафон',
                  'меньше',
                  'больше',
                  ]
    """
        далее делаю мега люлю и проверяю коэффы и ищу нужные
    """

    count_of_not_two_coffi = []

    for index, row in df.iterrows():
        if row['марафон'] != '(2.5)':
            count_of_not_two_coffi.append(index)

    main_driver.quit()

    main_driver = MainDriver()

    second_pbar = tqdm(desc="добираю коэффициенты", total=len(count_of_not_two_coffi))

    for index, row in df.iterrows():
        if row['марафон'] != '(2.5)':
            if DEBUG_MODE:
                print(row['ссылка'], index)
            main_driver.open_page(row['ссылка'])
            link_array = str(main_driver.current_url()).split("+")
            uniq_game_code = link_array[-1]
            total_class_id = 'shortcutLink_event' + uniq_game_code + 'type3'
            if DEBUG_MODE:
                print(f"динамический айдишник: {total_class_id}")
            totals_btn = main_driver.find_element(f"//td[@id='{total_class_id}']")

            try:
                main_driver.click(totals_btn)

                main_table = main_driver.find_elements(
                    "//body[1]/div[6]/div[1]/div[3]/div[1]/div[1]/div[3]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[3]/div[1]/div[1]/div[1]/table[2]/tbody[1]/tr")
      
                prices = []
                for price in main_table:
                    price = price.text.replace('\n', ' ')
                    if '(2.5)' in price:
                        price_spitted = price.split()
                        prices.append(price_spitted[1])
                        prices.append(price_spitted[3])

                df.loc[index, '2.5'] = '2.5'
                try:
                    df.loc[index, 'меньше2'] = prices[0]
                    df.loc[index, 'больше2'] = prices[1]
                    
                except IndexError:
                    if DEBUG_MODE:
                        print(f"\nпроизошла ошибка игры номер {index}")
                    df.loc[index, 'меньше2'] = "—"
                    df.loc[index, 'больше2'] = "—"
                    continue
            except selenium.common.exceptions.JavascriptException:
                print("тоталы не найдены на сайте")
                continue
            second_pbar.update(1)
        else:
            continue
            second_pbar.update(1)
        
    second_pbar.close()
    main_driver.quit()

    df.to_excel('marafon_data.xlsx', sheet_name='DATA', index=False)
except PermissionError:
    print('Скорее всего вы не закрыли файл эксель.')

input(Fore.BLUE + 'Press any key...')


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

from config import PARSER_URL, MENU_CLICK_XPATH, COUNTRY_CLICK_XPATH, LEAGUE_BLOCK_XPATH, LEAGUE_NAME_CLASS, MATCHES_BLOCK_CLASS, EXCEL_HEADERS
from schemas import FootballRow

tprint("Winline")
init()
just_fix_windows_console()


class MainDriver:
    @staticmethod
    def init_driver() -> WebDriver:
        chromedriver_autoinstaller.install()

        try:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--disable-blink-features=AutomationControlled")
            # options.add_argument("--ignore-certificate-errors")
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
        self.driver.execute_script('arguments[0].scrollIntoView()', element)


def date_validator(timestamp, v):
    try:
        if 'через' in v:
            data = v.split()[1].strip().split(':')
            return int(
                (datetime.datetime(
                    year=datetime.datetime.now().year,
                    month=datetime.datetime.now().month,
                    day=datetime.datetime.now().day,
                    hour=datetime.datetime.fromtimestamp(timestamp).hour,
                    minute=datetime.datetime.fromtimestamp(timestamp).minute,
                    second=datetime.datetime.fromtimestamp(timestamp).second
                ) + datetime.timedelta(minutes=int(data[0]), seconds=int(data[1]))).timestamp()
            )
        elif 'Сегодня' in v:
            data = v.split()[1].strip().split(':')
            return int(
                datetime.datetime(
                    year=datetime.datetime.now().year,
                    month=datetime.datetime.now().month,
                    day=datetime.datetime.now().day,
                    hour=int(data[0]),
                    minute=int(data[1]),
                    second=0
                ).timestamp()
            )
        elif 'Завтра' in v:
            data = v.split()[1].strip().split(':')
            return int(
                datetime.datetime(
                    year=datetime.datetime.now().year,
                    month=datetime.datetime.now().month,
                    day=datetime.datetime.now().day,
                    hour=int(data[0]),
                    minute=int(data[1]),
                    second=0
                ).timestamp() + 86400
            )
        else:
            data = v.strip()
            return int(datetime.datetime.strptime(data, '%d.%m.%y %H:%M').timestamp())
    except Exception as f:
        return 0



try:
    days_timestamp = datetime.datetime.now().timestamp() + int(input(Fore.GREEN + 'Введите кол-во дней:')) * 86400
except:
    print(Fore.RED + 'Некорректное кол-во дней')
    input(Fore.BLUE + 'Press any key...')
    exit()
excel_data = list()
all_league_block = list()
main_driver = MainDriver()
try:
    main_driver.open_page(PARSER_URL)
    football_menu = main_driver.find_element(MENU_CLICK_XPATH)
    main_driver.click(football_menu)
    countries = main_driver.find_elements(COUNTRY_CLICK_XPATH)
    for country in tqdm(countries, desc='Собираем все возможные лиги по странам'):
        main_driver.scroll_into_view(country)
        main_driver.click(country)
        count = 0
        while True:
            league_blocks = main_driver.find_elements(LEAGUE_BLOCK_XPATH)
            if len(league_blocks) == count:
                for i in range(5):
                    main_driver.scroll_into_view(league_blocks[-1])
                    time.sleep(0.5)
                    league_blocks = main_driver.find_elements(LEAGUE_BLOCK_XPATH)
                    if len(league_blocks) != count:
                        continue
                break
            else:
                count = len(league_blocks)
                main_driver.scroll_into_view(league_blocks[-1])
        all_league_block.extend(list(map(lambda league: (league.get_attribute('innerHTML'), int(datetime.datetime.now().timestamp())), league_blocks)))
finally:
    main_driver.close()

for league_block in tqdm(all_league_block, desc='Собираем все возможные матчи по лигам'):
    bs = BeautifulSoup(league_block[0], 'lxml')
    league_name = bs.find('span', class_=LEAGUE_NAME_CLASS).text
    if league_name is None:
        print(Fore.RED + "Ошибка получения лиги(#2)")
        continue
    matches = bs.find_all(MATCHES_BLOCK_CLASS)
    for match in matches:
        try:
            is_live = match.find('svg-icon', attrs={"src": "/assets/shared/svg/icon-live.svg"}) is not None
            if is_live:
                continue

            data = {
                'date': date_validator(league_block[1], match.find('div', class_='header-left__time ng-star-inserted').text.strip()),
                'team_name_1': match.find_all('div', class_='name ng-star-inserted')[0].text.strip(),
                'team_name_2': match.find_all('div', class_='name ng-star-inserted')[1].text.strip(),
                'league_name': league_name.strip(),
            }
            card_body = match.find('div', class_='card__body')
            try:
                data['match_outcome_1'] = card_body.find_all('ww-feature-event-market-dsk')[0].find_all('div', class_='coefficient-button')[0].find('span').text.strip()
            except:
                data['match_outcome_1'] = '-'
            try:

                data['match_outcome_x'] = card_body.find_all('ww-feature-event-market-dsk')[0].find_all('div', class_='coefficient-button')[1].find('span').text.strip()
            except:
                data['match_outcome_x'] = '-'

            try:
                data['match_outcome_2'] = card_body.find_all('ww-feature-event-market-dsk')[0].find_all('div', class_='coefficient-button')[2].find('span').text.strip()
            except:
                data['match_outcome_2'] = '-'

            try:
                data['match_total_m'] = card_body.find_all('ww-feature-event-market-dsk')[2].find_all('div', class_='coefficient-button')[0].find('span').text.strip()
            except:
                data['match_total_m'] = '-'

            try:
                data['match_total_coefficient'] = card_body.find_all('ww-feature-event-market-dsk')[2].find('div', class_='coefficient-middle').find('span').text.replace('-', '').replace('+', '').strip()
            except:
                data['match_total_coefficient'] = '-'

            try:
                data['match_total_b'] = card_body.find_all('ww-feature-event-market-dsk')[2].find_all('div', class_='coefficient-button')[1].find('span').text.strip()
            except:
                data['match_total_b'] = '-'

            excel_data.append(FootballRow.model_validate(data))
        except:
            print(Fore.RED + "Ошибка получения матча")

workbook = xlsxwriter.Workbook(uuid.uuid4().hex + '.xlsx')
worksheet = workbook.add_worksheet()
base_format = workbook.add_format()
base_format.set_align('center')
base_format.set_align('vcenter')
worksheet.write_row(1, 0, EXCEL_HEADERS, base_format)
worksheet.merge_range(0, 0, 0, 7, '')
worksheet.merge_range(0, 8, 0, 10, 'Тотал', base_format)
worksheet.merge_range(0, 11, 0, 13, 'Исход', base_format)
worksheet.merge_range(0, 14, 0, 16, 'Тотал', base_format)

for row, col in tqdm(enumerate(list(filter(lambda x: x.date <= days_timestamp, excel_data))), desc='Записываем данные в файл'):
    data = [
        datetime.datetime.fromtimestamp(col.date).strftime('%d'),
        datetime.datetime.fromtimestamp(col.date).strftime('%m'),
        datetime.datetime.fromtimestamp(col.date).strftime('%Y'),
        datetime.datetime.fromtimestamp(col.date).strftime('%H:%M'),
        col.team_name_1,
        col.team_name_2,
        col.bookmaker_company_name,
        col.league_name,
        col.match_total_coefficient,
        col.match_total_m,
        col.match_total_b,
        col.match_outcome_1,
        col.match_outcome_x,
        col.match_outcome_2,
        col.match_total_coefficient,
        col.match_total_m,
        col.match_total_b,
    ]
    worksheet.write_row(row + 2, 0, data, base_format)
worksheet.autofit()
workbook.close()
print(Fore.GREEN + 'Готово')
print(Fore.GREEN + f'Результат сохранен в файле: {workbook.filename}')
input(Fore.BLUE + 'Press any key...')
exit()

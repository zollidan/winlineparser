import datetime

from selenium.webdriver.common.by import By

BASE_URL = 'https://www.marathonbet.ru/su/?cppcids=all'
PARSER_URL = 'https://www.marathonbet.ru/su/betting/Football+-+11?interval=H24'

DEBUG_MODE = False

BOTTOM_SIGN = "//div[contains(text(),'2024 ООО «Букмекерская контора «Марафон»')]"
BG_COUPON_ROW = "//div[@class='bg coupon-row']"
CATEGORY_CONTAINER = "//div[@class='category-container']"
COUNTRY_CLICK_XPATH = '//a[contains(@class, "countries-list__item-link")]'
LEAGUE_BLOCK_XPATH = '//div[@class="block-sport__champ-item ng-star-inserted"]'
ITERATIONS_TO_BOTTOM = 35

VERSION = '0.5.5'

LEAGUE_NAME_CLASS = 'block-tournament-header__title'
MATCHES_BLOCK_CLASS = 'ww-feature-block-event-dsk'

EXCEL_HEADERS = [
    "День",
    "Месяц",
    "Год",
    "Время",
    "Команда 1",
    "Команда 2",
    "Букмекерская компания",
    "Лига",
    "Коэффициент",
    "M",
    "B",
    "1",
    "Коэффициент",
    "2",
    "Коэффициент",
    "M",
    "B",

]


def change_month(month):
    if month == "янв": return "01"
    if month == "фев": return "02"
    if month == "мар": return "03"
    if month == "апр": return "03"
    if month == "май": return "05"
    if month == "июн": return "06"
    if month == "июл": return "07"
    if month == "авг": return "08"
    if month == "сен": return "09"
    if month == "окт": return "10"
    if month == "ноя": return "11"
    if month == "дек": return "12"


def change_date(class_date):
    if len(class_date.split()) == 1:
        day = datetime.date.today().strftime("%d")
        month = datetime.date.today().strftime("%m")
        year = datetime.date.today().strftime("%Y")
        time = class_date.split()[0]
        return day, month, year, time
    elif len(class_date.split()) == 3:
        day = class_date.split()[0]
        month = change_month(class_date.split()[1])
        year = datetime.date.today().strftime("%Y")
        time = class_date.split()[2]
        return day, month, year, time


def games_counter(main_driver):
    games = main_driver.find_elements(BG_COUPON_ROW)

    games_list = []

    for game in games:
        games_list.append(game)
    return games_list


def get_new_prices(one_game, main_driver):
    game_href = one_game.find_elements(By.CLASS_NAME, 'member-link')[0]
    main_driver.click(game_href)
    link_array = str(main_driver.current_url()).split("+")
    uniq_game_code = link_array[-1]
    total_class_id = 'shortcutLink_event' + uniq_game_code + 'type3'
    if DEBUG_MODE:
        print(f"динамический айдишник: {total_class_id}")
    totals_btn = main_driver.find_element(f"//td[@id='{total_class_id}']")
    main_driver.click(totals_btn)

    main_table = main_driver.find_elements(
        "//body[1]/div[6]/div[1]/div[3]/div[1]/div[1]/div[3]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[3]/div[1]/div[1]/div[1]/table[2]/tbody[1]/tr")
    """
    сделал поиск всех коффи из таблицы, потом сделать все списком убрать больше меньше и вернуть новые коффи, спасибо)))

    """
    prices = []
    for price in main_table:
        prices.append(price.text)
    prices.remove('Меньше Больше')
    new_coffi8 = prices[2].replace('\n', ' ').split()[1]
    new_coffi9 = prices[2].replace('\n', ' ').split()[3]

    return new_coffi8, new_coffi9


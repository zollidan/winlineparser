import datetime

BASE_URL = 'https://www.marathonbet.ru/su/?cppcids=all'
PARSER_URL = 'https://www.marathonbet.ru/su/betting/Football+-+11?interval=H24'

DEBUG_MODE = False

BOTTOM_SIGN = "//div[contains(text(),'2024 ООО «Букмекерская контора «Марафон»')]"
BG_COUPON_ROW = "//div[@class='bg coupon-row']"
CATEGORY_CONTAINER = "//div[@class='category-container']"
COUNTRY_CLICK_XPATH = '//a[contains(@class, "countries-list__item-link")]'
LEAGUE_BLOCK_XPATH = '//div[@class="block-sport__champ-item ng-star-inserted"]'
ITERATIONS_TO_BOTTOM = 10

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

BASE_URL = 'https://www.marathonbet.ru/su/?cppcids=all'
PARSER_URL = 'https://www.marathonbet.ru/su/betting/Football+-+11'

MENU_CLICK_XPATH = '//a[contains(@class, "sport-menu__list-item__link")]'
COUNTRY_CLICK_XPATH = '//a[contains(@class, "countries-list__item-link")]'
LEAGUE_BLOCK_XPATH = '//div[@class="block-sport__champ-item ng-star-inserted"]'

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
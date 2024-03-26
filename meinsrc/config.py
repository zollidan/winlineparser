BASE_URL = 'https://www.marathonbet.ru/su/?cppcids=all'
PARSER_URL = 'https://www.marathonbet.ru/su/betting/Football+-+11?interval=H24'

BOTTOM_SIGN = "//div[contains(text(),'2024 ООО «Букмекерская контора «Марафон»')]"
COUPON_ROW_ITEM = "//table[@class='coupon-row-item']"
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
import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get('https://www.marathonbet.ru/su/betting/Football/Russia/Cup/Regions+Path/Quarter+Final/Stage+2/SKA-Khabarovsk+vs+Dynamo+Moscow+-+18235855')

link_array = str(driver.current_url).split("+")
uniq_game_code = link_array[-1]
total_class_id = 'shortcutLink_event' + uniq_game_code + 'type3'
totals_btn = driver.find_element(By.XPATH , f"//td[@id='{total_class_id}']")
totals_btn.click()

main_table = driver.find_elements(By.XPATH,
    "//body[1]/div[6]/div[1]/div[3]/div[1]/div[1]/div[3]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[3]/div[1]/div[1]/div[1]/table[2]/tbody[1]/tr")

prices = []
for price in main_table:
    price = price.text.replace('\n', ' ')
    if '(2.5)' in price:
        price_spitted = price.split()
        prices.append(price_spitted[1])
        prices.append(price_spitted[3])
print(prices)

new_coffi8 = prices[0]
new_coffi9 = prices[1]


driver.close()

import time

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


options = Options()

options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])


driver = webdriver.Chrome(options=options)

driver.get("https://www.marathonbet.ru/su/betting/Football+-+11?interval=H24")

SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = driver.execute_script("document.querySelector('.grid-middle').scrollHeight;")

time.sleep(5)

driver.quit()



from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


options = Options()

options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

driver.get("http://selenium.dev")

print(driver.get("http://selenium.dev"))

driver.quit()



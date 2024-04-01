import time
import pathlib

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()

# options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

driver.get(str(pathlib.Path().absolute()) + '\page.html')

time.sleep(10)

driver.quit()

import logging
import pathlib
import time
import typing
from colorama import Fore
from selenium import webdriver
from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import chromedriver_autoinstaller
class MainDriver:
    @staticmethod
    def init_driver() -> WebDriver:
        chromedriver_autoinstaller.install()

        try:
            options = Options()
            # options.add_argument("--headless")
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


main_driver = MainDriver()

for i in range(10):
    main_driver.open_page('https://www.youtube.com/')

    time.sleep(2)

main_driver.quit()
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



print(Fore.GREEN + 'собираю дату жестко... за все время жестко...')

excel_data = list()
all_league_block = list()
#main_driver = MainDriver()

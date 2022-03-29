import os
import csv
import time
import random

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from fake_useragent import UserAgent

## Firefox driver
# from selenium.webdriver import Firefox as Browser
# from selenium.webdriver.firefox.options import Options
# from webdriver_manager.firefox import GeckoDriverManager as DriverManager

## Chrome driver
from selenium.webdriver import Chrome as Browser
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager as DriverManager

class Scraper:
    def __init__(self):
        self.data = []

        ua = UserAgent()
        userAgent = ua.random
        print("\nUser agent:\n" + userAgent + "\n")

        options = Options()
        options.add_argument(f'user-agent = {userAgent}')
        options.add_argument("start-maximized")
        options.add_argument("disable-gpu")
        options.add_argument("no-default-browser-check")
        options.add_argument("no-first-run")
        options.add_argument("no-sandbox")

        self.driver = Browser(executable_path = DriverManager().install(), options = options)

        #viewportList = [1920, 1080, 520, 1300, 650, 320]
        #self.driver.set_window_size(random.choice(viewportList), random.choice(viewportList))

    def getContent(self, link, mainID, buttonText, pages=-1):
        self.driver.get(link)

        data = []
        self.downloading = True
        while(self.downloading):
            time.sleep(random.randint(1, 3))

            try:
                myElem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, mainID)))
                print("Page loaded")

                self._accept_cookies()
                self._extract_rents()

                # This variable stop the loop in the first page:
                self.downloading = False
                print("New page")
                self.changePage(buttonText)
            except TimeoutException:
                print("Too much time ...")

        self.getItemData()
        self.listDict2csv()

    def changePage(self, buttonText):
        if self.downloading:
            time.sleep(random.randint(1, 3))
            self.driver.get(self.nextLink)

    def listDict2csv(self):
        path = './data'

        isExist = os.path.exists(path)
        if not isExist:
          os.makedirs(path)

        keys = self.data[0].keys()

        with open('./data/rent_prices.csv', 'w', newline = '') as outputFile:
            dictWriter = csv.DictWriter(outputFile, keys)
            dictWriter.writeheader()
            dictWriter.writerows(self.data)

    def stop(self):
        self.driver.close()

    def _accept_cookies(self):
        pass

    def getItemData(self):
        pass

    def getNextPage(self):
        pass

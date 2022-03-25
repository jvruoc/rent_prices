import time
import random

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
            try:
                myElem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, mainID)))
                print("Page loaded")

                self._accept_cookies()
                data = self._extract_rents()

                # self.changePage(buttonText)
            except TimeoutException:
                print("Too much time ...")

        return data

    def changePage(self, buttonText):
        nextLink = self.driver.find_element_by_partial_link_text(buttonText)

        if(nextLink):
            time.sleep(random.randint(1, 3))
            self.driver.execute_script("arguments[0].click();", nextLink)
        else:
            self.downloading = False

    def stop(self):
        self.driver.close()

    def _accept_cookies(self):
        pass

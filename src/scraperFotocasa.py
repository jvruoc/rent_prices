import random

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from fake_useragent import UserAgent

## Firefox driver
# from selenium.webdriver import Firefox as Browser
# from selenium.webdriver.firefox.options import Options
# from webdriver_manager.firefox import GeckoDriverManager as DriverManager

## Chrome driver
from selenium.webdriver import Chrome as Browser
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager as DriverManager

class ScraperFotocasa():

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

    def getContent(self, link, pages=-1):
        self.driver.get(link)

        data = []
        while(True):
            try:
                myElem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'App')))
                self._accept_cookies()
                data = self._extract_rents()
                break
            except TimeoutException:
                print("Too much time ...")

        return data

    def _extract_rents(self):
        items = self.driver.find_elements(by=By.XPATH, value='//article[starts-with(@class, "re-CardPack")]' )
        data=[]
        for item in items:
            rent = dict()
            rent['title'] = item.find_element(by=By.XPATH, value="./a").get_attribute("title")
            rent['link'] = item.find_element(by=By.XPATH, value="./a").get_attribute("href")
            rent['precio'] = item.find_element(by=By.XPATH, value=".//span[@class='re-CardPrice']").text
            rent['periodicidad'] = item.find_element(by=By.XPATH, value=".//span[@class='re-CardPricePeriodicity']").text
            features = []
            for f in item.find_elements(by=By.XPATH, value=".//li[@class='re-CardFeatures-feature']"):
                features.append(f.text)
            rent['feaures'] = features
            data.append(rent)
        return data

    def _accept_cookies(self):
        buttons = self.driver.find_elements(by=By.XPATH, value="//footer[contains(@class,'Modal')]//button")
        if buttons:
            #Pulsa aceptar cookies
            buttons[1].click()

    def printList(self, list):
        for item in list:
            print('\n' + item.text + '\n')

    def stop(self):
        self.driver.close()

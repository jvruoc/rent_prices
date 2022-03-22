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

class ScraperIdealista():

    def __init__(self):
        ua = UserAgent()
        userAgent = ua.random
        print("\nUser agent:\n" + userAgent + "\n")

        options = Options()
        options.add_argument(f'user-agent = {userAgent}')

        self.driver = Browser(executable_path = DriverManager().install(), options = options)

        viewportList = [1920, 1080, 520, 1300, 650, 320]
        self.driver.set_window_size(random.choice(viewportList), random.choice(viewportList))

    def getContent(self, link):
        self.driver.get(link)

        while(True):
            try:
                myElem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'main-content')))
                print("Page loaded")

                list = self.driver.find_elements(By.XPATH, '//article[@class="item  item_contains_branding item-multimedia-container"]')
                self.printList(list)

                nextLink = self.driver.find_element_by_partial_link_text("Next")

                if(nextLink):
                    break
                    time.sleep(random.randint(1,3))
                    self.driver.execute_script("arguments[0].click();", nextLink)
                else:
                    break

            except TimeoutException:
                print("Too much time ...")

        
    def printList(self, list):
        for item in list:
            print('\n' + item.text + '\n')

    def stop(self):
        self.driver.close()
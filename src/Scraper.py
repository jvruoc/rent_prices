import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from fake_useragent import UserAgent

from webdriver_manager.chrome import ChromeDriverManager

class IdSeleniumScraper():

    def __init__(self):
        ua = UserAgent()
        userAgent = ua.random
        print("\nUser agent:\n" + userAgent + "\n")

        options = Options()
        options.add_argument(f'user-agent = {userAgent}')

        self.driver = webdriver.Chrome(executable_path = ChromeDriverManager().install(), chrome_options = options)

        viewportList = [1920, 1080, 520, 1300, 650, 320]
        self.driver.set_window_size(random.choice(viewportList), random.choice(viewportList))

    def connect(self, link):
        self.driver.get(link)

    def stop(self):
        self.driver.close()

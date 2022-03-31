from abc import ABC, abstractmethod
from fake_useragent import UserAgent
import urllib3
import backoff
import sys
import os
import json
import time
import random

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

## Firefox driver
# from selenium.webdriver import Firefox as Browser
# from selenium.webdriver.firefox.options import Options
# from webdriver_manager.firefox import GeckoDriverManager as DriverManager

## Chrome driver
from selenium.webdriver import Chrome as Browser
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager as DriverManager

## Remote chrome driver
from selenium.webdriver import Remote

from utilities.proxyManager import ProxiManager
from logger.logger import logger


class Scraper(ABC):
    """
        Clase base para todos los scraper que construyamos. Incluye:
        - Conexión con un logger para toda la app
        - Definición del driver remoto para selenium (preparado para docker)
        - Método de inicialización de la clase

        Los scraper que se construyan a partir de esta clase tienen que
        implementar el método getContent() que está definido como abstracto
        en esta clase
    """

    def __init__(self, proxi_manager=None):

        ua = UserAgent()
        userAgent = ua.random
        logger.debug("*************************************")
        logger.debug("\nUser agent:\n" + userAgent + "\n")
        self._set_driver(userAgent)

    def _set_driver(self, userAgent):

        SELENIUM_URL = "selenium:4444"

        in_docker = os.getenv("IN_DOCKER") == "yes"
        logger.info (f"ENV IN_DOKER: {in_docker}")
        if in_docker:
            # Si no logra conectar con la instancia de Selenium finaliza la app.
            try:
                self.driver = self._selenium_remote_connect(f"http://{SELENIUM_URL}/wd/hub")
            except urllib3.exceptions.MaxRetryError:
                logger.error("Unable to connect to Selenium.")
                sys.exit(1)
        else:
            options = Options()
            options.add_argument(f'user-agent = {userAgent}')
            options.add_argument("start-maximized")
            options.add_argument("disable-gpu")
            options.add_argument("no-default-browser-check")
            options.add_argument("no-first-run")
            options.add_argument("no-sandbox")
            options.add_argument("headless")
            self.driver = Browser(executable_path = DriverManager().install(), options = options)

    @backoff.on_exception(
        backoff.expo,
        urllib3.exceptions.MaxRetryError,
        max_tries=5,
        jitter=None
    )
    def _selenium_remote_connect(self, url, capabilities={'browserName': 'chrome'} ):
        return Remote(url, capabilities)

    def getContent(self, link, mainID):
        self.link = link
        self.driver.get(link)

        data = []
        self.downloading = True
        while(self.downloading):
            time.sleep(random.randint(1, 3))

            try:
                myElem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, mainID)))
                print("Page loaded")

                self._accept_cookies()
                data = self._extract_rents()

                for item in data:
                    yield item

                # This variable stop the loop in the first page:
                # self.downloading = False
                self.changePage()
            except TimeoutException:
                print("Too much time ...")

        # self.listDict2csv(data)

    def end_scraping(self):
        self.driver.quit()

    def changePage(self):
        if self.downloading:
            print("\n\nNew page:")
            print(self.nextLink)
            time.sleep(random.randint(1, 3))
            self.driver.get(self.nextLink)

    def listDict2csv(self, data):
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

    @abstractmethod
    def _accept_cookies(self):
        pass

    @abstractmethod
    def getNextPage(self):
        pass

from abc import ABC, abstractmethod
import csv
from datetime import datetime
from fake_useragent import UserAgent
import urllib3
import backoff
import sys
import os
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
from utilities.configuration import config


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
            options.add_argument("--headless")
            options.add_argument("disable-gpu")
            options.add_argument("no-default-browser-check")
            options.add_argument("no-first-run")
            options.add_argument("no-sandbox")
            self.driver = Browser(executable_path = DriverManager().install(), options = options)
            # Es el tamaño de la ventana que abre el webdriver en remoto
            # Lo igualamos para que el renderizado de la página sea igual
            self.driver.set_window_size(1050, 882)


    @backoff.on_exception(
        backoff.expo,
        urllib3.exceptions.MaxRetryError,
        max_tries=5,
        jitter=None
    )
    def _selenium_remote_connect(self, url, capabilities={'browserName': 'chrome'} ):
        return Remote(url, capabilities)

    def getContent(self, link, mainID):
        #self.driver.get(link)
        self.get_link(link)

        data = []
        self.downloading = True
        while(self.downloading):
            time.sleep(random.randint(1, 3))

            try:
                myElem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, mainID)))
                print("Page loaded")

                self._accept_cookies()
                data = self._extract_rents()

                for item in self.getItemData(data):
                    yield item

                # This variable stop the loop in the first page:
                self.downloading = False
                print("New page")
                self.changePage()
            except TimeoutException:
                print("Too much time ...")

        # self.listDict2csv(data)

    def end_scraping(self):
        self.driver.quit()

    def changePage(self):
        if self.downloading:
            time.sleep(random.randint(1, 3))
            #self.driver.get(self.nextLink)
            self.get_link(self.nextLink)

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

    def get_link(self, link):
        logger.info(f"descarga de link: {link}")
        self.driver.get(link)
        date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        if config.store_html or config.store_screenshot:
            path_file="./html"
            if 'PATH_TO_HTML' in os.environ:
                path_file = os.environ['PATH_TO_HTML']
            file_name = os.path.join(path_file, date_time)

            if not os.path.exists(path_file):
                os.makedirs(path_file)

            if config.store_html:
                with open(file_name + ".html", "w") as f:
                    f.write(self.driver.page_source)
                logger.info(f"html en : {file_name+'.html'}")

            if config.store_screenshot:
                self.driver.save_screenshot(file_name + ".png")
                logger.info(f"html en : {file_name+'.png'}")




    @abstractmethod
    def _accept_cookies(self):
        pass

    @abstractmethod
    def getItemData(self):
        pass

    @abstractmethod
    def getNextPage(self):
        pass

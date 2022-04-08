from abc import ABC, abstractmethod
import csv
from datetime import datetime
from fake_useragent import UserAgent
import urllib3
import backoff
import sys
import os
import re
import json
import time
import random
import requests
import shutil

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

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

        if config.output_images:
            gauth = GoogleAuth()
            self.gdrive = GoogleDrive(gauth)

    def _set_driver(self, userAgent):

        SELENIUM_URL = "selenium:4444"

        in_docker = os.getenv("IN_DOCKER") == "yes"
        logger.info (f"ENV IN_DOKER: {in_docker}")
        options = Options()
        options.add_argument(f'user-agent = {userAgent}')
        options.add_argument("disable-gpu")
        options.add_argument("no-default-browser-check")
        options.add_argument("no-first-run")
        options.add_argument("no-sandbox")
        options.add_argument("headless")

        if in_docker:
            # Si no logra conectar con la instancia de Selenium finaliza la app.
            try:
                self.driver = self._selenium_remote_connect(f"http://{SELENIUM_URL}/wd/hub", capabilities=options.to_capabilities())
            except urllib3.exceptions.MaxRetryError:
                logger.error("Unable to connect to Selenium.")
                sys.exit(1)
        else:
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

        self.link = link
        #self.driver.get(link)
        self.get_link(link)

        data = []
        self.downloading = True
        while(self.downloading):
            #time.sleep(random.randint(1, 3))

            try:
                myElem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, mainID)))
                logger.info("Page loaded")

                self._accept_cookies()
                data = self._extract_rents()

                for item in data:
                    yield item

                # This variable stop the loop in the first page:
                # self.downloading = False
                self.changePage()
            except TimeoutException:
                logger.info("Too much time ...")

        # self.listDict2csv(data)

    def end_scraping(self):
        self.driver.quit()

    def changePage(self):
        if self.downloading:
            logger.debug(self.nextLink)
            #time.sleep(random.randint(1, 3))
            #self.driver.get(self.nextLink)
            self.get_link(self.nextLink)

    def downloadImage(self, itemID, link):
        filename = re.sub('\.jpg.*', '.jpg', link.split("/")[-1])

        if not os.path.exists('./images/'):
            os.makedirs('./images/')

        r = requests.get(link, stream = True)

        if r.status_code == 200:
            r.raw.decode_content = True

            filename = str(itemID) + '-' + filename

            imagePath = './images/' + filename

            with open(imagePath, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

            logger.debug('Image downloaded: ' + filename)

            self.uploadFile(filename)

            os.remove(imagePath)
            logger.debug('Image deleted: ' + filename)
        else:
            logger.debug('Image couldn\'t be retreived')

    def uploadFile(self, filename):
        gfile = self.gdrive.CreateFile({'parents': [{'id': config.output_images}], 'title' : filename})

        logger.debug('Image uploaded: ' + filename)

        gfile.SetContentFile('./images/' + filename)
        gfile.Upload()

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
        random_time = random.randint(8, 12)
        logger.info(f"Retardo ({random_time} s.) -> descarga de link: {link}")
        time.sleep(random_time)
        try:
            self.driver.get(link)
        except Exception as e:
            logger.error(f"Error al descargar el link: {link}")
            raise e
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
    def _extract_rents(self):
        pass

    @abstractmethod
    def getNextPage(self):
        pass

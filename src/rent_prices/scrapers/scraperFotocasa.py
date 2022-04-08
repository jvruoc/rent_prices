from .scraper import Scraper
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from logger.logger import logger
from utilities.configuration import config
import json
import time


class ScraperFotocasa(Scraper):



    class script_whit_initial_props (object):
        """
            Esta clase espera a que exista un script
            que contenga la variable javascript __INITIAL_PROPS__
            y la extrae.

            Se utiliza junto con la función wait para esperar
            a que el contenido del script esté disponible.
        """

        def __init__(self, locator, var):
            self.locator = locator
            self.var = var

        def __call__(self, driver):
            elements = driver.find_elements(*self.locator)
            for element in elements:
                try:
                    html = element.get_attribute('innerHTML')
                    if html.find(self.var) > 0:
                        return element
                except:
                    return False




    def __init__(self, newPage = -1, maxPages = -1):
        Scraper.__init__(self)

        self.newPage = newPage
        self.maxPages = maxPages

    def _extract_rents(self):

        # Espera hasta 10 segundo para que esté disponible la información en la página
        wait = WebDriverWait(self.driver, 10)
        scriptElem = wait.until(self.script_whit_initial_props((By.XPATH, '//script'), 'window.__INITIAL_PROPS__'))
        splitScriptElem = scriptElem.get_attribute('innerHTML').split("window.")

        items = (splitScriptElem[2].replace('__INITIAL_PROPS__ = JSON.parse("', '')
            .replace('");', '')
        )
        items = items.encode("utf-8").decode("unicode_escape")
        items = json.loads(items)["initialSearch"]["result"]["realEstates"]

        # incluye el historial de precios y la última fecha de actualización
        logger.info(f"Cantidad de inmuebles en la página: {len(items)}")

        for item in items:
            yield self.getCardData(item)

        self.scrollDown()


    def _accept_cookies(self):
        buttons = self.driver.find_elements(by=By.XPATH, value="//footer[contains(@class,'Modal')]//button")
        if buttons:
            #Pulsa aceptar cookies
            buttons[1].click()

    def scrollDown(self):
        # articles = self.driver.find_elements(by=By.XPATH, value='//article')
        # nArticles = len(articles)
        # logger.debug("Cantidad de articulos: " + str(nArticles))

        # newNArticles = 100

        # while True:
        #     actions = ActionChains(self.driver)
        #     actions.move_to_element(articles[-1]).perform()

        #     articles = self.driver.find_elements(by=By.XPATH, value='//article')
        #     newNArticles = len(articles)

        #     if (newNArticles > nArticles):
        #         nArticles = newNArticles
        #     else:
        #         break
        
        # Para que de tiempo a que carge toda la página
        # time.sleep(5)
        # Como tenemos un wait que espera hasta que el script esté dispo
        self.driver.execute_script("var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;")
        logger.info("Finished scroll")

        self.getNextPage()


    def getNextPageHTML(self):
        try:
            #Solo lo necesita el get de la página
            #time.sleep(random.randint(5, 10))

            pageLinks = self.driver.find_elements_by_class_name('sui-MoleculePagination-item')
            self.nextLink = pageLinks[-1].find_element(by=By.XPATH, value="./a").get_attribute("href")

        except NoSuchElementException:
            self.downloading = False


    def getNextPage(self):
        if self.newPage < self.maxPages:
            self.nextLink = self.link + '/' + str(self.newPage)
            self.newPage = self.newPage  + 1
        else:
            self.downloading = False

    def getCardData(self, item):
        newDataItem = dict()

        newDataItem['zipCode'] = item['address']['zipCode']
        newDataItem['buildingSubtype'] = item['buildingSubtype']
        newDataItem['buildingType'] = item['buildingType']
        newDataItem['clientAlias'] = item['clientAlias']
        newDataItem['clientId'] = item['clientId']
        newDataItem['clientTypeId'] = item['clientTypeId']
        newDataItem['dateDiff'] = item['date']['diff']
        newDataItem['dateUnit'] = item['date']['unit']
        newDataItem['dateOriginalDiff'] = item['dateOriginal']['diff']
        newDataItem['dateOriginalUnit'] = item['dateOriginal']['unit']
        newDataItem['dateOriginalTimestamp'] = item['dateOriginal']['timestamp']

        # En algunas descripciones vienen caracteres no válidos para utf-8.
        # Si no se eliminan al grabar en MongoDB generan error
        # También se verifica que sea de la clase str para poder aplicar el encode
        if isinstance(item['description'], str):
            newDataItem['description'] = item['description'].encode('utf-8',errors="replace").decode("utf-8")
        else:
            newDataItem['description'] = item['description']
        

        for feature in item['features']:
            newDataItem[feature['key']] = feature['value']

        newDataItem['_id'] = f"fc-{item['id']}"
        newDataItem['isDiscarded'] = item['isDiscarded']
        newDataItem['isHighlighted'] = item['isHighlighted']
        newDataItem['isPackAdvancePriority'] = item['isPackAdvancePriority']
        newDataItem['isPackBasicPriority'] = item['isPackBasicPriority']
        newDataItem['isPackMinimalPriority'] = item['isPackMinimalPriority']
        newDataItem['isPackPremiumPriority'] = item['isPackPremiumPriority']
        newDataItem['isMsAdvance'] = item['isMsAdvance']
        newDataItem['isNew'] = item['isNew']
        newDataItem['isNewConstruction'] = item['isNewConstruction']
        newDataItem['hasOpenHouse'] = item['hasOpenHouse']
        newDataItem['isOpportunity'] = item['isOpportunity']
        newDataItem['isTrackedPhone'] = item['isTrackedPhone']
        newDataItem['isTop'] = item['isTop']
        newDataItem['minPrice'] = item['minPrice']

        newDataItem['multimedia'] = list()
        for multElem in item['multimedia']:
            multimedia = dict()
            multimedia['type'] = multElem['type']
            multimedia['src'] = multElem['src']

            if config.output_images:
                self.downloadImage(newDataItem['_id'], multimedia['src'])

            newDataItem['multimedia'].append(multimedia)

        newDataItem['otherFeaturesCount'] = item['otherFeaturesCount']
        newDataItem['periodicityId'] = item['periodicityId']
        newDataItem['price'] = item['rawPrice']
        newDataItem['promotionId'] = item['promotionId']
        newDataItem['promotionUrl'] = item['promotionUrl']
        newDataItem['promotionTitle'] = item['promotionTitle']
        newDataItem['promotionTypologiesCounter'] = item['promotionTypologiesCounter']
        newDataItem['realEstateAdId'] = item['realEstateAdId']
        newDataItem['reducedPrice'] = item['reducedPrice']
        newDataItem['subtypeId'] = item['subtypeId']
        newDataItem['transactionTypeId'] = item['transactionTypeId']
        newDataItem['typeId'] = item['typeId']

        return newDataItem

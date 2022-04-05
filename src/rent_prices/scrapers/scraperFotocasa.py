from .scraper import Scraper
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from logger.logger import logger
from utilities.configuration import config
import json


class ScraperFotocasa(Scraper):

    def __init__(self, newPage, maxPages):
        Scraper.__init__(self)

        self.newPage = newPage
        self.maxPages = maxPages

    def _extract_rents(self):
        self.scrollDown()

        # El sleep solo es necesario cuando se accede a la página (get)
        #time.sleep(random.randint(5, 10))

        scripts = self.driver.find_elements(by=By.XPATH, value='//script')

        for script in scripts:
            if script.get_attribute('innerHTML').find('window.__INITIAL_PROPS__') > 0:
                scriptElem = script
                break

        splitScriptElem = scriptElem.get_attribute('innerHTML').split("window.")

        items = (splitScriptElem[2].replace('__INITIAL_PROPS__ = JSON.parse("', '')
            .replace('");', '')
        )

        items = items.encode("utf-8").decode("unicode_escape")
        # items = re.sub('[a-zA-Z]*"', '', items)
        items = json.loads(items)["initialSearch"]["result"]["realEstates"]

        # incluye el historial de precios y la última fecha de actualización
        logger.info(f"Cantidad de inmuebles en la página: {len(items)}")

        for item in items:
            yield self.getCardData(item)

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
        #
        # logger.info("Finished scroll")


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
            newDataItem['multimedia'].append(multimedia)
            if config.output_images:
                #TODO Incluir descarga de imágenes
                pass

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



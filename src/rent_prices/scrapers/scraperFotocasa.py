from .scraper import *

from datetime import date

from selenium.webdriver.common.action_chains import ActionChains

class ScraperFotocasa(Scraper):

    def __init__(self, newPage, maxPages):
        Scraper.__init__(self)

        self.newPage = newPage
        self.maxPages = maxPages

    def _extract_rents(self):
        self.scrollDown()

        time.sleep(random.randint(5, 10))
        scripts = self.driver.find_elements(by=By.XPATH, value='//script')

        for script in scripts:
            if script.get_attribute('innerHTML').find('window.__INITIAL_PROPS__') > 0:
                scriptElem = script
                break

        splitScriptElem = scriptElem.get_attribute('innerHTML').split("window.")

        items = (splitScriptElem[2].replace('__INITIAL_PROPS__ = JSON.parse("', '')
            .replace('");', '')
            .replace('\\\\\\"', '')
            .replace('{\\"', '{\\\'')
            .replace('\\"}', '\\\'}')
            .replace('[\\"', '[\\\'')
            .replace('\\"]', '\\\']')
            .replace(',\\"', ',\\\'')
            .replace('\\":', '\\\':')
            .replace(':\\"', ':\\\'')
            .replace('\\",', '\\\',')
            .replace('"', '')
            .replace('\\\'', '"')
            .replace('\'', '')
            .replace('\\', ''))

        # items = re.sub('[a-zA-Z]*"', '', items)

        print(splitScriptElem[2])

        items = json.loads(items)

        for item in items["initialSearch"]["result"]["realEstates"]:
            yield self.getCardData(item)

    def _accept_cookies(self):
        buttons = self.driver.find_elements(by=By.XPATH, value="//footer[contains(@class,'Modal')]//button")
        if buttons:
            #Pulsa aceptar cookies
            buttons[1].click()

    def scrollDown(self):
        articles = self.driver.find_elements(by=By.XPATH, value='//article')
        nArticles = len(articles)

        newNArticles = 100

        while True:
            actions = ActionChains(self.driver)
            actions.move_to_element(articles[-1]).perform()

            articles = self.driver.find_elements(by=By.XPATH, value='//article')
            newNArticles = len(articles)

            if (newNArticles > nArticles):
                nArticles = newNArticles
            else:
                break

        self.getNextPage()

        print("Finished scroll")

    def getNextPageHTML(self):
        try:
            time.sleep(random.randint(5, 10))

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

        newDataItem['id'] = item['id']
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

        newDataItem['otherFeaturesCount'] = item['otherFeaturesCount']
        newDataItem['periodicityId'] = item['periodicityId']
        newDataItem['price'] = item['price']
        newDataItem['promotionId'] = item['promotionId']
        newDataItem['promotionUrl'] = item['promotionUrl']
        newDataItem['promotionTitle'] = item['promotionTitle']
        newDataItem['promotionTypologiesCounter'] = item['promotionTypologiesCounter']
        newDataItem['rawPrice'] = item['rawPrice']
        newDataItem['realEstateAdId'] = item['realEstateAdId']
        newDataItem['reducedPrice'] = item['reducedPrice']
        newDataItem['subtypeId'] = item['subtypeId']
        newDataItem['transactionTypeId'] = item['transactionTypeId']
        newDataItem['typeId'] = item['typeId']

        return newDataItem

from .scraper import *

from datetime import date

from selenium.webdriver.common.action_chains import ActionChains

class ScraperFotocasa(Scraper):
    def _extract_rents(self):
        self.scrollDown()

        data = []
        items = self.driver.find_elements(by=By.XPATH, value='//article[starts-with(@class, "re-CardPack")]')
        for item in items:
            rent = self.getCardData(item)

            data.append(rent)

        return data

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

    def getNextPage(self):
        try:
            pageLinks = self.driver.find_elements_by_class_name('sui-MoleculePagination-item')

            self.nextLink = pageLinks[-1].find_element(by=By.XPATH, value="./a").get_attribute("href")

        except NoSuchElementException:
            self.downloading = False

    def getCardData(self, item):
        rent = dict()

        # General
        today = date.today()
        rent['download-date'] = today.strftime("%d/%m/%Y")
        rent['Source'] = "Fotocasa"

        # Specific
        rent['title'] = item.find_element(by=By.XPATH, value="./a").get_attribute("title")
        rent['link'] = item.find_element(by=By.XPATH, value="./a").get_attribute("href")
        rent['precio'] = item.find_element(by=By.XPATH, value=".//span[@class='re-CardPrice']").text
        rent['periodicidad'] = item.find_element(by=By.XPATH, value=".//span[@class='re-CardPricePeriodicity']").text
        features = []
        for f in item.find_elements(by=By.XPATH, value=".//li[@class='re-CardFeatures-feature']"):
            features.append(f.text)
        rent['feaures'] = features

        return rent

    def getItemData(self, data):
        for item in data:

            self.driver.get(item['link'])

            featureLabels = self.driver.find_elements_by_class_name('re-DetailFeaturesList-featureLabel')
            featuresValues = self.driver.find_elements_by_class_name('re-DetailFeaturesList-featureValue')

            item['Antigüedad'] = ''
            item['Orientación'] = ''
            item['Mascotas'] = ''

            for index in range(len(featureLabels)):
                item[featureLabels[index].text] = featuresValues[index].text.replace('\n', '')

            extras = self.driver.find_elements_by_class_name('re-DetailExtras-listItem')

            if len(extras) > 0:
                actions = ActionChains(self.driver)
                actions.move_to_element(extras[-1]).perform()
                item['Address'] = self.driver.find_element_by_class_name('re-DetailMap-address').text

            strExtras = ''
            for extra in extras:
                strExtras += extra.text + ", "
            strExtras = strExtras[:len(strExtras)-2]

            item['extras'] = strExtras
            item['Contact'] = self.driver.find_element_by_class_name('re-ContactDetail-inmoContainer-clientName').text
            item['Ref'] = self.driver.find_element_by_class_name('re-ContactDetail-referenceContainer-reference').text
            item['RefFotocasa'] = self.driver.find_element_by_class_name('re-ContactDetail-referenceContainer-reference').text

            yield item

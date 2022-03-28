from scraper import *

from datetime import date

from selenium.webdriver.common.action_chains import ActionChains

class ScraperFotocasa(Scraper):
    def _extract_rents(self):
        self.scrollDown()

        items = self.driver.find_elements(by=By.XPATH, value='//article[starts-with(@class, "re-CardPack")]')
        for item in items:
            rent = self.getItemData(item)
            self.data.append(rent)

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

        '''
        element = self.driver.find_element_by_class_name('re-SearchRelated')
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        '''

        print("Finished scroll")

    def getItemData(self, item):
        rent = dict()

        # General
        today = date.today()
        rent['id'] = len(self.data) + 1
        rent['download-date'] = today.strftime("%d/%m/%Y")

        # Specific
        rent['title'] = item.find_element(by=By.XPATH, value="./a").get_attribute("title")
        rent['link'] = item.find_element(by=By.XPATH, value="./a").get_attribute("href")
        # rent['precio'] = item.find_element(by=By.XPATH, value=".//span[@class='re-CardPrice']").text
        # rent['periodicidad'] = item.find_element(by=By.XPATH, value=".//span[@class='re-CardPricePeriodicity']").text
        features = []
        for f in item.find_elements(by=By.XPATH, value=".//li[@class='re-CardFeatures-feature']"):
            features.append(f.text)
        rent['feaures'] = features

        return rent

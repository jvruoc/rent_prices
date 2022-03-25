from scraper import *

class ScraperFotocasa(Scraper):
    def _extract_rents(self):

        items = self.driver.find_elements(by=By.XPATH, value='//article[starts-with(@class, "re-CardPack")]' )
        data=[]
        for item in items:
            rent = dict()
            rent['title'] = item.find_element(by=By.XPATH, value="./a").get_attribute("title")
            rent['link'] = item.find_element(by=By.XPATH, value="./a").get_attribute("href")
            rent['precio'] = item.find_element(by=By.XPATH, value=".//span[@class='re-CardPrice']").text
            rent['periodicidad'] = item.find_element(by=By.XPATH, value=".//span[@class='re-CardPricePeriodicity']").text
            features = []
            for f in item.find_elements(by=By.XPATH, value=".//li[@class='re-CardFeatures-feature']"):
                features.append(f.text)
            rent['feaures'] = features
            data.append(rent)
        return data

    def _accept_cookies(self):
        buttons = self.driver.find_elements(by=By.XPATH, value="//footer[contains(@class,'Modal')]//button")
        if buttons:
            #Pulsa aceptar cookies
            buttons[1].click()

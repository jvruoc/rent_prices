from .scraper import *

class ScraperIdealista(Scraper):

    def _extract_rents(self):
        list = self.driver.find_elements(By.XPATH, '//article[@class="item  item_contains_branding item-multimedia-container"]')

        for item in list:
            print('\n' + item.text + '\n')

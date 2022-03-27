import random
from datetime import datetime
from .scraper import Scraper



class ScraperMock(Scraper):



    def getContent(self, link):

        num_pages = random.randint(2,4)
        for i in range(num_pages):
            for rent in self._extract_rents():
                yield rent

    def _extract_rents(self):
        num_links = random.randint(3,5)
        for item in range(num_links):
            rent = dict()
            rent['title'] = f"Título Aleatorio {item}"
            rent['link'] = f"http://test/id/{item}"
            rent['precio'] = random.randint(300,1000)
            rent['periodicidad'] = "Mes"
            features = ["Habitaciones", "Aire acondicionado"]
            rent['feaures'] = features
            rent['date'] = datetime.now()
            yield rent

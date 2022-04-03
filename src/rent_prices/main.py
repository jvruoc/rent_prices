import sys
from scrapers.scraperMock import ScraperMock
from scrapers.scraperIdealista import ScraperIdealista
from scrapers.scraperFotocasa import ScraperFotocasa
from logger.logger import logger

'''
url = 'https://www.idealista.com/en/alquiler-viviendas/madrid-madrid/'
scraper = ScraperIdealista()
scraper.getContent(url, 'main-content', 'Next')
'''

logger.info("Se inicia scraping")

url = "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/todas-las-zonas/l"
scraper = ScraperFotocasa(2, 192)
for item in scraper.getContent(url, 'App'):
    print(item)

scraper.end_scraping()
logger.info("Scraping finalizado")

sys.exit(1000)

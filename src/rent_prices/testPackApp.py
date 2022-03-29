import sys
from scrapers.scraperMock import ScraperMock
from logger.logger import logger

logger.info("Se inicia scraping")
scraper = ScraperMock()
for item in scraper.getContent("test"):
    print (item)

scraper.end_scraping()
logger.info("Scraping finalizado")

sys.exit(1000)


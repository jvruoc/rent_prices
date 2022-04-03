from distutils.command.config import config
import sys
import os
import argparse
from scrapers.scraperMock import ScraperMock
from scrapers.scraperIdealista import ScraperIdealista
from scrapers.scraperFotocasa import ScraperFotocasa
from logger.logger import logger
from utilities.configuration import config

'''
url = 'https://www.idealista.com/en/alquiler-viviendas/madrid-madrid/'
scraper = ScraperIdealista()
scraper.getContent(url, 'main-content', 'Next')
'''


def main():
    logger.info("Se inicia scraping")


    url = "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/todas-las-zonas/l"
    scraper = ScraperFotocasa()
    for item in scraper.getContent(url, 'App'):
        print(item)

    scraper.end_scraping()
    logger.info("Scraping finalizado")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--html', action='store_true', help='Guardar el html de la página')
    parser.add_argument('--screenshot', action='store_true', help='Guardar una captura de la página')
    args = parser.parse_args()

    if args.html:
        logger.info("Grabando html")
        config.store_html = True

    if args.screenshot:
        logger.info("Grabando screenshot")
        config.store_screenshot = True
    main()
    sys.exit(1000)

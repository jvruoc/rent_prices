from distutils.command.config import config
import sys
import os
import argparse
from scrapers.scraperMock import ScraperMock
from scrapers.scraperIdealista import ScraperIdealista
from scrapers.scraperFotocasa import ScraperFotocasa
from logger.logger import logger
from utilities.configuration import config
from utilities.database import Db

'''
url = 'https://www.idealista.com/en/alquiler-viviendas/madrid-madrid/'
scraper = ScraperIdealista()
scraper.getContent(url, 'main-content', 'Next')
'''


def main():
    logger.info("Se inicia scraping")

    Db.initialize('mongo-atlas.json')
    url = "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/todas-las-zonas/l"
    scraper = ScraperFotocasa(192, 194)
    for item in scraper.getContent(url, 'App'):
        logger.info(f"Grabando elemento id: {item['_id']}")
        if config.collection:
            Db.insert_or_update_price('rents', item['_id'], item)        

    scraper.end_scraping()
    logger.info("Scraping finalizado")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--html', action='store_true', help='Guardar el html de la página')
    parser.add_argument('--screenshot', action='store_true', help='Guardar una captura de la página')
    parser.add_argument('--collection', help='Graba en la colección mongo especificada')
    parser.add_argument('--output_images', help='Directorio para guardar las imágenes')
    args = parser.parse_args()

    if args.html:
        logger.info("Grabando html")
        config.store_html = True

    if args.screenshot:
        logger.info("Grabando screenshot")
        config.store_screenshot = True

    if args.collection:
        config.collection = args.collection
        logger.info("Los datos se gardan en la colección", config.collection)

    if args.output_images:
        config.output_images = args.output_images
        logger.info("Las imágenes se guardarán en ", config.output_images)
    main()
    sys.exit(1000)

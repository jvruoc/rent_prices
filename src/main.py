from Scraper import IdSeleniumScraper

url = 'https://www.idealista.com/en/alquiler-viviendas/madrid-madrid/'

scraper = IdSeleniumScraper()

scraper.getContent(url)

scraper.stop()

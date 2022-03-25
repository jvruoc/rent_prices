from scraperIdealista import ScraperIdealista
from scraperFotocasa import ScraperFotocasa

'''
url = 'https://www.idealista.com/en/alquiler-viviendas/madrid-madrid/'
scraper = ScraperIdealista()
scraper.getContent(url, 'main-content', 'Next')
'''

url = "https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/todas-las-zonas/l"
scraper = ScraperFotocasa()
data = scraper.getContent(url, 'App', '')
print(data)

scraper.stop()

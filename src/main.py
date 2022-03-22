from scraperIdealista import ScraperIdealista
from scraperFotocasa import ScraperFotocasa

url = 'https://www.idealista.com/en/alquiler-viviendas/madrid-madrid/'

#scraper = ScraperIdealista()
#scraper.getContent(url)
scraper = ScraperFotocasa()
data = scraper.getContent("https://www.fotocasa.es/es/alquiler/viviendas/madrid-capital/todas-las-zonas/l")
print(data)

scraper.stop()

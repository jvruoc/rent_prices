"""
    Genera fichero csv con el contenido de la colección `rents`
"""


import argparse
from logger.logger import logger
from scrapers.scraper import Scraper
from utilities.database import Db
import csv
from datetime import date



def main(file_name="rents.csv", limit=0, file_cat="categorical_values.txt"):

    logger.info(f"Inicio descarga en CSV")

    Db.initialize('mongo-atlas.json')

    cols = {"_id":0, "description":0, "multimedia":0}
    cursor = Db.find(collection='rents', query={}, projection=cols, limit=limit)

    cursor_cat = cursor.clone()

    Scraper.generate_file_categorical_vars(cursor_cat, file_cat)
    cursor = Db.find(collection='rents', query={}, projection=cols, limit=limit)
    lastIdCliente = 0
    clientes={}
    with open(file_name, "wt") as out:
        writer = csv.DictWriter(out, fieldnames=Scraper.get_col_names())
        writer.writeheader()
        for count, doc in enumerate(cursor,1):
            #Eliminamos del timestap la parte de la hora
            timestamp = doc.pop('dateOriginalTimestamp', None) // 1000 
            doc["dateOriginal"] = date.fromtimestamp(timestamp)
            doc["_id"] = count
            idCliente = clientes.get(doc["clientId"], None)
            if idCliente is None:
                idCliente = lastIdCliente + 1
                lastIdCliente = idCliente
                clientes[doc["clientId"]] = idCliente
            doc["clientId"] = f'id-{idCliente}'
            doc = Scraper.to_csv_dict(doc)
            writer.writerow(doc)

    logger.info(f"Se han escrito {count} registros en {file_name}")





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='madrid-rent-prices.csv', help='Path del fichero de salida')
    parser.add_argument('--categorical_values', default='categorical_values.txt', help='Path del fichero de información variables categoricas')
    parser.add_argument('--limit', type=int, default=0, help="Número de registros a extraer (0=Todos)")
    args = parser.parse_args()

    main(file_name=args.output, limit=args.limit, file_cat=args.categorical_values)

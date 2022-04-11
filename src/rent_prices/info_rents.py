"""
    Imprime información de los registros grabados en la colección rents
"""

import argparse
from logger.logger import logger
from utilities.database import Db



def main(file_name="rents.csv", limit=0, file_cat="categorical_values.txt"):

    Db.initialize('mongo-atlas.json')

    alquilados_por_fecha = [
        {"$group": {
            "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$lastAccess"}},
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]

    print("Anuncios por último acceso")
    print("=========================")
    for r in Db.agg('rents',alquilados_por_fecha):
        print (f"{r['_id']} - {r['count']}")

    historial_precios = [
        {"$group": {
            "_id": {"$size": "$history"},
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]

    total_regs = 0
    print("Anuncios con historial de precios")
    print("===================================")
    for r in Db.agg('rents',historial_precios):
        print (f"{r['_id']} - {r['count']}")
        total_regs += r['count']

    print()
    print(f"Total de registros: {total_regs}")


if __name__ == "__main__":
    logger.info(f"Queries información")
    main()
    logger.info(f"Fin queries información")

import pymongo
import json
import os
from logger.logger import logger

class Db ():
    """
    Clase que gestiona la conexión a la base de datos
    """
        
    @staticmethod
    def initialize(filename):
        """
        Inicializa la conexión a la base de datos

        Args:
            filename: Nombre del fichero con la información de conexión
                      El fichero debe estar en la ruta: <root>/dbconfig
                Fichero para conexión
                {URI = ""
                "bbdd": ".......",
                "server": "mongodb.services.clever-cloud.com:27017"
                }
        """
        with open(os.path.join("dbconfig",filename) as f:
            user, passw, bbdd, server = json.load(f).values()
        uri = f"mongodb+srv://{user}:{passw}@{server}"
        client = pymongo.MongoClient(Db.URI)
        db.DB = client[bbdd]
        logger.info(f"Connected to {bbdd}")

    @staticmethod
    def insert(collection, data):
        """
        Inserta un documento en la colección indicada

        Args:
            collection: Nombre de la colección
            data: Diccionario con los datos a insertar
        """
        Db.DB[collection].insert_one(data)

    @staticmethod
    def find(collection, query):
        """
        Devuelve una lista con los documentos que cumplen con el query

        Args:
            collection: Nombre de la colección
            query: Diccionario con los criterios de búsqueda
        """
        return Db.DB[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        """
        Devuelve un documento que cumpla con el query

        Args:
            collection: Nombre de la colección
            query: Diccionario con los criterios de búsqueda
        """
        return Db.DB[collection].find_one(query)
        
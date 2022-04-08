import pymongo
import json
import os
from logger.logger import logger
from datetime import datetime

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
        with open(os.path.join("src", "dbconfig", filename)) as f:
            user, passw, bbdd, server = json.load(f).values()
        uri = f"mongodb+srv://{user}:{passw}@{server}"
        client = pymongo.MongoClient(uri)
        Db.DB = client[bbdd]
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
    def find(collection, query, projection={}, limit=0):
        """
        Devuelve una lista con los documentos que cumplen con el query

        Args:
            collection: Nombre de la colección
            query: Diccionario con los criterios de búsqueda
            limit: Si > 0 limita los registros a la cantidad indicada
        """
        if limit > 0:
            return Db.DB[collection].find(query, projection).limit(limit)
        else:
            return Db.DB[collection].find(query, projection)

    @staticmethod
    def find_one(collection, query, projection={}):
        """
        Devuelve un documento que cumpla con el query

        Args:
            collection: Nombre de la colección
            query: Diccionario con los criterios de búsqueda
        """
        return Db.DB[collection].find_one(query, projection)

    @staticmethod
    def update_one(collection, query, new_data):
        """
        Actualiza los datos de un documento que cumpla con el query

        Args:
            collection: Nombre de la colección
            query: Diccionario con los criterios de búsqueda
            new_data: Diccionario con los datos a insertar
        """
        Db.DB[collection].update_one(query, new_data)


    @staticmethod
    def insert_or_update_price(collection, id, new_data):
        """
        Si el inmueble no existe incluye los datos en la colección indicada
        añadiendo las claves 'history' y 'lastAccess'. 
            'history' es un array que mantiene el histórico de precios:
                {'date': '...', 'price': ...}
            'lastAccess' es una fecha de última acceso al inmueble

        Si el inmueble existe actualiza:
            'price' con el precio extraído de la página
            'lastAccess' con la fecha actual
            'history': añade una entrada si el precio es distinto al anterior
        Args:
            collection: Nombre de la colección
            id: Identificador del inmueble
            new_data: Diccionario con los datos a insertar
        """
        price = new_data['price']
        new_history = [{"date":datetime.now().strftime("%Y-%m-%d"), "price":price}]
        try:
            new_data["history"] = new_history
            new_data["lastAccess"] = datetime.now()
            Db.insert(collection,new_data)
            logger.debug(f"Insertado el inmueble {id}")
        except pymongo.errors.DuplicateKeyError:
            try:
                set_data = [{"$set": {
                    "price":price,
                    "lastAccess":datetime.now(),
                    "history": {
                        "$cond":{
                            "if": {"$ne": ["$price", price]},
                            "then": {"$concatArrays": ["$history", new_history]},
                            "else": "$history"   
                        }
                    }
                }}]
                Db.update_one(collection, {'_id': id}, set_data)
                logger.debug(f"Actualizado el inmueble {id} con el precio {price}")
            except Exception as e: 
                logger.error(f"Error al actualizar el inmueble {id}")
                logger.error(f"id: {id}")
                logger.error(f"price: {price}")
                logger.error(f"query: {set_data}")
                raise Exception(e)


        
# Clase para almacenar la configuración de la aplicación
from dataclasses import dataclass
from dataclasses import dataclass

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]



@dataclass
class Configuration(metaclass=Singleton):
    """
        Clase que almacena la configuración de la aplicación
    """
    store_html: bool = False;
    store_screenshot: bool = False;

config = Configuration()

# Clase para almacenar la configuración de la aplicación
from dataclasses import dataclass

@dataclass()
class Configuration:
    """
        Clase que almacena la configuración de la aplicación
    """
    store_html: bool = False;
    store_screenshot: bool = False;

config = Configuration()

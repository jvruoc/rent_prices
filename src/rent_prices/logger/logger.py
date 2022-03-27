# setup_logger.py
# import logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger('rent_prices')
"""
    Módulo que contiene el logger para la aplicación. El fichero
    logging_config_ini contiene un handler para fichero y otro 
    para consola.

    Logger_root: Handler para consola
    Logger_sLogger: Handler para fichero y consola
"""

import logging
from logging.config import fileConfig
from os import path


log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging_config.ini')
fileConfig(log_file_path)
logger = logging.getLogger("sLogger")

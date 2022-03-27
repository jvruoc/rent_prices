# Rent prices

## Descripción 🚀

Repositorio realizado para la práctica 1 de web scraping de la asignatura _Tipología y ciclo de vida de los datos_ del Máster en Ciencia de Datos de la [Universitat Oberta de Catalunya](https://www.uoc.edu/portal/en/index.html).

## Contenido 📦



## Autores ✒️

* Jose Ventura Roda
* Kevin Martín Chinea

## Recursos 📄

## Sobre estructura del proyecto

He creado una pequeña estructura para intentar organizar todo el código:

```
rent_prices/
├── docker-compose.yml    --> Configuración selenium y scraper
├── Dockerfile            --> Imagen scraper
├── logfile.log           --> Fichero de log
├── pdf
│   ├── images
│   └── README.md
├── README.md
├── src
│   ├── rent_prices
│   │   ├── __init__.py
│   │   ├── logger
│   │   │   ├── __init__.py
│   │   │   ├── logger.py           --> logger de la app
│   │   │   ├── logging_config.ini  --> Configuración logger
│   │   │   └── __pycache__
│   │   ├── scrapers
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   ├── scraperMock.py      --> Ejemplo scraper
│   │   │   └── scraper.py          --> Clase base  
│   │   ├── testPackApp.py      --> Ejemplo lanzador app.
│   │   └── utilities
│   │       ├── __init__.py
│   │       ├── proxyManager.py     --> Pruebas proxies rotatorios
│   │       └── __pycache__
│   └── requirements.txt    --> Dependencias python
└── tests
    └── __init__.py

```

## Sobre proxies rotatorios

He probado los proxies de "http://free-proxy-list.net" y en la primera prueba me ha indicado que funcionaba sólo 1 de la lista, pero al probar por segunda vez ya me ha indicado que no funcionaba ninguno.


## Sobre arranque aplicación en docker

para arrancar la aplicación hay que ejecutar el comando:

```
docker-compose up --build --abort-on-container-exit 
```

Esta instrucción reconstruye el docker e inicia el servicio de Selenium y del Scraper para iniciar la extracción de información. El parámetro `--abort-on-container-exit` hace que cuando un contenedor se detiene se pare el resto de contenedores, así cuando el Scraper finaliza de extraer la información se para también el contenedor de selenium.

El objetivo de llevar el desarrollo a contenedores es poder desplegarlo en un servidor de forma sencilla. Una vez que se finalice la programación de la aplicación, se puede construir una imagen y crear un contenedor a partir de la imagen.

Independientemente de las aplicaciones instaladas en el servidor, cuando se inicien los servicios será capaz de realizar el scraping.

La planificación de su ejecución en el servidor se puede hacer con airflow si se incluye en el contenedor o con crontab si no queremos incluir muchos componentes en el proyecto.

## Sobre los scrapers

He creado una clase base que tiene el código para conectarse a Selenium en local o en remoto, si ejecutamos en local utiliza el DriverManager, en remoto utiliza la instalación de Selenium en remoto.

* En local: pruebas en nuestros equipos
* En remoto (docker): Para despligue en servidor

## Mantenimiento de dependencias

Es importante para el correcto despliegue que el fichero `requirements.txt` tenga todas las dependencias bien definidas.

El proyecto tiene un entorno virtual, para crear el entorno y activarlo:
```
python -m venv .venv/
source .venv/bin/activate
pip install -r requirements.txt
```

Para añadir nuevas dependencias:
```
python -m venv .venv/
source .venv/bin/activate
pip install <nueva libreria>
pip freeze > requirements.txt
```


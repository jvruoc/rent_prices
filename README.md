# Rent prices

## Descripción 🚀

Repositorio realizado para la práctica 1 de web scraping de la asignatura _Tipología y ciclo de vida de los datos_ del Máster en Ciencia de Datos de la [Universitat Oberta de Catalunya](https://www.uoc.edu/portal/en/index.html).

El proyecto aquí presente busca trabajar con diversas páginas web de venta y alquiler de alojamientos para descargar los datos presentes. Concretamente se ha trabajado exclusivamente con el alquiler| centrándonos en los hechos acarreados de los últimos años en los que se ha visto un incremento de la demanda y por consecuencia de sus precios. La web seleccionada para la obtención de los datos se trata de  [Fotocasa](https://www.fotocasa.es/es/), pero la generación del código ha sido enfocada para que se pueda ampliar y desarrollar otras clases que trabajen con otras plataformas de similares contextos.

A lo largo de este _README_ se puede observar el contenido concreto del repositorio, pero para una mayor descripción del conjunto de datos es posible acceder al informe situado en la carpeta _**pdf**_.

### Objetivo 🚀

Recoger la información de la web de Fotocasa, extrayendo los datos de los apartamentos que se encuentran en alquiler. Los datos de estos apartamentos se incluirán en una BBDD de MongoDB y las imágenes publicadas para cada anuncio se descargarán en una unidad de Google Drive.

Se pretende que el proceso se ejecute diariamente para poder obtener la evolución de los precios de alquiler de un inmueble e intentar determinar el tiempo que está publicado cada uno de los anuncios.

### Metodología de desarrollo

A lo largo del desarrollo de la aplicación se ha aplicado una metodología Scrum, con reuniones semanales en las que se establecen las tareas finalizadas, los problemas/errores obtenidos y la definición de los siguientes pasos a realizar. El correspondiente tablero se puede encontrar en el siguiente [enlace](https://github.com/jvruoc/rent_prices/projects/1).

## Código

Se ha creado una clase base, _Scraper.py_, que tiene el código para conectarse a Selenium en local o en remoto, si ejecutamos en local utiliza el DriverManager, en remoto utiliza la instalación de Selenium pero en remoto.

* En local: pruebas en nuestros equipos
* En remoto (docker): despliegue en servidor

A parte de estas conexiones para conectarse a Selenium, dicha clase define los métodos establecidos para acceder a los datos de la web e iterar en las diversas páginas devolviendo los elementos con todas sus características. Algunos de estos métodos son abstractos para garantizar que pueda servir en diferentes webs. Como se puede ver en la clase _ScraperFotocasa.py_ estos métodos heredados de la clase padre se centran en funcionalidades específicas de la web como _aceptar las cookies_, _seleccionar la siguiente página_ ó _obtener contenido específico_.

### Instalación 🔧

#### Local

El proyecto tiene un entorno virtual, para crear el entorno y activarlo:
```
python -m venv .venv/
source .venv/bin/activate
pip install -r requirements.txt
```

_Es importante para el correcto despliegue que el fichero `requirements.txt` tenga todas las dependencias bien definidas._

Para añadir nuevas dependencias:
```
python -m venv .venv/
source .venv/bin/activate
pip install <nueva libreria>
pip freeze > requirements.txt
```

#### Docker

Para ejecutar la aplicación en Docker:

```
docker-compose up --build --abort-on-container-exit
```

Esta instrucción reconstruye el docker e inicia el servicio de Selenium y del Scraper para iniciar la extracción de información. El parámetro `--abort-on-container-exit` hace que cuando un contenedor se detiene se pare el resto de contenedores, así cuando el Scraper finaliza de extraer la información se para también el contenedor de selenium.

El objetivo de llevar el desarrollo a contenedores es poder desplegarlo en un servidor de forma sencilla. Una vez que se finalice la programación de la aplicación, se puede construir una imagen y crear un contenedor a partir de la imagen.

Independientemente de las aplicaciones instaladas en el servidor, cuando se inicien los servicios será capaz de realizar el scraping.

La planificación de su ejecución en el servidor se puede hacer con airflow si se incluye en el contenedor o con crontab si no queremos incluir muchos componentes en el proyecto.

![](pdf/images/arquitectura.svg)

La aplicación está preparada para su ejecución en docker a través del `webdriver remote` de selenium.

Se crea un contenedor que contiene la aplicación construida (`scraper`), que accede a otro contenedor con Selenium instalado (`selenium/standalone-chrome:3.141`).

El contenedor de Selenium incluye todos los componentes necesarios para el acceso a páginas web sin necesidad de instalar ningún navegador en el servidor, y al utilizarlo de forma conjunta con el contenedor de la aplicación, se puede ejecutar de forma sencilla en cualquier dispositivo.

### Contenido 📦

Finalmente el proyecto generado se distribuye con el siguiente árbol de directorios:

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
│   ├── dbconfig
│   │   └── template.json           --> Configuración para el acceso a la BBDD     
│   ├── rent_prices
│   │   ├── __init__.py
│   │   ├── logger
│   │   │   ├── __init__.py
│   │   │   ├── logger.py           --> Logger de la app
│   │   │   ├── logging_config.ini  --> Configuración logger
│   │   │   └── __pycache__
│   │   ├── scrapers
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   ├── scraperMock.py      --> Ejemplo scraper
│   │   │   └── scraper.py          --> Clase base
│   │   │   └── scraperFotocasa.py  --> Clase heredada Fotocasa
│   │   │   └── scraperIdealista.py --> Clase heredada Idealista   
│   │   ├── utilities
│   │   ├   ├── __init__.py
│   │   │   ├── proxyManager.py     --> Pruebas proxies rotatorios
│   │   │   ├── configuration.py    --> Clase para la configuración de la aplicación
│   │   │   ├── database.py         --> Conexción a la base de datos
│   │   │   └── __pycache__
│   │   ├── main.py                 --> Programa principal para ejecutar el scraping
│   │   └── extract.py                 --> Programa principal obtener el CSV
│   └── requirements.txt    --> Dependencias python
└── tests
    └── __init__.py

```

### Ejecución

La ejecución del programa tiene definidos diversos parámetros:

* _--html_: Guarda el html de la página

* _--screenshot_: Guarda una captura de la página.

* _--collection_: Graba en la colección mongo especificada.

* _--output_images_: Se define el directorio en Google Drive para guardar las imágenes.

* _--start_page_: Inicializa el número de página para comenzar el scraping.

## Resultado del proyecto

A lo largo del proyecto se han solventado diversas tareas las cuales están reflejadas en el [tablero de trabajo de este proyecto](https://github.com/jvruoc/rent_prices/projects/1). Pero dentro de estas podemos destacar algunas más concretas como:

* Gestión del user-agent
* Pruebas con diversos proxies (en desarrollo)
* Gestión de sesiones (en desarrollo)
* Dockerizar la aplicación
* Gestión de elementos dinámicos de la aplicación para obtener los datos
* …

Después de todo el desarrollo aplicado podemos ver el resultado que obtenemos, concretamente con respecto al CSV obtenido, a continuación se muestran algunos elementos de ejemplo:

|_id|zipCode|buildingType|buildingSubtype|clientId|clientTypeId|dateOriginal|bathrooms|balcony|air_conditioner|heater|heating|swimming_pool|parking|conservationState|floor|terrace|elevator|rooms|surface|isHighlighted|isPackPremiumPriority|isNewConstruction|hasOpenHouse|isOpportunity|minPrice|otherFeaturesCount|price|periodicityId|history|lastAccess|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
fc-162172800|28023|Flat|GroundFloorWithGarden|9202760159851|3|2022-02-24|2|||||||1|3|1|1|2|91|False|True|False|False|False|0|15|1325|3|"[{'date': '2022-04-04', 'price': 1325}]"|2022-04-09 16:55:15.693000|
fc-161358964|28023|Flat|Flat|9202760159851|3|2022-02-23|2|||||||1|6||1|2|90|False|True|False|False|False|0|15|1120|3|"[{'date': '2022-04-04', 'price': 1120}]"|2022-04-09 16:55:15.743000
fc-162885268|28052|Flat|GroundFloorWithGarden|9202750766581|3|2022-03-10|2|||||||1|3||1|3|109|False|True|False|False|False|0|18|1095|3|"[{'date': '2022-04-04', 'price': 1095}]"|2022-04-09 16:56:23.579000|


## Autores ✒️

* [Jose Ventura Roda](https://www.linkedin.com/in/joseventuraroda/)
* [Kevin Martín Chinea](https://www.linkedin.com/in/kevmch/)

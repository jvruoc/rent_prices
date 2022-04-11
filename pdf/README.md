# Memoria del proyecto

El presente documento refleja los puntos principales de la realización de la práctica 1 de web scraping de la asignatura _Tipología y ciclo de vida de los datos_ del Máster en Ciencia de Datos de la [Universitat Oberta de Catalunya](https://www.uoc.edu/portal/en/index.html), la cual tiene como objetivo general la recolección de datos de una página web.

# 1. Contexto

El contexto de esta práctica se basa en el estudio y el análisis del estado de la situación actual del alquiler, ya que, como se ha vivido en los últimos años existe una gran demanda ligado a su correspondiente aumento de precios. Para esto se ha trabajado con la web [Fotocasa](https://www.fotocasa.es/es/) a través de la herramienta Selenium y centrándonos exclusivamente en Madrid.

A pesar de centrarnos solamente en la web [Fotocasa](https://www.fotocasa.es/es/) todo el código desarrollado se ha enfocado para extrapolar la metodología aplicada a otras web con similar contexto.

# 2. Título

A partir del contexto anterior se ha establecido el nombre _**Madrid Rent Prices**_ para el conjunto de datos generado.

# 3. Descripción del dataset

Como se puede intuir, cada elemento del conjunto representa una casa/piso de alquiler en [Fotocasa](https://www.fotocasa.es/es/) y sus correspondientes atributos los cuales se describirán en las siguientes secciones. Estos elementos se han obtenido en diversos días durante el mes de abril de este año (2022) para tener una variabilidad de los cambios ocurridos en determinados periodos de tiempo.

# 4. Representación gráfica

A continuación se ve una representación del proyecto completo. Se obtienen los datos de [Fotocasa](https://www.fotocasa.es/es/) mediante Selenium y el código realizado en Python. Por un lado, guarda los datos en la base de datos, con la opción de ejecutar el posterior código para transformar estos datos en formato _CSV_ y por otro lado se puede conectar con Google Drive para guardar las imágenes en una carpeta determinada:

![](https://github.com/jvruoc/rent_prices/blob/doc/pdf/images/project.png?raw=true)

# 5. Contenido

El dataset se encuentra formado por las siguientes características:

* _**id**_: Id. del inmueble, este identificador está formado por una sección que define la plataforma de la que se obtienen los datos, y el identificador del piso. Ej: _fc-162172800_

* _**zipCode**_: Código postal en el que se encuentra la localidad. Ej: _28023_

* _**buildingType**_: Categoría del tipo de inmueble, en la mayoría de los casos se tratan de pisos (_Flat_).

* _**buildingSubtype**_: Subtipo de inmueble, valor categórico. Ej: _GroundFloorWithGarden_, _Flat_, _SemiDetached_, _Attic_, ...

* _**clientId**_: Id. del cliente. Ej: _9202750766581_

* _**clientTypeId**_: Categoría del tipo de cliente (_1_ ó _3_).

* _**dateOriginal**_: Fecha de publicación del inmueble. Ej: _2022-03-01_

* _**bathrooms**_: Cantidad de baños (valor numérico). Ej: _2_

* _**balcony**_: Balcón, valor binario tiene o no tiene este extra (_0_ ó _1_).

* _**air_conditioner**_: Aire acondicionado, valor binario tiene o no tiene este extra (_0_ ó _1_).

* _**heater**_: Calentador, valor binario tiene o no tiene este extra (_0_ ó _1_).

* _**heating**_: Calefacción, valor binario tiene o no tiene este extra (_0_ ó _1_).

* _**swimming_pool**_: Piscina, valor binario tiene o no tiene este extra (_0_ ó _1_).

* _**parking**_: Parking propio, valor binario tiene o no tiene este extra (_0_ ó _1_).

* _**conservationState**_: Estado de conservación valor categórico (1, 2, 3, 4, ó 8).

* _**floor**_: Planta en la que se sitúa el piso. Ej: _4_

* _**terrace**_: Terrazas, valor binario tiene o no tiene este extra (_0_ ó _1_).

* _**elevator**_: Ascensores, valor binario tiene o no tiene este extra (_0_ ó _1_).

* _**rooms**_: Número de habitaciones. Ej: _3_

* _**surface**_: Superficie de la vivienda en m². Ej: _102_

* _**isHighlighted**_: Valor binario que define si el inmueble está destacado o no (_True_ ó _False_).

* _**isPackPremiumPriority**_: Anuncio premium, valor binario (_True_ ó _False_).

* _**isNewConstruction**_: Es de nueva construcción, valor binario (_True_ ó _False_).

* _**hasOpenHouse**_: Visita libre, valor binario (_True_ ó _False_).

* _**isOpportunity**_: Es una oportunidad, valor binario (_True_ ó _False_).

* _**minPrice**_: Precio mínimo aceptado. Ej: _0_

* _**otherFeaturesCount**_: Cantidad de características adicionales, valor numérico. Ej: _15_

* _**price**_: Precio del alquiler. Ej: _1325_

* _**periodicityId**_: Periodicidad del alquiler variable categórica (_1_ ó _3_).

* _**history**_: Historial de precios del inmueble. Ej: _[{'date': '2022-04-04', 'price': 1120}]_

* _**lastAccess**_: Última fecha de acceso a la obtención de los datos. Ej: _2022-04-09 16:55:15.693000_

Además se ha trabajado con las imágenes aunque no se haya unificado con el conjunto de datos por motivos de almacenamiento:

![](https://github.com/jvruoc/rent_prices/blob/master/pdf/images/downloaded%20examples/fc-162706645-466660935.jpg?raw=true)

# 6. Agradecimientos

Específicamente el conjunto de datos obtenido se ha generado, como se comentó en secciones anteriores, de la plataforma de venta y alquiler de viviendas [Fotocasa](https://www.fotocasa.es/es/). Gracias al enfoque de servicios que presenta nos ha permitido definir diversas características para obtener todos los datos mediante técnicas de scraping y conseguir obtener el conjunto de datos aquí presente. Siguiendo los modelos que presentan este tipo de plataformas para anonimizar su localización dentro de los datos recolectados se han obviado algunos como podrían ser cualquier aspecto con el que se pueda obtener la dirección real del establecimiento. Todo con el fin de que esto no pueda generar ningún problema al proceso de alquiler o al actual propietario. A parte de este tipo de información el resto de atributos se consideran dentro de los principios éticos y legales del contexto del proyecto.

# 7. Inspiración

El fin de trabajar con estos datos es por el potencial que presentan. De similar forma existen otros conjuntos de datos los cuales tienen unas similares características pero están enfocados en una mayor medida a el precio de venta de determinadas viviendas, podemos ver un ejemplo en el conjunto de datos _[House Prices - Advanced Regression Techniques](https://www.kaggle.com/c/house-prices-advanced-regression-techniques)_ de Kaggle. En este, como su título indica se busca aplicar técnicas de regresión para predecir los precios de una vivienda según sus características.

En nuestro caso, no sólo se busca poder responder a estas cuestiones, si no que se planean otras como podrían ser la predicción del tiempo que una vivienda estará en alquiler (por esto el motivo de registrar los datos existentes en diferentes fechas). Con esto se podría optimizar el tiempo de publicación de los anuncios, destacando los parámetros que influyen en mayor medida para que un alojamiento sea alquilado en un determinado periodo de tiempo.

# 8. Licencia

Dentro de las licencias establecidas para su publicación se le ha asignado la **CC BY-SA 4.0 License**. El motivo de aplicar este tipo de licencia es que permite el uso de la obra, incluyendo en esto su modificación pero destacando que la autoría original tiene que estar presente definiendo así cualquier cambio o transformación realizada en el conjunto de datos. Además, por el potencial que observamos en los datos para su uso comercial permitimos así su uso en este contexto.

# 9. Código

El código para generar el correspondiente conjunto de datos se ha realizado mediante el lenguaje de programación Python. Este se encuentra disponible en el siguiente [repositorio de Github](https://github.com/jvruoc/rent_prices). En el README principal de dicho repositorio se describen detalladamente las carpetas y códigos existentes que lo forman, además de las diversas formas de ejecución desarrolladas y otras notas importantes al trabajar con este proyecto.

# 10. Dataset

Finalmente, el resultado final del dataset se puede encontrar en Zenodo a través del siguiente [enlace del DOI]().

# 11. Contribuciones

En este apartado se reflejan las contribuciones realizadas por cada uno de los autores en las diversas tareas realizadas. Las iniciales en la sección de firma representan la confirmación por parte del autor de su participación en el apartado correspondiente.

| Contribución| Firma|
|-------------------|-------------|
| Investigación previa | V. R., J. - M.Ch., K. |
| Redacción de las respuestas | M.Ch., K. - V. R., J. |
| Desarrollo del código: |
|  - User-agent aleatorio | M.Ch., K. |
|  - Aceptación de las cookies | V. R., J. |
|  - Pruebas con proxys | V. R., J. |
|  - Gestión de elementos dinámicos | M.Ch., K. - V. R., J. |
|  - Descarga de imágenes y subida a Google Drive | M.Ch., K. |
|  - Obtención de características | M.Ch., K. - V. R., J. |
| Base de datos MongoDB Atlas (carga y extracción) | V. R., J. |
| Dockerización de la aplicación | V. R., J. |

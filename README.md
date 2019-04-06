# Shopping person counter

Es un proyecto de visión artificial cuyo cometido es cuantificar el número de personas que pasan de largo por el escaparate de un comercio y no llegan a entrar en el mismo.

El **cliente** José Vélez Serrano tiene la **necesidad** de conocer la cantidad de personas que pasan
de largo por el escaparate de un comercio, sin entrar en el establecimiento. 

Con el **objetivo** de conocer la capacidad de atracción del escaparate del comercio sobre los potenciales clientes.

Para ello **se propone** establecer un sistema de video vigilancia sobre la entrada de la tienda, que permita informar con una posterior interfaz web al cliente de cuantos peatones han pasado de largo por el escaparate sin entrar en el comercio.


Las características con las que el sistema deberá contar son las siguientes:

- El sistema deberá contar con un sistema de videovigilancia encargado de la grabación de la zona del escaparate y
entrada de la tienda.
- Se desarrollará un sistema de visión artificial encargado de la detección de personas y de comprobar cuantas de
estas no entran en el comercio, es decir, pasan de largo.
- Se desarrollará una interfaz web a la cual se podrá acceder fácilmente desde dispositivos con conexión a internet,
smartphones, ordenadores…
- La interfaz web permitirá entrar con una clave de acceso al interesado, el cual podrá obtener las métricas de las
personas que pasan de largo a lo largo de un día, respecto del total de personas que pasan por en frente del
escaparate.

Se aplican las siguientes **condiciones o restricciones** que deberá cumplir el sistema:

- El sistema ha de ser capaz de registrar e identificar el número de personas que pasan por delante del escaparate
con una precisión del 90% como mínimo, es decir que solo 1/10 personas puede no ser reconocida por el sistema.

- El sistema habrá de funcionar durante las 24 horas del día, pero será el usuario el encargado de habilitar y
deshabilitar el sistema durante las horas que el comercio permanezca cerrado en caso de desearlo.
- El sistema deberá cumplir con Ley Orgánica de Protección de Datos y el Reglamento General de Protección de
Datos europeo, debiendo entre otras cosas, colocar un cartel informativo sobre la existencia de videocámara, así
como impresos para que los peatones puedan ejercer sus derechos.
- El desarrollo de el proyecto se realizará en un plazo de dos meses una vez que se apruebe.

# Prerequisitos

El proyecto se ha desarrollado con la versión de **python 3.6**. Cualquier versión de python 3.X.X deberia funcionar.
En caso de no contar con una instalación de python 3.X.X, por favor instale una.
Se recomienda la creación de un entorno virtual mediante por ejemplo "virtualenv" aunque no es necesario.
Para la correcta ejecución de la aplicación es necesario tener instalado las siguientes dependencias.

```
$ pip install numpy==1.16.1
$ pip install scikit-learn==0.20.3
$ pip install opencv-python==3.4.2.17
```
# Instalación de AIVA_shopping_person_counter

Para la descarga e instalación de este proyecto se recomienda usar la herramienta git. En una consola utilice el siguiente comando:

```
$ git clone https://github.com/garciamorenc/AIVA_shopping_person_counter
```
 Esto descargará el proyecto en un directorio de nombre AIVA_shopping_person_counter.


# Test unitarios

Se proporciona una colección de test unitarios en el directory **unit_test**. Su lanzamiento puede realizarse mediante el siguiente comando.

``$ python test_main.py``

# Ejecución

Podemos ejecutar la aplicación mediante la linea de commando para ello deberemos seguir los siguientes pasos:

* Configurar el sistema.
* Realizar el conteo de personas.

## Linea de comandos

### Configuración
En primer lugar es necesario parametrizar la configuración que utilizaremos indicando las coordenadas de la entrada del comercio (x0, y0, x1, y1) y una imagen de nuestro comercio sin ninguna oclusión. Se recomienda el uso de los datos indicados en la siguiente instrucción.

``$ python initialize_configuration.py -c 214 135 360 200 -b resources/background.png``


### Resultados
A través del módulo pedestrian_counter.py realizaremos el conteo de personas que han pasado por delante del comercio y no han llegado a entrar. Para ello es necesario indicar el video sobre el cual queremos aplicar el algoritmo, además exite la opción de ver los resultados durante la ejecución o no, si indicamos el parámero **-t** se mostrarán los resultados (en caso de no querer ver los resultados bastará con no indicar dicho parámetro). Se recomienda el uso de los datos indicados en la siguiente instrucción.

``$ python pedestrian_counter.py -v dataset_2/ThreePastShop1front.mpg -t``

Si la ejecución ha sido correcta nos mostrará el restultado por pantalla:

``Total of people who did not enter the store: 3``


## Docker
Se ha creado un contenedor Docker que proporciona un entorno de ejecución completo para su uso deberemos seguir los siguientes pasos.

### Obtención del contendor
La imagen se encuentra alojada en docker hub, para su obtención debemos usar el siguiente commando:
``$ docker pull garciamorenc/aiva_shopping_person_counter``

### Ejecución
Una vez tengamos la imagen podremos ejecutar la aplicación en modo configuración o en modo análisis de videos.

Para que nuestro contenedor tenga acceso a ficheros del exterior propios de la configuración o los videos a analizar deberemos trabajar mediante volúmenes. Deberemos crear las siguientes rutas de ficheros:

- /mydata/configuration
- /mydata/videos

Por ejemplo, podemos crear esta estructura de carpetas en el $HOME path. En la ruta **configuration** incluiremos una imagen de nuestro comercio sin oclusiones como la que se proporiona en la ruta de este repositorio **/AIVA_shopping_person_counter/resources/background.png**. Por otro lado en la ruta **videos** incluiremos los videos que deseemos analizar, en este caso podemos utilizar el video proporcionado en este repositorio **AIVA_shopping_person_counter/dataset_2/ThreePastShop1front.mpg**. De modo que tendremos la siguiente estructura en nuestro $HOME path.

![configuration_example](https://i.imgur.com/q5ve1Yb.png)

#### Configuración
En primer lugar es necesario parametrizar la configuración que utilizaremos indicando las coordenadas de la entrada del comercio (x0, y0, x1, y1) y una imagen de nuestro comercio sin ninguna oclusión. 

Apoyandonos en la estructura de carpeta que hemos realizado podeoms aplicar la configuración desada mediante el siguiente comando.

``$ sudo docker run -v /home/docker_data/configuration/:/config aiva_shopping_person_counter -a configuration -x 214 -y 135 -w 360 -h 200 -b config/background.png ``

Si hemos realizado este paso correctamente recibiremos un mensaje indicando la correcta ejecución:

``$ Configuration saved to config.xml``

### Análisis de video
Nuevamente nos apoyaremos en la estructura de carpetas creada previamente de modo que podremos realizar el análisis de los videos que queramos através de la siguiente instrucción.

``$ sudo docker run -v /home/docker_data/videos/:/videos aiva_shopping_person_counter -a video``

La ejecución nos indicará el video que se esta analizando en cada momento y al terminar podremos acceder a la ruta **/home/docker_data/videos** donde encontraremos ficheros de texto con el nombre del video al que corresponden indicandonos el número de personas que han pasado por delante de la tienda y no han llegado a entrar.

# Autores

* **Omar Garrido Martín** - [omar-ogm](https://github.com/omar-ogm)
* **Carlos García Moreno** - [garciamorenc](https://github.com/garciamorenc)

# Licencia

Este proyecto está licenciado bajo la licencia MIT - vea el documento [LICENSE.md](LICENSE) para más detalles.

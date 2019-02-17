# Shopping person counter

Es un proyecto de visión artificial cuyo cometido es cuantificar el número de personas que pasan de largo por el escaparate de un comercio y no llegan a entrar en el mismo.

Se proveerá de una interfaz gráfica que facilite el uso del sistema implementado.

# Prerequisitos

Para la correcta ejecución de la aplicación es necesario tener instalado el módulo Numpy.

```
$ pip install numpy
```

# Test unitarios

Se proporciona una colección de test unitarios en el directory **unit_test**. Su lanzamiento puede realizarse mediante el siguiente comando.

``$ python test_main.py``

# Ejecución

Podemos ejecutar la aplicación mediante la linea de commando o una interfaz gráfica. En ambas opciones deberemos seguir los siguientes pasos:

* Configurar el sistema.
* Realizar el conteo de personas.

## Linea de comandos

### Configuración
En primer lugar es necesario parametrizar la configuración que utilizaremos indicando las coordenadas de la entrada del comercio (x0, y0, x1, y1).

``$ python initialize_configuration.py -c 10 10 50 50``


### Resultados
A través del módulo pedestrian_counter.py realizaremos el conteo de personas que han pasado por delante del comercio y no han llegado a entrar.

``$ python pedestrian_counter.py -v /path/to/video``

Si la ejecución ha sido correcta nos mostrará el restultado por pantalla:

``Total of people who did not enter the store: 1``


## Interfaz web

En futuras implementaciones ser permitirá la ejecución y configuración de la aplicación mediante un entorno web.

En construcción ...

# Autores

* **Omar Garrido Martín** - [omar-ogm](https://github.com/omar-ogm)
* **Carlos García Moreno** - [garciamorenc](https://github.com/garciamorenc)

# Licencia

Este proyecto está licenciado bajo la licencia MIT - vea el documento [LICENSE.md](LICENSE.md) para más detalles.
# Technical Challenge for Python

### Objetivo

Crear un endpoint local que exponga una operación que permita: instalar y lanzar una app Android (.apk) en un emulador local o en un device real (conectado via USB). 

Se deberá utilizar lenguaje Python y Android SDK.

## Getting Started

El proyecto está desarrollado con Python 2.7 y las librerías que se detallan en la seccion de pre-requisitos. Para levantar el endpoint localmente se deben seguir las instrucciones de la sección ejecución

### Pre-requisitos

Por ahora el endpoint fue testeado en sistemas Linux por lo que se recomiendo ejecutarlo en dicho entorno. 
Para el proyecto se utilizó la librería  [AndroidViewClient](https://github.com/dtmilano/AndroidViewClient) junto con Android Debug Bridge (adb) y Android Asset Packaging Tool (aapt)

La versión estable AndroidViewClient funciona con Python 2.7 por lo que es recomendable instalarlo un entorno separado como se recomienda en [su documentación](https://github.com/dtmilano/AndroidViewClient/wiki). 
Lo mejor es instalarlo a través de pip en el entorno virtual creado ejecutando: 

```
pip install androidviewclient
```

Para installar adb y aapt puede instalarse por completo [Android SDK](https://developer.android.com/studio) o en en caso que se utilize ubuntu o alguna distribución similar se pueden instalar por separado esas herramientas con:

```
sudo apt-get install android-tools-adb android-tools-fastboot aapt
```

Para verificar que esté todo instalado correctamente se pueden verificar las versiones de ambas herramientas: 

```
adb version
```

```
aapt version
```
En el caso que se use un dispositivo real para ejecutar el challenge, recordar que se debe habilitar la depuración por usb dentro de las opciones de desarrollador. 

### Instalación

Una vez que se hayan completado los pasos antes mencionados, se debe clonar este repositorio en cualquier carpeta.
Luego, se debe activar el entorno de python en el cual se van a instalar las dependencias (si es que se hizo uno separado). 
Todo lo necesario para ejecutar las pruebas y correr el endpoint está detallado en el archivo * *requiremets.txt* *  y se pueden installar ejecutando:

```
pip install -r requirements.txt
```

Para verificar que todo esté listo se puede usar el script * *check.py* * desarrollado por los autores de AndroidViewClient:

```
python check.py
```
En pantalla se deberá ver un * *OK* * . En caso contrario se deben seguir los pasos detallados en [la documentación oficial](https://github.com/dtmilano/AndroidViewClient/wiki)  

## Ejecución

Para ejecutar el endpoint simplemente se debe escribir en consola y dentro de la carpeta donde se haya clonado el proyecto:

```
python challenge.py
```

Con esto debería verse en pantalla algo como lo siguiente:

Esto significa que el endpoint está ejecutándose dentro del servidor * *localhost:8000* * .
La operación para instalar la apk y tomar el screenshot se ecuentran en el endpoint * *localhost:8000/run* * y se debe pasar como parámetro el nombre de la apk que se quiera instalar. Para ver las apks disponibles 

## Ejecutar los tests

Las pruebas unitarias están desarrolladas con pytest y para ejecutarlas primero debe estar levantado el servidor siguiendo los pasos de la sección anterior. Posteriormente simplemente se debe escribir: 

```
pytest test
```
Esto probará que el endpoint esté disponible y devuelva todo correctamente. 

---
## Preguntas
- ¿Cómo resolvió el problema?
Para resolver el problema decidí utilizar flask para levantar el endpoint ya que era una herramienta que ya conocía. Preferí invertir parte del timpo en investigar todo lo involucrado con el control de android ya que es en lo que menos experiencia tengo. 
Para la parte de la instalación de la app y todo lo relativo a ello, ejecuté el adb del android SDK a través de python con la librería standard subprocess junto con AndroidViewClient. Como esta útlima por ahora solo funciona en android 2.7 decidí desarrollar todo en esa versión. Me incliné por esa librería por sobre otras similares porque es la más actualizada, siendo que el último commit se hizo hace dos meses contra otras tal vez más conocidas que no se actualizan desde hace años. 
Para instalar la aplicación extraigo el nombre del paquete desde el archivo .apk con * *aapt* * y uso grep para extraer solamente lo que necesito. Esto hizo que perdiera la posibilidad de ejecutarse en otras plataformas que no sean linux, pero por el límite de tiempo decidí mantener la solución simple en lugar de buscar algo 100% multiplataforma. Luego que se instala la aplicación, extraigo el nombre de actividad de la apk para ejecutarla. Esto lo hice para no tener que buscar pantalla por pantalla a la aplicación y hacer click en ella, lo que permite siempre encontar a la app independientemente del layout del launcher del smartphone. Una vez que se ejecuta la app, se toma el screeshot con AndroidViewClient y se almacena con el nombre de la apk junto con un timestamp. Lo que la api devuelve se puede observar en la sección de documentación.

- ¿Cuáles fueron los principales desafios?
El principal desafío fue entender cómo utilizar python junto con Android SDK y cómo manejar un dispositivo conectado por USB. Si bien puede ser trivial, es algo que nunca tuve la necesidad de desarrollar y tuve que investigar bastante. También estuve un tiempo pensando la mejor forma de ejecutar la app sin depender de la navegación por el dispositivo. 

- ¿Cómo probar el endpoint?
El endpoint se puede probar con los tests que vienen en el proyecto. Sino se puede usar cualquier .apk que se quiera y se deben seguir los pasos de la documentación. 

- Si quisiera darle acceso a un tercero para que pueda instalar cualquier APK en una lista de emuladores existentes, ¿cómo lo resolvería ?
Por como está armado el proyecto, primero tendría que darle la posibilidad de cargar una APK en la carpeta del servidor. Luego tendría que proveerle la lista de dispositivos disponibles, cosa que se podría hacer mostrando el resultado de * *adb devices* * para que pueda envíar como parámetros el nombre de la apk a instalar y el dispositivo en el cuál lo quiere probar.  

- Si tuviese más de 8 horas ... ¿qué haría?
Si tuvuese más de 8 horas habría pensado como evitar la dependencia de un sistema linux para ejecutar algunas de las funciones del proyecto. Además agregaría más pruebas ya que todo lo hice con un celular físico y no probé de testearlo con un emulador android ni con otras apks. Me hubiera gustado también documentar más los scripts y agregar un par de pruebas unitarias más para las funciones del script android_utils.py 

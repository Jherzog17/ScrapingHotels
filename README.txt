Estructura del proyecto:
El proyecto  se divide en carpetas. En la carpeta de Datos podemos encontrar 2 subcarpetas, Crudo y Limpio.
En Crudo están los csv tan cual salen del scraping mientras que en limpio están los csvs procesados.
Luego está la carpeta Scrapings, la cual contiene todos los archivos relevantes al scraping tanto dinámico como
estático. Por otro lado tenemos la carpeta Pruebas, la cual contiene el archivo que se va a ejecutar durante la presentación
como prueba en directo. Por último, tenemos Scripts Limpieza Datos, la cual contiene todos los archivos relacionados
con la limpieza de los datos. Además de todo esto, de la carpeta root cuelga un archivo llamado ejecutar scrapings, el
cual lo que hace es ejecutar todos los scrapings para todas las webs y lugares de forma seguida.

Ejecutar el código:
Si se quiere ejecutar la parte del scraping basta con ejecutar el archivo ejecutar_scrapings.py en la carpeta root.
Por otro lado, si se desea ejecutar algún archivo relacionado con la limpieza de datos o generación de gŕaficas se 
deberá acceder a la carpeta de Scripts Limpieza Datos y ejecutar el archivo que se desee.

Librerias:
-BeutifulSoup v4.14.2
-Selenium v4.38.0
-Pandas 2.3.3
-Matplotlib 3.10.7
-Numpy v2.3.4


from scrapBooking import *

import os

# ajuste de la ruta de trabajo para asegurar que se puede guardar el csv 
# conn ello el programa siempre se ejecute desde la carpeta
# donde se encuentra este archivo y asi las rutas
# relativas ( ../csv/) funiconaran siempre sin importar
# desde dónde se ejecute el script 
carpeta_actual = os.path.abspath(os.path.dirname(__file__))  # ruta absoluta de este archivo
os.chdir(carpeta_actual)  # camba la carpeta de trabajo a ScrapBooking

"""
Script que ejecuta el scraping completo a Booking
"""

#Parametros ajustables
url = "https://www.booking.com"
lugar = "Ibiza"
nom_csv_ibiza = "resultados_booking_ibiza.csv"

#Ejecutar código
ejecutar_script(url, lugar,nom_csv_ibiza)


from scrapAmimir import *

#Scrap para Ibiza

url="https://www.amimir.com/es/"
lugar_ibiza ="Ibiza"
nom_csv_ibiza = "resultados_amimir_ibiza.csv"

ejecutar_script(url, lugar_ibiza, nom_csv_ibiza)


#Scrap para Sevilla

lugar_sevilla ="Sevilla"
nom_csv_sevilla = "resultados_amimir_sevilla.csv"

ejecutar_script(url, lugar_sevilla, nom_csv_sevilla)
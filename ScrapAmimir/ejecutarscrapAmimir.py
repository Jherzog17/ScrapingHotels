from scrapAmimir import *

#Scrap para Ibiza

url="https://www.amimir.com/es/"
lugar_ibiza ="Ibiza"
nom_csv_ibiza = "resultados_amimir_ibiza.csv"

ejecutar_script(url, lugar_ibiza, nom_csv_ibiza)


#Scrap para Murcia

lugar_murcia ="Valencia"
nom_csv_murcia = "resultados_amimir_murcia.csv"

ejecutar_script(url, lugar_murcia, nom_csv_murcia)
from Scraping.scrapAmimir import ejecutar_script_amimir, AMIMIR
from Scraping.scrapBooking import ejecutar_script_booking, BOOKING
from Scraping.scrapeDreams import ejecutar_script_edreams, EDREAMS
import time

print(f"Hora de inicio: [{time.strftime('%H:%M:%S')}]")#Esto es para saber cuanto tarda por curiosidad
lista_lugares = ["Ibiza", "Sevilla", "Zaragoza"]
webs = [AMIMIR, BOOKING, EDREAMS]

ejecuciones= []
i = 0
for lugar in lista_lugares:

    nom_csv = f"resultados_{webs[i]}_{lugar}.csv"
    i+=1
    ejecutar_script_amimir(lugar, nom_csv)

    nom_csv = f"resultados_{webs[i]}_{lugar}.csv"
    i+=1
    ejecutar_script_booking(lugar, nom_csv)

    nom_csv = f"resultados_{webs[i]}_{lugar}.csv"
    i+=1
    ejecutar_script_edreams(lugar, nom_csv)

    i=0

print(f"Hora de fin: [{time.strftime('%H:%M:%S')}] ")
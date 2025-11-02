from ScrapAmimir.scrapAmimir import ejecutar_script_amimir, AMIMIR
from ScrapBooking.scrapBooking import ejecutar_script_booking, BOOKING
from scrapingEdreams.scrapeDreams import ejecutar_script_edreams, EDREAMS
import multiprocessing
import threading
import time

# if __name__ == "__main__":
#     print(f"Hora de inicio: [{time.strftime('%H:%M:%S')}]")
#     lista_lugares = ["Ibiza", "Sevilla"]
#     webs = [AMIMIR, BOOKING, EDREAMS]

#     ejecuciones= []
#     i = 0
#     for lugar in lista_lugares:
#         nom_csv = f"resultados_{webs[i]}_{lugar}.csv"
#         i+=1
#         proceso = multiprocessing.Process(target=ejecutar_script_amimir, args=(lugar, nom_csv))
#         ejecuciones.append(proceso)
#         nom_csv = f"resultados_{webs[i]}_{lugar}.csv"
#         i+=1

#         nom_csv = f"resultados_{webs[i]}_{lugar}.csv"
#         proceso = multiprocessing.Process(target=ejecutar_script_booking, args=(lugar, nom_csv))
#         ejecuciones.append(proceso)
#         i=0

#     for proc in ejecuciones:
#         proc.start()


#     for ejec in ejecuciones:
#         ejec.join()
    
#     print("Todas las ejecuciones finalizadas")
#     print(f"hora de fin: [{time.strftime('%H:%M:%S')}]")

print(f"Hora de inicio: [{time.strftime('%H:%M:%S')}]")
lista_lugares = ["Ibiza", "Sevilla"]
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
    # nom_csv = f"resultados_{webs[i]}_{lugar}.csv"
    # i+=1
    i=0

print(f"Hora de fin: [{time.strftime('%H:%M:%S')}]")
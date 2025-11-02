from scrapAmimir import *

#Scrap para Ibiza

lugar_ibiza ="Ibiza"
nom_csv_ibiza = "resultados_amimir_ibiza.csv"

print(f"[{time.strftime('%H:%M:%S')}] Proceso Ibiza iniciado.")
ejecutar_script_amimir(lugar_ibiza, nom_csv_ibiza)
print(f"[{time.strftime('%H:%M:%S')}] Proceso Ibiza terminado.")

#Scrap para Sevilla

lugar_sevilla ="Sevilla"
nom_csv_sevilla = "resultados_amimir_sevilla.csv"

print(f"[{time.strftime('%H:%M:%S')}] Proceso Sevilla iniciado.")
ejecutar_script_amimir(lugar_sevilla, nom_csv_sevilla)
print(f"[{time.strftime('%H:%M:%S')}] Proceso Sevilla terminado.")
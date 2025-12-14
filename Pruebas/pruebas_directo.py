import sys
from pathlib import Path

carpeta_root = Path(__file__).parent.parent
sys.path.insert(0, str(carpeta_root))

from Scraping.scrapBooking import ejecutar_script_booking
from Scraping.scrapeDreams import ejecutar_script_edreams
from Scraping.scrapAmimir import ejecutar_script_amimir
from ScriptsLimpiezaDatos.diff_precios_por_zonas import leer_csv_zona_webs, normalizar_nombres, unir_df, plot_comparativa_webs
from ScriptsLimpiezaDatos.precio import limpiar_puntuacion

if __name__ == "__main__":
    ejecutar_script_amimir("Zaragoza", f"{carpeta_root}/Datos/Crudo/resultados_Amimir_Zaragoza.csv")
    ejecutar_script_booking("Zaragoza", f"{carpeta_root}/Datos/Crudo/resultados_Booking_Zaragoza.csv")
    ejecutar_script_edreams("Zaragoza", f"{carpeta_root}/Datos/Crudo/resultados_Edreams_Zaragoza.csv")

    dfs_dict = leer_csv_zona_webs(["Zaragoza"], ["Amimir", "Booking", "Edreams"])
    df_norm_dict = normalizar_nombres(dfs_dict)
    df_unido = unir_df(df_norm_dict)

    df_unido["Puntuacion"] = df_unido["Puntuacion"].map(limpiar_puntuacion)
    df_unido["Precio"] = df_unido["Precio"].map(limpiar_puntuacion)

    plot_comparativa_webs(df_unido)
    
    
from diff_precios_por_zonas import leer_csv_zona_webs, unir_df
import numpy as np
import matplotlib.pyplot as plt

def dividir_apartamento_hotel_etc(df):
    """
    Esta función, crea una columna nueva en el que dependiendo del nombre del alojamiento lo clasifica según convenga,
    si no es capaz de clasificarlo, lo pone como nan y luego lo quita
    """
    df["Tipo_alojamiento"] = df["Nombre"].apply(clasificar_alojamiento)
    df_sin_na = df.dropna(subset=["Tipo_alojamiento"])#Quitar los na si hay
    return df_sin_na
    
def clasificar_alojamiento(nombre):
    """
    Función que dado un string, clasifica dicho string en un tipo de alojamiento u otro. Si no es capaz de clasificarlo,
    lo clasifica con nan.
    """
    res = ""
    nombre_minusc = str(nombre).lower()
    
    tipo_aloj = {"Apartamento": ["apartamento", "apartamentos", "apartments", "apartment", "aparment", "aparments", "suites","suite"],
                 "Hotel": ["hoteles", "hotels","hotel"],
                 "Hostal": ["hostales", "hostal", "hostel"],
                 "Posada": ["posadas", "posada", "guesthouses", "guesthouse"],
                 "Pension": ["pensiones", "pensión", "pension"]}
    
    for key,values in tipo_aloj.items():
        for opcion in values:
            if opcion in nombre_minusc:
                res = key
    if res == "":
        res = np.nan
    return res
    

def hacer_plot_freq_tipo_aloj(df):
    """
    Función que crea un plot de tipo tarta donde aparece la distribución de los tipos de alojamientos
    """
    df_grupos = df.groupby("Tipo_alojamiento").count()
    grafica = df_grupos["Nombre"].plot(kind="pie", autopct= lambda p : "{:.1f}%".format(p), labels=None,
                                    title="Distribución de tipos de alojamiento")
    plt.ylabel("")
    plt.legend(["Apartamento", "Hostal", "Hotel", "Pensión", "Posada"], loc="upper right", bbox_to_anchor=(1.3, 1))
    plt.show()


if __name__ == "__main__":
    dfs = leer_csv_zona_webs(["Sevilla"], ["Amimir", "Booking", "Edreams"])
    df_unido = unir_df(dfs)
    df_divido_tipos = dividir_apartamento_hotel_etc(df_unido)
    hacer_plot_freq_tipo_aloj(df_divido_tipos)

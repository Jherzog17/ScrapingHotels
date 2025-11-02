from typing import re

def sacarHtmlEstático(driver):
    """
    Función que saca el Html de la pagina estatica a scrapear
    """
    WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, "//body"))) #Esperar a que cargue todo
    WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, "//html")))
    html_estatico = driver.page_source
    soup = BeautifulSoup(html_estatico, "html.parser")
    return soup

def sacarInfoHotel(soup):
    result = []
    try:
        hotel_data = soup.findAll(name="div", attrs={"class":"e1e2fhza0 css-1xbhoqb e4px6vc2"})
        for hd in hotel_data:
            h_nombre = hd.find(name="div", attrs={"class":"css-1kr9ao9 e1hue9ey0"}).text
            h_puntuacion_div = hd.find(name="div", attrs={"class": "css-ap40a3 e8d0hso0"})
            if h_puntuacion_div:
                texto_puntuacion = h_puntuacion_div.text.strip()
                match = re.search(r'\d+(\.\d+)?', texto_puntuacion)
                h_rate = match.group() if match else ""
            else:
                h_rate = ""
            h_price = hd.find(name="span", attrs={"class":"css-1vtqrtx e139ay0z0"}).text
            h_estrellas = len(hd.findAll(name="i", attrs={"class":"css-lbmci7 e5a5h7y0"}))
            h_direccion =hd.find(name="div", attrs={"class":"css-9xspy4 e8d0hso0"}).text
            if len(h_nombre) > 0:
                result.append(h_nombre + ";" + h_rate*2 + ";" + h_price + ";" + str(h_estrellas) + ";" + h_direccion)
        return result
    except Exception as e:
        print(f"Fallo al conseguir la info de prueba {e}")


def guardar_en_csv(datos_hoteles, nombre_archivo='hoteles_extraidos.csv'):
    cabeceras = ['Nombre', 'Puntuacion', 'Precio', 'Estrellas', 'Direccion']
    try:
        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo_csv:
            escritor = csv.writer(archivo_csv, delimiter=';')
            escritor.writerow(cabeceras)
            for linea_datos in datos_hoteles:
                fila_lista = linea_datos.split(';')
                escritor.writerow(fila_lista)

        print(f"¡Datos guardados exitosamente en '{nombre_archivo}'!")

    except IOError as e:
        print(f" Error al escribir el archivo CSV: {e}")

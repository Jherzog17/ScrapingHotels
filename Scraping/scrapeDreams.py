from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import re
import time
import numpy as np

EDREAMS = "Edreams"

#----------------------------Inicio scraping dinámico-----------------------------------
def iniciar_navegador():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = "/usr/bin/chromium-browser"

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.edreams.com/")
    return driver


def aceptarCookies(driver):
    '''
    Función que acepta las cookies de Amimir
    '''
    try:
        btn_accpt_cookies = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button")))
        btn_accpt_cookies.click()
        print("Cookies aceptadas con éxito")
    except Exception as e:
        print(f"Error al aceptar cookies: {e}")

def cerrarLogin(driver):
    '''
    Función que cierra el popup del login
    '''
    try:
        cerrar_login = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='css-s5y9r0 eq1iaxz0']")))
        cerrar_login.click()
        print("Login cerrado con éxito")
    except Exception as e:
        print(f"Error al cerrar el login")

def pulsar_hotels(driver):
    try:
        hot=WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[@test-id='tab-hotels']")))
        hot.click()
        print("Opción hotels seleccionada con exito")
    except Exception as e:
        print(f"errro al pulsar hotels: {e}")

def seleccionarLugar(driver, lugar):
    '''
    Función que escribe en el buscador un lugar
    '''
    try:
        # Esperar y enfocar el input
        input_buscador = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='Search for a destination or hotel']"))
        )
        input_buscador.send_keys(lugar)
        coger_ibiza=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@test-id='airport-destination']/div/div[1]/ul/li")))
        coger_ibiza.click()
        print("Lugar seleccionado con éxito")

    except Exception as e:
        print(f"Error al introducir destino: {e}")

def seleccionarFechas(driver):
    """
    funcion para elegir las fechas, que serán del 17 al 18 de febrero
    """
    try:

        #Seleccionar botón fecha
        btn_fecha_inicio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='departure-date-picker']/div/div/div/input")))
        btn_fecha_inicio.click()

        #Seleccionar pasar mes
        btn_pasar_mes=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='departure-date-picker']/div/div/div[2]/div/div/div/div[4]/button")))
        btn_pasar_mes.click()

        #Botón día de inicio
        btn_dia = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@data-testid='departure-date-picker']/div/div/div[2]/div/div/div/div[2]/div/div[2]/div[4]/div[6]")))
        btn_dia.click()
        
        # Botón día de fin
        todos_los_dias = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="odf-calendar-day odf-calendar-day-weekend"]')))
        i=0
        encontrado = False
        while i < len(todos_los_dias) and not encontrado:
            if todos_los_dias[i].text == "18":
                encontrado = True
            else:
                i +=1 
        btn_dia_fin = todos_los_dias[i]
        btn_dia_fin.click()

        print("Fechas seleccionadas con éxito")

    except Exception as e:
        print(f"Error al seleccionar fechas {e}")

def seleccionar_adulto(driver):
    """
    funcion para elegir que solo viaja un adulto
    :param driver:
    :return:
    """
    try:
        #presionar botón desplegable de adultos y habitaciones
        btn_adult = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@data-testid='room-pax-selector-summary']")))
        btn_adult.click()

        #presionar botón según el número de adultos querido, en este caso 1
        btn_uno = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='pax-selector-item']/div[2]/div/div/button[@data-testid='decrease-picker']")))
        btn_uno.click()

        btn_done=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='odf-btn odf-btn-sm odf-btn-secondary odf-col-span12 prisma-btn prisma-btn-highlight prisma-btn-round']")))
        btn_done.click()
        print("Viajeros seleccionados con éxtio")
    except Exception as e:
        print(f"Error al seleccionar adultos {e}")

def search(driver):
    """
    Función que pulsa el botón de busar
    """
    try:
        btn_search=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@test-id='search-hotel-standalone-btn']")))
        btn_search.click()
        print("Búsqueda realizada con éxito")
    except Exception as e:
        print(f"error al search")

def dismissDiscounts(driver):
    """
    Función que cierra el panel de propaganda 
    """
    try:
        btn_dismiss = WebDriverWait(driver,15).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="css-17q5jfm e139ouyt2"]')))
        btn_dismiss.click()
        print("Propaganda cerrada con éxito")
    except Exception as e:
        print(f"Error al cerrar la propaganda: {e}")

def cargar_mas_resultados(driver):
    """
    Funcion que le da al boton de siguiente pagina,
    si no está es que ya no hay mas resultado por lo que devuelve False
    """
    try:
        # Buscamos el botón por el texto "See more hotels"
        btn_siguiente = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Next page"]'))
        )
        btn_siguiente.click()
        print("Botón de siguiente pagina presionado")
        return True
    except Exception:
        # Si no se encuentra el botón o no es clickable, asumimos que no hay más resultados
        return False

#-------------Fin scraping dincamico------------------------------------

def sacarHtmlEstático(driver):
    """
    Función que saca el Html de la pagina estatica a scrapear
    """
    WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH, "//html"))) #Esperar a que cargue todo
    WebDriverWait(driver,40).until(EC.presence_of_all_elements_located((By.XPATH, '//div')))
    time.sleep(3)
    

    #Coge la primera altura del html, es decir, la altura inicial sin hacer scroll down
    ult_altura = driver.execute_script("return document.body.scrollHeight")
    
    #Hacer todo el scroll down
    fin = False
    while not fin:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(3)

        altura = driver.execute_script("return document.body.scrollHeight")
        if altura == ult_altura:
            fin = True
        ult_altura = altura

    html_estatico = driver.page_source
    soup = BeautifulSoup(html_estatico, "html.parser")

    print("Html obtenido con éxito")
    return soup

#-------------Inicio scraping estático-------------------------------------

def sacarInfoHotel(soup):
    resultado = []
    try:
        # se usa data testid (como en booking) porque las clases de cada bloque de info son diferentes algunas 
        hotel_data = soup.find_all("div", attrs={"data-testid": True})
        # todas empiezan igual pero luego tienen un numero por eso busco por lo que empieza no por el data testid como tal 
        hotel_data = [h for h in hotel_data if "e2e-accommodation-item-" in h["data-testid"]]

        for hd in hotel_data:
          
            nodo_nom = hd.find("div", class_=["css-1kr9ao9", "e1hue9ey0"])
            h_nombre = nodo_nom.text if nodo_nom else "N/A"

            nodo_rate = hd.find("div", class_=["css-ap40a3"])
            if nodo_rate:
                texto_rate = nodo_rate.text
                # para dejar solo numeros y el decimal
                h_rate = ""
                for caracter in texto_rate:
                    if caracter.isdigit() or caracter == ".":
                        h_rate = h_rate + caracter
                if h_rate == "":
                    h_rate = "N/A"
            else:
                h_rate = "N/A"


            try:
                nodo_price = hd.find("span", class_=["css-1vtqrtx", "e139ay0z0"])
                if nodo_price:
                    h_price = nodo_price.text
                else:
                    raise Exception
            except Exception:
                nodo_price= hd.find("div", attrs={"data-testid":"striked-price"})
                if nodo_price:
                    h_price = nodo_price.text
                else:
                    h_price = np.nan

            cont_est = hd.find("div", class_=["css-1szo4kn", "e17fzqxg0"])
            h_estrellas = len(cont_est.find_all(class_=["css-lbmci7"])) if cont_est else 0

        
            nodo_dir = hd.find("div", class_=["css-9xspy4"])
            h_direccion = nodo_dir.text if nodo_dir else "N/A"

         
            if h_nombre != "N/A":
                resultado.append(
                    h_nombre + ";" + h_rate + ";" + h_price + ";" + str(h_estrellas) + ";" + h_direccion
                )

        return resultado

    except Exception as e:
        print(f"Fallo al conseguir la info de prueba {e}")
        return []  



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

#-----------------Fin del scraping estático----------------------------------------------

def ejecutar_script_edreams(lugar, nom_csv):
    #Scraping dinámico
    driver = iniciar_navegador()
    aceptarCookies(driver)
    cerrarLogin(driver)
    pulsar_hotels(driver)
    seleccionarLugar(driver, lugar)
    seleccionarFechas(driver)
    seleccionar_adulto(driver)
    search(driver)
    dismissDiscounts(driver)


    #Sacar html estático
    soup = sacarHtmlEstático(driver)
    lista_resultado = sacarInfoHotel(soup)

    while cargar_mas_resultados(driver):
        soup = sacarHtmlEstático(driver)
        list_temp = sacarInfoHotel(soup)
        for e in list_temp:
            lista_resultado.append(e)

    
    
    guardar_en_csv(lista_resultado, nom_csv)

    driver.quit()


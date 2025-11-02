from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import re
import time

EDREAMS = "Edreams"

#----------------------------Inicio scraping dinámico-----------------------------------
def iniciar_navegador(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
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
    funcion para elegir las fechas, que serán del 7 al 8 de enero
    """
    try:

        #Seleccionar botón fecha
        btn_fecha_inicio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='departure-date-picker']/div/div/div/input")))
        btn_fecha_inicio.click()

        #Seleccionar pasar mes
        btn_pasar_mes=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='departure-date-picker']/div/div/div[2]/div/div/div/div[4]/button")))
        btn_pasar_mes.click()
        btn_pasar_mes.click()

        #Botón día de inicio
        btn_dia = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@data-testid='departure-date-picker']/div/div/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[3]")))
        btn_dia.click()

        # Botón día de fin
        todos_los_dias = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "odf-calendar-day")))
        i=0
        encontrado = False
        while i < len(todos_los_dias) and not encontrado:
            if todos_los_dias[i].text == "8":
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

#-------------Fin scraping dincamico------------------------------------

def sacarHtmlEstático(driver):
    """
    Función que saca el Html de la pagina estatica a scrapear
    """
    WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, "//body"))) #Esperar a que cargue todo
    WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, "//html")))
    time.sleep(2)
    html_estatico = driver.page_source
    soup = BeautifulSoup(html_estatico, "html.parser")
    return soup

#-------------Inicio scraping estático-------------------------------------

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
        with open(f"../csv/{nombre_archivo}", 'w', newline='', encoding='utf-8') as archivo_csv:
            escritor = csv.writer(archivo_csv, delimiter=';')
            escritor.writerow(cabeceras)
            for linea_datos in datos_hoteles:
                fila_lista = linea_datos.split(';')
                escritor.writerow(fila_lista)

        print(f"¡Datos guardados exitosamente en '{nombre_archivo}'!")

    except IOError as e:
        print(f" Error al escribir el archivo CSV: {e}")

#-----------------Fin del scraping estático----------------------------------------------

def ejecutar_script_edreams(url, lugar, nom_csv):
    #Scraping dinámico
    driver = iniciar_navegador(url)
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
    
    #Scraping estático y guardado en csv
    lista_resultado = sacarInfoHotel(soup)
    guardar_en_csv(lista_resultado, nom_csv)


    input("Pulsa para salir")
    driver.quit()
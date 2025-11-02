from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import time

AMIMIR = "Amimir"

def iniciar_navegador():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.amimir.com/es/")
    return driver


def aceptarCookies(driver):
    '''
    Función que acepta las cookies de Amimir
    '''
    try:
        btn_accpt_cookies = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[2]/a")))
        btn_accpt_cookies.click()
        print("Cookies aceptadas con éxito")
    except Exception as e:
        print(f"Error al aceptar cookies: {e}")


def seleccionarLugar(driver, lugar):
    '''
    Función que escribe en el buscador un lugar
    '''
    try:
        # Esperar y enfocar el input
        input_buscador = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='mainsearch-xs']//div[1]//div[2]/form/div//div[3]/div/span/input"))
        )
        input_buscador.send_keys(lugar)

    except Exception as e:
        print(f"Error al introducir destino: {e}")


def seleccionarFechas(driver):
    """
    funcion para elegir las fechas, que serán del 7 al 8 de enero
    """
    try:
        # Presionar el boton de las fechas
        btn_fecha = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "start-date-text")))
        btn_fecha.click()
        # pasar de mes
        btn_flecha = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//i[@class='fa fa-lg fa-chevron-right']")))
        btn_flecha.click()
        btn_flecha.click()
        # seleccionar fecha de inicio
        btn_dia_inicio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='Enero 7, 2026']")))
        btn_dia_inicio.click()
        #seleccionar la fecha de fin
        btn_dia_fin = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='Enero 8, 2026']")))
        btn_dia_fin.click()

        # aceptar fechas
        btn_acept = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='vpt-btn vpt-btn-complementary']")))
        btn_acept.click()
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
            (By.XPATH, "//div[@id='dropdown-search-rooms']//div[@data-container='dropdown-button']/div")))
        btn_adult.click()
        #presionar botón de número de adultos
        btn_ch = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//select[@id='book-hab-1-adults']")))
        btn_ch.click()
        #presionar botón según el número de adultos querido, en este caso 1
        btn_uno = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//select[@id='book-hab-1-adults']/option[1]")))
        btn_uno.click()
    except Exception as e:
        print(f"Error al seleccionar adultos {e}")


def boton_buscar(driver):
    """
    funcion para empezar la búsqueda
    :param driver:
    :return:
    """
    try:
        btn_buscar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='col-xs-12 col-lg-2 col-md-2  mainsearch-formblockl']/button")))
        btn_buscar.click()
    except Exception as e:
        print(f"Error al pulsar buscar {e}")

# ------------------------Fin scraping dinámico---------------------------------------------
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
# ------------------------Inicio scrapping estático---------------------------------------------
def sacarInfoHotel(soup):
    """
    Funcion que saca el nombre del primer hotel
    """
    result = []
    try:
        hotel_data = soup.findAll(name="div", attrs={"class":"hotel-data-container"})
        for hd in hotel_data:
            h_nombre = hd.find(name="div", attrs={"class":"hotel-name"}).text
            h_rate = hd.find(name="span", attrs={"class":"hotel-rate"}).text
            h_price = hd.find(name="div", attrs={"class": "hotel-price"}).text
            h_estrellas = len(hd.findAll(name="i", attrs={"class": "ci-star"}))
            """if h_estrellas == 0:"""
            h_llaves = len(hd.findAll(name="i", attrs={"class": "ci-key"}))
            icono = hd.find(name="i", attrs={"class": "ci ci-map-icon ci-s-12"})
            h_direccion = "N/A"  # Valor por defecto

            if icono:
                direccion_texto = icono.next_sibling
                if direccion_texto:
                    h_direccion = direccion_texto.strip().replace('"', '')

            if len(h_nombre) > 0:
                result.append(h_nombre + ";" + h_rate + ";" + h_price + ";" + str(h_estrellas) + " estrellas" + ";" + str(h_llaves) + " llaves" + ";" + h_direccion)
        print("Scraping estático realizado con éxtio")
        return result
    except Exception as e:
        print(f"Fallo al conseguir la info de prueba {e}")
        return []

def guardar_en_csv(datos_hoteles, nombre_archivo='hoteles_extraidos_amimir.csv'):
    cabeceras = ['Nombre', 'Puntuación', 'Precio', 'Estrellas', 'Llaves', 'Direccion']
    try:
        with open(f"csv/{nombre_archivo}", 'w', newline='', encoding='utf-8') as archivo_csv:
            escritor = csv.writer(archivo_csv, delimiter=';')
            escritor.writerow(cabeceras)
            for linea_datos in datos_hoteles:
                fila_lista = linea_datos.split(';')
                escritor.writerow(fila_lista)

        print(f"¡Datos guardados exitosamente en '{nombre_archivo}'!")

    except IOError as e:
        print(f" Error al escribir el archivo CSV: {e}")

# ------------------------Fin scraping estático---------------------------------------------
def ejecutar_script_amimir(lugar, nom_csv):
    #Parte dinámica
    driver = iniciar_navegador()
    aceptarCookies(driver)
    seleccionarLugar(driver, lugar)
    seleccionarFechas(driver)
    seleccionar_adulto(driver)
    boton_buscar(driver)
    
    #Parte estática
    soup_final = sacarHtmlEstático(driver)
    lista_datos = sacarInfoHotel(soup_final)
    guardar_en_csv(lista_datos, nom_csv)
    driver.quit()
    
    

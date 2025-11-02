from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


#----------------------Inicio Scraping Dinámico-----------------------------------

def iniciarNavegador(url):
    '''
    Función que inicializa el navegador, en este caso
    Google Chrome, con unas opciones específicas.
    '''
    #Opciones del navegador
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    return driver

def cerrarLogin(driver):
    '''
    Función que cierra el popup del login
    '''
    try:
        cerrar_login = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Ignorar información sobre el inicio de sesión.']")))
        cerrar_login.click()
        print("Login cerrado con éxito")
    except Exception as e:
        pass #Hay veces que no salta el login

def aceptarCookies(driver):
    '''
    Función que acepta las cookies de Booking
    '''
    try:
        btn_accpt_cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        btn_accpt_cookies.click()
        print("Cookies acceptadas con éxito")
    except Exception as e:
        print(f"Error al aceptar cookies: {e}")

        
def seleccionarLugar(driver, lugar):
    '''
    Función que escribe en el buscador de Maps un lugar
    '''
    try:
        input_buscador = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, ":rh:")))
        input_buscador.send_keys(lugar)#Introduce el texto en el buscador
        print("Búsqueda de lugar realizada con éxito")
    except Exception as e:
        print(f"Error al seleccionar lugar: {e}")

def seleccionarFechas(driver):
    """
    Función que selecciona las fechas del 7 al 8 de enero
    """
    try:
        #Presionar el boton de las fechas
        btn_fechas = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='searchbox-dates-container']")))
        btn_fechas.click()

        #Presionar el boton de mes siguiente
        btn_siguiente_mes = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Mes siquiente']")))
        btn_siguiente_mes.click()
        btn_siguiente_mes.click()

        #Presionar seleccionar 7 de enero
        btn_7_enero = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='Mi 7 enero 2026']")))
        btn_7_enero.click()

        #Presionar seleccionar 8 de enero
        btn_8_enero = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='Ju 8 enero 2026']")))
        btn_8_enero.click()


        print("Fechas Seleccionadas con éxito")
    except Exception as e:
        print(f"Error al seleccionar las fechas: {e}")

def seleccionarViajeros(driver):
    """
    Función que selecciona el número de viajeros
    """
    try:
        #Abrir menú de viajeros
        btn_viajeros = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='occupancy-config']")))
        btn_viajeros.click()

        #Seleccionar 1 viajero
        btn_1_viajero = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='a9669463b9']//div[1]/div[@class='e301a14002']/button")))
        btn_1_viajero.click()

        #Darle a listo
        btn_listo = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='f766b6b016 aad29c76fe']/button[@class='de576f5064 b46cd7aad7 d0a01e3d83 c7a901b0e7 e4f9ca4b0c bbf83acb81 d1babacfe0 a9d40b8d51']")))
        btn_listo.click()

        print("Viajeros seleccionados con éxito")
    except Exception as e:
        print(f"Error al seleccionar viajeros {e}")

def buscar(driver):
    """
    Función que busca y presiona el botón de buscar
    """
    try:
        #Presionar el boton de buscar
        btn_buscar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='de576f5064 b46cd7aad7 ced67027e5 dda427e6b5 e4f9ca4b0c ca8e0b9533 cfd71fb584 a9d40b8d51']")))
        btn_buscar.click()
        print("Botón de buscar presionado con éxito")
        return driver
    except Exception as e:
        print(f"Error al darle a buscar {e}")


#------------------------Fin scraping dinámico------------------------------------------------

def sacarHtmlEstático(driver):
    """
    Función que saca el Html de la pagina estatica a scrapear
    """
    WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, "//div"))) #Esperar a que cargue todo
    WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, "//html")))
    html_estatico = driver.page_source
    soup = BeautifulSoup(html_estatico, "html.parser")
    return soup

#------------------------Inicio scraping estático---------------------------------------------

def sacarInfoHoteles(soup):
    """
    Funcion que va a sacar la informacion de los hoteles necesaria
    """
    resultado = []
    try:
        datos_hoteles = soup.find_all(name="div", attrs={"class":"aa97d6032f"})
        for dh in datos_hoteles:
            #nombre del hotel y la excepcion si no encuentra nada
            nom_hot = dh.find("div", class_=["b87c397a13", "a3e0b4ffd1"])
            nombre_hotel = nom_hot.text.strip() if nom_hot else "N/A"

            # como booking  en algunos elemntos contiene dos clases o mas dentro (<div class="f63b14ab7a dff2e52086">) BeautifulSoup lo lee como una sola clase con un espacio dentro (qe no existe en html) por eso hay que ponerlas como una lista para que puedan ser leidas
            valor_hot = dh.find("div", class_=["f63b14ab7a", "dff2e52086"])
            valoracion_hotel = valor_hot.text.strip() if valor_hot else "N/A"

            # aqui uso un data testid porque al ser booking un html dinamico las clases son bastante insetables, y por eso con el metodo de antes me devolvia de nuevo el nombre del hotel. Usando data-testid se concreta mas y me resolvio el problema
            pre_hot = dh.find(attrs={"data-testid": "price-and-discounted-price"})
            precio_hotel = pre_hot.get_text() if pre_hot else "N/A"

            #comome ha fucnionado bien, repito el metdoo para la ubicacion
            ubi_hot = dh.find("span", class_=["d823fbbeed", "f9b3563dd4"])
            ubicacion_hotel = ubi_hot.text.strip() if ubi_hot else "N/A"

            cont_est = dh.find("div", class_="b5ab46c480")
            num_estrellas = len(cont_est.find_all(class_="e03979cfad")) if cont_est else 0



    
            if nombre_hotel != "N/A":
                linea = (
                    nombre_hotel + ";" +
                    (valoracion_hotel if valoracion_hotel else "N/A") + ";" +
                    (precio_hotel if precio_hotel else "N/A") + ";" +
                    f"{num_estrellas}" + ";" + 
                    (ubicacion_hotel if ubicacion_hotel else "N/A")
                )
                resultado.append(linea)

        return resultado

    except Exception as e:
        print(f"Fallo al conseguir la info de prueba {e}")
        return []


#------------------------Fin scraping estático------------------------------------------------
def ejecutar_script(url, lugar):
    #Inicio scraping dinámico
    driver = iniciarNavegador(url)
    cerrarLogin(driver)
    aceptarCookies(driver)
    seleccionarLugar(driver, lugar)
    seleccionarFechas(driver)
    seleccionarViajeros(driver)
    buscar(driver)

    #Sacar el html estatico
    soup = sacarHtmlEstático(driver)

    #Inicio del scraping estático
    lista_hoteles = sacarInfoHoteles(soup)
    print("Número de hoteles encontrados:", len(lista_hoteles))
    print("Primeros resultados:")
    for fila in lista_hoteles[:3]:
        print(fila)

    #Esto esta para poder ver la pagina mientras programamos, luego hay que quitar el input y poner el driver.quit justo despues de soup
    input("Pulsa cualquier tecla para cerrar el navegador ")
    driver.quit()
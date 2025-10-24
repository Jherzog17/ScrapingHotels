from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
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

def cerrarLogin():
    '''
    Función que cierra el popup del login
    '''
    try:
        cerrar_login = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Ignorar información sobre el inicio de sesión.']")))
        cerrar_login.click()
        print("Login cerrado con éxito")
    except Exception as e:
        pass #Hay veces que no salta el login

def aceptarCookies():
    '''
    Función que acepta las cookies de Booking
    '''
    try:
        btn_accpt_cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        btn_accpt_cookies.click()
        print("Cookies acceptadas con éxito")
    except Exception as e:
        print(f"Error al aceptar cookies: {e}")

        
def seleccionarLugar(lugar):
    '''
    Función que escribe en el buscador de Maps un lugar
    '''
    try:
        input_buscador = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, ":rh:")))
        input_buscador.send_keys(lugar)#Introduce el texto en el buscador
        print("Búsqueda de lugar realizada con éxito")
    except Exception as e:
        print(f"Error al seleccionar lugar: {e}")

def seleccionarFechas():
    """
    Función que selecciona las fechas del 16 al 17 de enero
    """
    try:
        #Presionar el boton de las fechas
        btn_fechas = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='searchbox-dates-container']")))
        btn_fechas.click()

        #Presionar el boton de las fechas flexibles
        btn_fechas_flexibles = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "flexible-searchboxdatepicker-tab-trigger")))
        btn_fechas_flexibles.click()

        #Seleccionar boton de otro
        input_otro = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "//fieldset[@class='b99b6ef58f a10a015434']/div//div[4]")))
        input_otro.click()

        #Seleccionar enero
        input_enero = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//fieldset[@class='fd8258f8a6']/div//div[1]//div[4]/label")))
        input_enero.click()

        #Presionar seleccionar fechas
        btn_sel_fechas = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='d810db075c']//button")))
        btn_sel_fechas.click()


        print("Fechas Seleccionadas con éxito")
    except Exception as e:
        print(f"Error al seleccionar las fechas: {e}")

def seleccionarViajeros():
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

def buscar():
    """
    Función que busca y presiona el botón de buscar
    """
    try:
        #Presionar el boton de buscar
        btn_buscar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='de576f5064 b46cd7aad7 ced67027e5 dda427e6b5 e4f9ca4b0c ca8e0b9533 cfd71fb584 a9d40b8d51']")))
        btn_buscar.click()
        print("Botón de buscar presionado con éxito")
    except Exception as e:
        print(f"Error al darle a buscar {e}")

def seleccionarSoloHoteles():
    """
    Función que selecciona los alojamientos que sean hoteles, hostales o albergues
    """
    try:
        input_hoteles = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='b7ef425131 e9f1adff2b ba5aaf262f bfb55afbed']")))
        print(len(input_hoteles))
        
        print("Opoción de hoteles seleccionada con éxito")
    except Exception as e:
        print(f"Error al seleccionar la opción de hoteles {e}")


#------------------------Fin scraping dinámico------------------------------------------------

#Parametros ajustables
url = "https://www.booking.com"
lugar = "Ibiza"

#Secuencia de ejecución
driver = iniciarNavegador(url)
cerrarLogin()
aceptarCookies()
seleccionarLugar(lugar)
seleccionarFechas()
seleccionarViajeros()
buscar()
seleccionarSoloHoteles()
input("Hola mundo ")
driver.quit()
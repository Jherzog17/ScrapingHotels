from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import time


def iniciar_navegador(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")

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
        print("Cookies acceptadas con éxito")
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
        pass #Hay veces que no salta el login

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

    except Exception as e:
        print(f"Error al introducir destino: {e}")

def seleccionarFechas(driver):
    """
    funcion para elegir las fechas, que serán del 7 al 8 de enero
    """
    try:

        # seleccionar fecha de inicio
        btn_fecha_inicio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='departure-date-picker']/div/div/div/input")))
        btn_fecha_inicio.click()

        btn_pasar_mes=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='departure-date-picker']/div/div/div[2]/div/div/div/div[4]/button")))
        btn_pasar_mes.click()
        btn_pasar_mes.click()

        btn_dia = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@data-testid='departure-date-picker']/div/div/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[3]")))
        btn_dia.click()
        btn_dia.click()

        # seleccionar fecha de fin
        btn_fecha_fin = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='return-date-picker']/div/div/div//input")))
        btn_fecha_fin.click()

        btn_dia_f = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH,
             "//div[@data-testid='return-date-picker']/div/div/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[4]")))
        btn_dia_f.click()
        btn_dia_f.click()

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
    except Exception as e:
        print(f"Error al seleccionar adultos {e}")

def search(driver):
    try:
        btn_search=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@test-id='search-hotel-standalone-btn']")))
        btn_search.click()
    except Exception as e:
        print(f"error al search")

def ejecutar_script(url, lugar):
    driver = iniciar_navegador(url)
    aceptarCookies(driver)
    cerrarLogin(driver)
    pulsar_hotels(driver)
    seleccionarLugar(driver, lugar)
    seleccionarFechas(driver)
    seleccionar_adulto(driver)
    search(driver)
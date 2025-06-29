import time
import os
import json
from collections import deque
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException, NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth

# --- NUEVA LIBRERÍA PARA COLORES ---
import colorama
from colorama import Fore, Style

# --- DEFINICIÓN DE COLORES ---
C_INFO = Fore.CYAN
C_SUCCESS = Fore.GREEN
C_ERROR = Fore.RED
C_PROMPT = Fore.MAGENTA
C_BANNER = Fore.GREEN
C_AUTHOR = Fore.YELLOW
C_RESET = Style.RESET_ALL

def imprimir_banner():
    banner = r"""
        ██╗     ███████╗    ███╗   ███╗██╗   ██╗    ██╗  ██╗███████╗███████╗
        ██║     ██╔════╝    ████╗ ████║╚██╗ ██╔╝    ╚██╗██╔╝██╔════╝██╔════╝
        ██║     █████╗      ██╔████╔██║ ╚████╔╝      ╚███╔╝ ███████╗███████╗
        ██║     ██╔══╝      ██║╚██╔╝██║  ╚██╔╝       ██╔██╗ ╚════██║╚════██║
        ███████╗██║         ██║ ╚═╝ ██║   ██║       ██╔╝ ██╗███████║███████║
        ╚══════╝╚═╝         ╚═╝     ╚═╝   ╚═╝       ╚═╝  ╚═╝╚══════╝╚══════╝
                                                                 
    """
    print(f"{C_BANNER}{banner}{C_RESET}")
    print(f"{C_AUTHOR}{Style.BRIGHT}                        Code By ss3k{C_RESET}\n")

def xss_hunter_pro():
    nombre_archivo = ""
    while True:
        nombre_archivo = input(f"{C_PROMPT}Introduce el nombre del archivo que contiene las URLs base (ej: urls.txt): {C_RESET}")
        if os.path.exists(nombre_archivo):
            break
        else:
            print(f"{C_ERROR}Error: El archivo '{nombre_archivo}' no fue encontrado.{C_RESET}")
            
    codigo_a_buscar = input(f"{C_PROMPT}Introduce el código o texto exacto que deseas buscar: {C_RESET}")
    profundidad_max = 0
    while True:
        try:
            profundidad_max = int(input(f"{C_PROMPT}Introduce la profundidad de rastreo (1-5, o 0 para no rastrear): {C_RESET}"))
            if 0 <= profundidad_max <= 5:
                break
            else:
                print(f"{C_ERROR}Por favor, introduce un número entre 0 y 5.{C_RESET}")
        except ValueError:
            print(f"{C_ERROR}Entrada no válida. Introduce un número.{C_RESET}")
            
    cookies_list = []
    usar_cookies = input(f"{C_PROMPT}¿Deseas usar cookies de sesión? (s/n): {C_RESET}").lower()
    if usar_cookies in ['s', 'si', 'y', 'yes']:
        ruta_archivo_cookies = ""
        while True:
            ruta_archivo_cookies = input(f"{C_PROMPT}Introduce la ruta al archivo de cookies JSON (ej: cookie.json): {C_RESET}")
            if os.path.exists(ruta_archivo_cookies):
                break
            else:
                print(f"{C_ERROR}Error: El archivo '{ruta_archivo_cookies}' no fue encontrado. Inténtalo de nuevo.{C_RESET}")
        try:
            with open(ruta_archivo_cookies, 'r', encoding='utf-8') as f:
                cookies_list = json.load(f)
            print(f"{C_SUCCESS}Archivo de cookies leído correctamente. Se encontraron {len(cookies_list)} cookies.{C_RESET}")
        except json.JSONDecodeError:
            print(f"{C_ERROR}Error: El contenido de '{ruta_archivo_cookies}' no es un JSON válido.{C_RESET}")
        except Exception as e:
            print(f"{C_ERROR}Ocurrió un error inesperado al leer el archivo de cookies: {e}{C_RESET}")

    print("\n" + f"{C_INFO}="*50)
    print(f"Iniciando XSS Hunter en modo ASISTIDO...")
    print(f"="*50 + f"{C_RESET}\n")

    try:
        with open(nombre_archivo, 'r') as f:
            urls_base = [linea.strip() for linea in f if linea.strip()]
    except Exception as e:
        print(f"{C_ERROR}Error crítico al leer el archivo: {e}{C_RESET}")
        return

    busqueda_terminada = False

    for url_inicial in urls_base:
        if busqueda_terminada:
            break

        dominio_base = urlparse(f"https://{url_inicial.replace('http://', '').replace('https://', '')}").netloc
        print(f"\n{C_AUTHOR}--- Iniciando rastreo para el dominio: {dominio_base} ---{C_RESET}")

        driver = None
        try:
            options = ChromeOptions()
            options.add_argument("start-maximized")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            driver = webdriver.Chrome(options=options)
            stealth(driver, languages=["es-ES", "es"], vendor="Google Inc.", platform="Win32", webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True)
            
            print(f"{C_INFO}Navegador iniciado. Cargando cookies...{C_RESET}")
            driver.get(f"https://{dominio_base}") 
            for cookie in cookies_list:
                try:
                    if 'name' in cookie and 'value' in cookie:
                        driver.add_cookie(cookie)
                except Exception:
                    pass
            print(f"{C_INFO}Cookies cargadas. Refrescando página...{C_RESET}")
            driver.refresh() 

            print("\n" + f"{C_PROMPT}#"*60)
            print("### OPCIONAL ###")
            print(f"En caso de existir un desafío WAF, puedes completarlo ahora '{dominio_base}'.")
            input("Una vez resuelto, vuelve a esta terminal y PRESIONA ENTER para continuar el rastreo...")
            print("### REANUDANDO SCRIPT ###")
            print("#"*60 + f"{C_RESET}\n")

            cola = deque()
            urls_visitadas = set()
            urls_iniciales_para_la_cola = [driver.current_url]
            url_normalizada = url_inicial
            if not url_normalizada.startswith('http'):
                url_normalizada = f"https://{url_normalizada}"
            if urlparse(url_normalizada).path not in ('', '/'):
                urls_iniciales_para_la_cola.append(url_normalizada)
            
            for url in urls_iniciales_para_la_cola:
                if url not in urls_visitadas:
                    cola.append((url, 0))
                    urls_visitadas.add(url)
            
            while cola and not busqueda_terminada:
                url_actual, profundidad_actual = cola.popleft()
                print(f"[{profundidad_actual}] Procesando: {url_actual}")
                try:
                    driver.get(url_actual)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                    
                    try:
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert_text = alert.text
                        alert.accept()
                        print("\n" + f"{C_SUCCESS}{Style.BRIGHT}!"*60)
                        print(f"    ¡¡¡ ÉXITO: XSS EJECUTADO !!! Se detectó un pop-up en: {url_actual}")
                        print(f"    Texto del pop-up: '{alert_text}'")
                        print("!"*60 + f"{C_RESET}\n")
                        continuar = input(f"{C_PROMPT}¿Deseas continuar buscando? (s/n): {C_RESET}").lower()
                        if continuar not in ['s', 'si', 'y', 'yes']:
                            busqueda_terminada = True
                    except TimeoutException:
                        pass
                    
                    if busqueda_terminada: continue

                    html_final = driver.page_source
                    if codigo_a_buscar in html_final:
                        print("\n" + f"{C_SUCCESS}{Style.BRIGHT}*"*60)
                        print(f"    ¡¡¡ ÉXITO: XSS REFLEJADO !!! Código encontrado como texto en: {url_actual}")
                        print("*"*60 + f"{C_RESET}\n")
                        continuar = input(f"{C_PROMPT}¿Deseas continuar buscando? (s/n): {C_RESET}").lower()
                        if continuar not in ['s', 'si', 'y', 'yes']:
                            busqueda_terminada = True
                    else:
                        print(f"    -> {C_ERROR}FALLO. No se encontró el código como texto.{C_RESET}")
                    
                    if profundidad_actual < profundidad_max and not busqueda_terminada:
                        soup = BeautifulSoup(html_final, 'lxml')
                        for link in soup.find_all('a', href=True):
                            url_nueva = urljoin(url_actual, link['href'])
                            url_nueva = urlparse(url_nueva)._replace(query='', fragment='').geturl()
                            if urlparse(url_nueva).netloc.endswith(dominio_base) and url_nueva not in urls_visitadas:
                                urls_visitadas.add(url_nueva)
                                cola.append((url_nueva, profundidad_actual + 1))
                except Exception as e:
                    print(f"    -> {C_ERROR}ERROR al procesar la página: {e}{C_RESET}")
        
        finally:
            if driver:
                driver.quit()

    print(f"\n{C_INFO}Búsqueda finalizada.{C_RESET}")

if __name__ == "__main__":
    colorama.init(autoreset=True)
    imprimir_banner()
    xss_hunter_pro()
    colorama.deinit()
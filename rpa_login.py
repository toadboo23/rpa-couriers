from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


def get_latest_file(download_dir):
    files = [os.path.join(download_dir, f) for f in os.listdir(download_dir) if os.path.isfile(os.path.join(download_dir, f))]
    if not files:
        return None
    return max(files, key=os.path.getctime)


def rename_file_with_timestamp(file_path):
    """
    Renombra el archivo agregando la hora actual en formato HH-MM-SS antes de la extensión.
    Ejemplo: archivo.csv -> archivo_10-30-45.csv
    """
    if not file_path or not os.path.exists(file_path):
        return None
    
    # Obtener la hora actual en formato HH-MM-SS
    current_time = datetime.now().strftime("%H-%M-%S")
    
    # Separar nombre y extensión
    file_dir = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    name, ext = os.path.splitext(file_name)
    
    # Crear nuevo nombre con timestamp
    new_name = f"{name}_{current_time}{ext}"
    new_path = os.path.join(file_dir, new_name)
    
    # Renombrar el archivo
    try:
        os.rename(file_path, new_path)
        print(f"[RPA] Archivo renombrado: {file_name} -> {new_name}")
        return new_path
    except Exception as e:
        print(f"[RPA] Error al renombrar archivo: {e}")
        return file_path


def login_glovo(email: str, password: str) -> str:
    """
    Automatiza el login en https://fleet.glovoapp.com/login usando Selenium.
    Luego hace clic en el menú 'Couriers', en el botón 'Download CSV' de la página y en el botón 'Download CSV' dentro de la ventana modal.
    Descarga el archivo en /downloads, lo renombra con timestamp y lo sube a la carpeta pública de SharePoint indicada.
    Devuelve un mensaje de éxito o error.
    """
    driver = None
    try:
        print("[RPA] Iniciando configuración de Selenium y carpeta de descargas...")
        download_dir = os.path.abspath("downloads")
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach', True)
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)
        print(f"[RPA] Carpeta de descargas: {download_dir}")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        wait = WebDriverWait(driver, 20)
        print("[RPA] Navegando a la página de login de Glovo Fleet...")
        driver.get('https://fleet.glovoapp.com/login')

        print("[RPA] Esperando campos de login...")
        time.sleep(2)
        email_input = driver.find_element(By.NAME, 'email')
        password_input = driver.find_element(By.NAME, 'password')

        print("[RPA] Ingresando credenciales...")
        email_input.clear()
        email_input.send_keys(email)
        password_input.clear()
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)

        print("[RPA] Esperando respuesta de login...")
        time.sleep(5)
        if 'login' in driver.current_url:
            print("[RPA] Error: No se pudo iniciar sesión. Verifica las credenciales.")
            return 'Error: No se pudo iniciar sesión. Verifica las credenciales.'

        print("[RPA] Login exitoso. Buscando menú lateral...")
        time.sleep(3)
        couriers_menu = driver.find_element(By.XPATH, "//span[contains(@class, 'side-menu__item-label') and text()='Couriers']")
        couriers_menu.click()

        print("[RPA] Esperando página de Couriers...")
        time.sleep(5)
        download_csv_btn = driver.find_element(By.XPATH, "//span[contains(@class, 'uds-button__content__label') and text()='Download CSV']")
        print("[RPA] Haciendo clic en 'Download CSV' (página principal)...")
        download_csv_btn.click()

        print("[RPA] Esperando ventana modal de descarga...")
        time.sleep(2)
        modal_download_btn = driver.find_element(By.XPATH, "//div[contains(@class, 'modal')]//span[contains(@class, 'uds-button__content__label') and text()='Download CSV']")
        print("[RPA] Haciendo clic en 'Download CSV' (modal)...")
        modal_download_btn.click()

        print(f"[RPA] Proceso de descarga finalizado. Archivo guardado en: {download_dir}")
        time.sleep(5)  # Espera extra para asegurar que el archivo se descargue
        latest_file = get_latest_file(download_dir)
        if not latest_file:
            print("[RPA] No se encontró archivo descargado para subir a SharePoint.")
            return 'Error: No se encontró archivo descargado.'
        print(f"[RPA] Último archivo descargado: {latest_file}")

        # Renombrar archivo con timestamp
        renamed_file = rename_file_with_timestamp(latest_file)
        if not renamed_file:
            print("[RPA] Error al renombrar el archivo.")
            return 'Error: No se pudo renombrar el archivo.'

        # --- SUBIDA A SHAREPOINT ---
        sharepoint_url = "https://consultingsallent-my.sharepoint.com/:f:/g/personal/nmartinez_solucioning_net/Eh0WmhGIq2tPsF5pN8SJXPEB2kEsn0oVZtftapuN0gJUEA?e=z6cXKf"
        print("[RPA] Abriendo nueva pestaña para SharePoint...")
        driver.execute_script(f"window.open('{sharepoint_url}', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        print("[RPA] Esperando carga de SharePoint...")
        time.sleep(8)

        # Click en 'Cargar'
        print("[RPA] Buscando y haciendo clic en 'Cargar'...")
        cargar_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'text_cb8e3e55') and text()='Cargar']")))
        cargar_btn.click()
        time.sleep(2)

        # Click en 'Archivos' en la modal
        print("[RPA] Buscando y haciendo clic en 'Archivos' en la modal...")
        archivos_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'ms-ContextualMenu-itemText') and text()='Archivos']")))
        archivos_btn.click()
        time.sleep(2)

        # Seleccionar archivo (input type=file)
        print("[RPA] Buscando input de archivos y subiendo el archivo...")
        file_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        file_input.send_keys(renamed_file)
        print("[RPA] Archivo enviado. Esperando confirmación de subida...")
        time.sleep(8)  # Espera para que la subida se complete

        print(f"[RPA] Archivo {os.path.basename(renamed_file)} subido exitosamente a SharePoint.")
        return f'Archivo descargado, renombrado y subido exitosamente a SharePoint: {os.path.basename(renamed_file)}'
    except Exception as e:
        print(f"[RPA] Error durante el proceso: {e}")
        return f'Error durante el proceso: {e}'
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
        print("[RPA] Ejecución finalizada. Cerrando script.")
        sys.exit(0)

if __name__ == "__main__":
    EMAIL = "hola@solucioning.net"
    PASSWORD = "Solucioning25+-."
    resultado = login_glovo(EMAIL, PASSWORD)
    print(f"[RPA] Resultado: {resultado}") 
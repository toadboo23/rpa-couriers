from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


def login_glovo(email: str, password: str) -> str:
    """
    Automatiza el login en https://fleet.glovoapp.com/login usando Selenium.
    Luego hace clic en el menú 'Couriers', en el botón 'Download CSV' de la página y en el botón 'Download CSV' dentro de la ventana modal.
    Descarga el archivo en /downloads.
    Devuelve un mensaje de éxito o error.
    """
    try:
        # Configurar carpeta de descargas
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
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get('https://fleet.glovoapp.com/login')

        # Esperar a que cargue el campo de email
        time.sleep(2)
        email_input = driver.find_element(By.NAME, 'email')
        password_input = driver.find_element(By.NAME, 'password')

        email_input.clear()
        email_input.send_keys(email)
        password_input.clear()
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)

        # Esperar a que procese el login
        time.sleep(5)
        if 'login' in driver.current_url:
            return 'Error: No se pudo iniciar sesión. Verifica las credenciales.'

        # Esperar a que cargue el menú lateral
        time.sleep(3)
        couriers_menu = driver.find_element(By.XPATH, "//span[contains(@class, 'side-menu__item-label') and text()='Couriers']")
        couriers_menu.click()

        # Esperar a que cargue la página de Couriers
        time.sleep(5)
        # Buscar el botón 'Download CSV' por su clase y texto en la página principal
        download_csv_btn = driver.find_element(By.XPATH, "//span[contains(@class, 'uds-button__content__label') and text()='Download CSV']")
        download_csv_btn.click()

        # Esperar a que se abra la ventana modal
        time.sleep(2)
        # Buscar el botón 'Download CSV' dentro de la modal
        modal_download_btn = driver.find_element(By.XPATH, "//div[contains(@class, 'modal')]//span[contains(@class, 'uds-button__content__label') and text()='Download CSV']")
        modal_download_btn.click()

        return f'Inicio de sesión, clic en Couriers, descarga de CSV y descarga en modal realizados. Archivo guardado en: {download_dir}'
    except Exception as e:
        return f'Error durante el proceso: {e}' 
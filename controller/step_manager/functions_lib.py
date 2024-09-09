import platform
from controller.settings import env
import os, subprocess
import requests
from controller.step_manager.steps import StepManager
import time
from bs4 import BeautifulSoup


sm = StepManager()
OS_PLATFORM = platform.system()
VERSIONS=[]
IS_MINECRAFT_INSTALLED=False

def check_operative_system():
    """Identifica el sistema operativo que estas usando"""
    time.sleep(3)
    if OS_PLATFORM == 'Windows':
        if not os.path.isfile(os.path.join("./controller/chromedriver", "chromedriver")):
            sm.execute_manual_step("download_file_chromedriver", env.CHROMEDRIVER_PACKAGE_W64, env.DRIVER_PATH, env.DRIVER_NAME)
            print("Descargado")
    elif OS_PLATFORM == 'Linux':
        if not os.path.isfile(os.path.join("./controller/chromedriver", "chromedriver")):
            sm.execute_manual_step("download_file_chromedriver", env.CHROMEDRIVER_PACKAGE_LINUX, env.DRIVER_PATH, env.DRIVER_NAME)
    elif OS_PLATFORM == 'Darwin':
        if not os.path.isfile(os.path.join("./controller/chromedriver", "chromedriver")):
            sm.execute_manual_step("download_file_chromedriver", env.CHROMEDRIVER_PACKAGE_MACOS64, env.DRIVER_PATH, env.DRIVER_NAME)
    else:
        print(f"Estas usando un sistema operativo no identificado: {OS_PLATFORM}. La descarga no se ha podido realizar")

def download_file(url, save_dir, file_name):
    """Descarga un archivo para tu sistema operativo"""
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_path = os.path.join(save_dir, file_name)
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    except requests.RequestException as e:
        print(f"Error al descargar el archivo: {e}")
        
def download_file_chromedriver(url, save_dir, file_name):
    download_file(url, save_dir, file_name)
    
def download_file_minecraft_server(url, save_dir, file_name):
    download_file(url, save_dir, file_name)
    
def check_current_installation():
    required_files = ['server.jar']
    required_dirs = ['world'] 
    for file in required_files:
        if not os.path.isfile(os.path.join(env.SERVER_DIR, file)):
            print(f"Archivo requerido '{file}' no encontrado en {env.SERVER_DIR}")
            IS_MINECRAFT_INSTALLED=False
            return 
    for directory in required_dirs:
        if not os.path.isdir(os.path.join(env.SERVER_DIR, directory)):
            print(f"Directorio requerido '{directory}' no encontrado en {env.SERVER_DIR}")
            IS_MINECRAFT_INSTALLED=False
            return 
    print(f"Se encontró una instalación válida de Minecraft en {env.SERVER_DIR}")
    IS_MINECRAFT_INSTALLED=True

    
def get_minecraft_versions():
    response = requests.get('https://mcversions.net/')
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    h5 = soup.find('h5', string='Stable Releases')
    if h5:
        container = h5.find_parent('div')
    container.find_all('div')
    elements = container.find_all(attrs={"data-version": True})
    for element in elements:
        VERSIONS.append(element['data-version'])
    return VERSIONS

def download_minecraft_server(version="1.21.1"):
    if version in VERSIONS and not IS_MINECRAFT_INSTALLED:
        response = requests.get(_web_constructor(version))
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        h5 = soup.find('h5', string='Server Jar')
        if h5:
            container = h5.find_parent('div')
            a = container.find('a', attrs={"download": True})
        sm.execute_manual_step("download_file_minecraft_server", a['href'],env.SERVER_DIR, 'server.jar')
        sm.execute_manual_step("_first_time_execute_minecraft_server")
    else:
        return

def _web_constructor(version="1.21.1"):
    return f'https://mcversions.net/download/{version}'

def _first_time_execute_minecraft_server():
    os.chdir(env.SERVER_DIR)

    with open("eula.txt", 'w') as file:
        file.write("eula=true")

    server_process = subprocess.Popen(env.EXE_COMMAND, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        for line in server_process.stdout:
            if "Done" in line:
                print("Servidor Minecraft iniciado exitosamente.")
                break

        server_process.stdin.write("stop\n")
        server_process.stdin.flush()

        server_process.wait(timeout=30)

    except KeyboardInterrupt:
        print("Interrupción del teclado, deteniendo el servidor.")
        server_process.stdin.write("stop\n")
        server_process.stdin.flush()
        server_process.terminate()
        server_process.wait()

    except subprocess.TimeoutExpired:
        print("El servidor no se cerró a tiempo, forzando el cierre.")
        server_process.terminate()
        server_process.wait()

    finally:
        os.chdir("../")

def launch_cli():
    option = input("")
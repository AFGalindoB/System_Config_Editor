import os
from shutil import copy
import json

class ConfigurationManager:
    def __init__(self):
        self.root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.templates_path = os.path.join(self.root_path, "templates")

        self.config_path = os.path.join(self.root_path, "config")
        self.config_file_path = os.path.join(self.config_path, "config.json")

        self.backups_path = os.path.join(self.root_path, "backups")
        self.auto_backups_path = os.path.join(self.backups_path, "auto")
        self.manual_backups_path = os.path.join(self.backups_path, "manual")
    
def modify_config_json(config_file:dict) -> None:
    config_file_path = ConfigurationManager().config_file_path
    with open(config_file_path, "w") as f:
        json.dump(config_file, f, indent=4)

def setup_config() -> None:
    """ Verifica que la carpeta de configuraciones este disponible y los archivos de configuracion
    y si no es asi los genera a partir de los templates."""
    print("Revisando estado de las configuraciones...")

    paths = ConfigurationManager()

    # Crear las carpetas necesarias si no existen
    folders = [paths.config_path, paths.backups_path, paths.auto_backups_path, paths.manual_backups_path]
    for folder in folders:
        if not os.path.exists(folder):
            print("Creando carpeta:", folder)
            os.mkdir(folder)
     
    # Copiar archivos de templates a config si no existen
    for file in os.listdir(paths.templates_path):
        src = os.path.join(paths.templates_path, file)
        dst = os.path.join(paths.config_path, file)

        if not os.path.exists(dst):
            copy(src, dst)
            print("Archivo Creado:", dst)
    
    print("Configuraciones En Orden")

def load_config() -> dict:
    """ Carga el archivo de configuracion """
    paths = ConfigurationManager()
    with open(paths.config_file_path, "r") as f:
        config_data = json.load(f)
    return config_data

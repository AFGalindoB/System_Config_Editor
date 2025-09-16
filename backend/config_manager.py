import os
from shutil import copy
import json

class ConfigurationManager:
    def __init__(self):
        self.root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.templates_path = os.path.join(self.root_path, "templates")
        self.config_path = os.path.join(self.root_path, "config")
        self.config_file_path = os.path.join(self.config_path, "config.json")

def setup_config() -> None:
    """ Verifica que las configuraciones esten disponibles, si no es asi las crea """
    print("Revisando estado de las configuraciones...")

    paths = ConfigurationManager()

    # Crear carpeta config si no existe
    if not os.path.exists(paths.config_path):
        print("Preparando configuraciones...")
        os.mkdir(paths.config_path)
    
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

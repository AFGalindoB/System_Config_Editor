import os
from sys import exit as secure_exit
from shutil import copy, which
from cli_ui import advise, accept, select_option
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
    y si no es asi los genera a partir de los templates. A su vez revisa que las dependencias se
    encuentren en orden."""
    print("Revisando estado de las configuraciones...")

    paths = ConfigurationManager()

    # Crear las carpetas necesarias si no existen
    folders = [paths.config_path, paths.backups_path, paths.auto_backups_path, paths.manual_backups_path]
    for folder in folders:
        if not os.path.exists(folder):
            print("Creando carpeta:", folder)
            os.mkdir(folder)
    print("Carpetas en orden.")

    # Copiar archivos de templates a config si no existen
    for file in os.listdir(paths.templates_path):
        src = os.path.join(paths.templates_path, file)
        dst = os.path.join(paths.config_path, file)

        if not os.path.exists(dst):
            copy(src, dst)
            print("Archivo Creado:", dst)
    print("Archivos de configuracion en orden.")

    # Verificar dependencias del sistema
    if which("nano") is None:
        advise("Ups! Parece que no tienes 'nano' instalado.")
        if accept("¿Deseas usar algun otro editor?"):
            editor = input("Ingresa el nombre del editor que deseas usar (debe estar instalado en el sistema): ")
            if which(editor) is None:
                advise(f"El editor '{editor}' no se encuentra instalado. Saliendo...")
                secure_exit("Saliendo...")
            else:
                config_data = load_config()
                config_data["editor"] = editor
                modify_config_json(config_data)
                advise(f"Editor por defecto cambiado a '{editor}'.")
        else:
            print("Saliendo... Por favor instala 'nano' o cambia el editor por defecto en el archivo de configuracion.")
            secure_exit("Saliendo...")
    print("Dependencias en orden.")

    advise("Configuraciones En Orden")

def load_config() -> dict:
    """ Carga el archivo de configuracion """
    paths = ConfigurationManager()
    with open(paths.config_file_path, "r") as f:
        config_data = json.load(f)
    return config_data

def edit_config() -> None:
    """ Permite al usuario editar las configuraciones del programa """
    config_data = load_config()
    editor = config_data["editor"]
    max_backups = config_data["backup_configs"]["max_auto_backups"]

    advise("Configuracion Actual")
    print(f"Editor: {editor}", f"Limite de copias de seguridad automaticas: {max_backups}", sep="\n", end="\n\n")
    option = select_option("¿Que desea modificar?", ["Editor", "Limite de copias de seguridad automaticas", "Salir"])

    if option == 1:
        new_editor = input("Ingrese el nombre del nuevo editor (debe estar instalado en el sistema): ")
        if which(new_editor) is None:
            advise(f"El editor '{new_editor}' no se encuentra instalado. No se realizaron cambios.")
        else:
            config_data["editor"] = new_editor
            modify_config_json(config_data)
            advise(f"Editor cambiado a '{new_editor}'.")
    elif option == 2:
        while True:
            try:
                new_max = int(input("Ingrese el nuevo limite de copias de seguridad automaticas (numero entero): "))
                if new_max < 1:
                    raise ValueError
                break
            except ValueError:
                advise("Por favor ingrese un numero entero valido mayor que 0.")
        config_data["backup_configs"]["max_auto_backups"] = new_max
        modify_config_json(config_data)
        advise(f"Limite de copias de seguridad automaticas cambiado a {new_max}.")
    else:
        advise("Saliendo sin realizar cambios.")

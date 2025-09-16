import os
import shutil
from sys import exit as secure_exit
import json

class System_Config_Editor:
    def __init__(self):
        #Rutas
        self.root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(self.root_path, "config")
        self.templates_path = os.path.join(self.root_path, "templates")
        
        BIENVENIDA = "Bienvenid@ a System_Config_Editor"

        self.advise(BIENVENIDA)
        
        self.setup_config()
        
        self.config_file_path = os.path.join(self.config_path, "config.json")
        self.open_config()

        self.main_menu()

    def advise(self, message:str):
        print("","="*len(message),message,"="*len(message),"",sep="\n")

    def setup_config(self):
        print("Revisando estado de las configuraciones...")
        if not os.path.exists(self.config_path):
            print("Preparando configuraciones...")
            os.mkdir(self.config_path)
        
        for file in os.listdir(self.templates_path):
            src = os.path.join(self.templates_path, file)
            dst = os.path.join(self.config_path, file)

            if not os.path.exists(dst):
                shutil.copy(src, dst)
                print("Archivo Creado:", dst)
        
        print("Configuraciones En Orden")

    def open_config(self):
        with open(self.config_file_path, "r") as f:
            config_data = json.load(f)
        self.config_file = config_data

    def select_option(self, title:str, options:list):
        while True:
            print("---",title,"---")
            for index, item in enumerate(options, start=1):
                print(f" {index}. {item}")
            try:
                option = int(input("Ingrese el numero de la opcion que quiere hacer: "))
                if 0 < option <= len(options):
                    return option
                else:
                    raise IndexError("Opcion inexistente")
            except (ValueError, IndexError) as e:
                error = f"Entrada invalida: {e}"
                self.advise(error)
            
    def main_menu(self):
        menu_options = {
            "Agregar un archivo":self.new_archive,
            "Editar un archivo":self.edit_archive,
            "Restaurar un archivo":self.restore_archive,
            "Salir":self.exit_program 
            }
        menu_keys = list(menu_options.keys())
        
        while True:
            option = self.select_option("¿Que desea realizar?", menu_keys)
            menu_options[menu_keys[option - 1]]()
    
    def search_archive(self, text:str):
        path = input(text)
        if path.startswith("~"):
            path = os.path.expanduser(path)
        
        if os.path.isfile(path):
            return [True, path]
        else:
            return [False, "El archivo no existe en la ruta proporcionada."]

    def new_archive(self):
        path = self.search_archive("Ingrese el path del archivo a agregar: ")

        if path[0]:
            if path[1] in self.config_file["path_configs"].values():
                self.advise("El archivo ya se encuentra en las configuraciones")
            else:
                print(f"El archivo '{path[1]}' fue encontrado")
                name = input("Ingrese el nombre con el que quiere guardar el archivo: ")
                
                print("agregando a las configuraciones...")
                self.config_file["path_configs"][name] = path[1]
                with open(self.config_file_path, "w") as f:
                    json.dump(self.config_file, f, indent=4)
                self.advise(f"Archivo '{name}' agregado a las configuraciones.")
                
                self.open_config() # Recargar configuraciones
        else:
            self.advise(path[1])

    def edit_archive(self):
        options = list(self.config_file["path_configs"].keys())
        options.append("Otro archivo")
        option = self.select_option("¿Que archivo desea editar?", options)
        if option == len(options):
            path = self.search_archive("Ingrese el path del archivo a editar: ")
            if path[0]:
                print(f"El archivo '{path[1]}' fue encontrado")
                os.system(f"${{EDITOR:-nano}} {path[1]}")
            else:
                self.advise(path[1])
        else:
            name = options[option - 1]
            path = self.config_file["path_configs"][name]
            print(f"Abriendo '{name}'...")
            os.system(f"${{EDITOR:-nano}} {path}")

    def restore_archive(self):
        print("Que archivo quiere restaurar")

    def exit_program(self):
        secure_exit("Saliendo...")
        
if __name__ == "__main__":
    x = System_Config_Editor()
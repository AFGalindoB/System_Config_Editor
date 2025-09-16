import os
import shutil
from sys import exit as secure_exit

class System_Config_Editor:
    def __init__(self):
        #Rutas
        self.root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(self.root_path, "config")
        self.templates_path = os.path.join(self.root_path, "templates")
        
        BIENVENIDA = "Bienvenid@ a System_Config_Editor"

        print("="*len(BIENVENIDA),BIENVENIDA,"="*len(BIENVENIDA),sep="\n")
        
        self.setup_config()
        self.main_menu()

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

    def select_option(self, title:str, options:list):
        while True:
            print(title)
            for index, item in enumerate(options):
                print(f" {index + 1}. {item}")
            try:
                option = int(input("Ingrese el numero de la opcion que quiere hacer: "))
                if 0 < option <= len(options):
                    return option
                else:
                    raise IndexError("Opcion inexistente")
            except (ValueError, IndexError) as e:
                error = f"Entrada invalida: {e}"
                print("","="*len(error),error,"="*len(error),"",sep="\n")
            
    def main_menu(self):
        menu_options = {
            "Agregar un archivo":self.new_archive,
            "Editar un archivo":self.edit_archive,
            "Restaurar un archivo":self.restore_archive,
            "Salir":self.exit_program 
            }
        menu_keys = list(menu_options.keys())
        
        while True:
            option = self.select_option("--- ¿Que desea realizar? ---", menu_keys)
            menu_options[menu_keys[option - 1]]()
    
    def new_archive(self):
        print("Ingrese el path del archivo a agregar")

    def edit_archive(self):
        print("Que archivo quiere editar")

    def restore_archive(self):
        print("Que archivo quiere restaurar")

    def exit_program(self):
        secure_exit("Saliendo...")
        
if __name__ == "__main__":
    x = System_Config_Editor()
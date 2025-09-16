import os
import shutil
from sys import exit as secure_exit
import json

class System_Config_Editor:
    def __init__(self):
        #Rutas
        self.root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.templates_path = os.path.join(self.root_path, "templates")
        self.config_path = os.path.join(self.root_path, "config")
        self.config_file_path = os.path.join(self.config_path, "config.json")

        BIENVENIDA = "Bienvenid@ a System_Config_Editor"

        self.advise(BIENVENIDA)
        
        self.setup_config()
        
        self.open_config()

        self.main_menu()

    def advise(self, message:str) -> None:
        """ Muestra un mensaje en pantalla con un formato """
        print("","="*len(message),message,"="*len(message),"",sep="\n")

    def setup_config(self) -> None:
        """ Verifica que las configuraciones esten disponibles, si no es asi las crea """
        print("Revisando estado de las configuraciones...")
        
        # Crear carpeta config si no existe
        if not os.path.exists(self.config_path):
            print("Preparando configuraciones...")
            os.mkdir(self.config_path)
        
        # Copiar archivos de templates a config si no existen
        for file in os.listdir(self.templates_path):
            src = os.path.join(self.templates_path, file)
            dst = os.path.join(self.config_path, file)

            if not os.path.exists(dst):
                shutil.copy(src, dst)
                print("Archivo Creado:", dst)
        
        print("Configuraciones En Orden")

    def open_config(self) -> None:
        """ Abre el archivo de configuracion y lo carga en el atributo config_file """
        with open(self.config_file_path, "r") as f:
            config_data = json.load(f)
        self.config_file = config_data

    def select_option(self, title:str, options:list) -> int:
        """ Muestra un menu de opciones verifica que la entrada sea valida y la retorna"""
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
    
    def accept(self, text:str) -> bool:
        """ Solicita una entrada si/no y retorna True/False """
        while True:
            option = input(f"{text} (s/n): ").lower()
            if option in ["s", "n"]:
                return option == "s"
            else:
                self.advise("Entrada invalida, por favor ingrese 's' o 'n'.")

    def main_menu(self) -> None:
        """ Menu principal del programa """

        menu_options = {
            "Agregar un archivo":self.new_archive,
            "Editar un archivo":self.menu_edit_archive,
            "Restaurar un archivo":self.restore_archive,
            "Salir":self.exit_program 
            }
        
        menu_keys = list(menu_options.keys())
        
        while True:
            option = self.select_option("¿Que desea realizar?", menu_keys)
            menu_options[menu_keys[option - 1]]()
    
    def archive_exist(self, text:str) -> dict:
        """ Verifica si un archivo existe en la ruta proporcionada """
        path = input(text)
        if path.startswith("~"):
            path = os.path.expanduser(path)
        
        if os.path.isfile(path):
            print(f"El archivo '{path}' fue encontrado")
            return {"Exist":True, "path":path}
        else:
            self.advise("El archivo no existe en la ruta proporcionada.")
            return {"Exist":False, "path":""}

    def archive_is_in_config(self, path) -> dict:
        """ Verifica si un archivo ya se encuentra en las configuraciones """
        if path in self.config_file["path_configs"].values():
            name = [key for key,value in self.config_file["path_configs"].items() if value == path][0]
            self.advise(f"El archivo ya se encuentra en las configuraciones. Bajo el nombre '{name}'")
            return {"Is_in":True, "name":name}
        else:
            return {"Is_in":False, "name":None}

    def add_archive(self, name, path) -> None:
        """ Agrega un nuevo archivo a las configuraciones """
        print("Agregando a las configuraciones...")
        self.config_file["path_configs"][name] = path

        with open(self.config_file_path, "w") as f:
            json.dump(self.config_file, f, indent=4)
        
        self.advise(f"Archivo '{name}' agregado a las configuraciones.")
        self.open_config() # Recargar configuraciones

    def new_archive(self, path=None) -> None:
        """ Establece el formato para un nuevo archivo para las configuraciones """
        if path == None:
            path = self.get_path_archive("Ingrese el path del archivo a agregar: ")

        if path != None:
            if not self.archive_is_in_config(path["path"])["Is_in"]:
                name = input("Ingrese el nombre con el que quiere guardar el archivo: ")
                self.add_archive(name, path["path"])

    def get_path_archive(self, text=None, select=False) -> str|None:
        """ Obtiene el path de un archivo  """
        if select:
            options = list(self.config_file["path_configs"].keys()) # Obtenemos los nombres de los archivos
            options.append("Otro archivo") # Opcion para otro archivo
            option = self.select_option("¿Que archivo desea elegir?", options) # Seleccion de opcion
        
            if option < len(options):
                name = options[option - 1]
                path = self.config_file["path_configs"][name]
                return path
            
        path = self.archive_exist("Ingrese el path del archivo: " if text == None else text)
        return path["path"] if path["Exist"] else None

    def edit_archive(self, path) -> None:
        """ Abre el archivo usando el editor nano """
        name = self.archive_is_in_config(path)
        print(f"Abriendo archivo '{name["name"] if name["Is_in"] else path}'...")
        os.system(f"${{EDITOR:-nano}} {path}")

    def menu_edit_archive(self) -> None:
        ## Refactorizar codigo separar la logica en metodos individuales
        path = self.get_path_archive()
        
        if path != None:
            if not self.archive_is_in_config(path)["Is_in"]:
                self.edit_archive(path)
                self.advise("El archivo no se encuentra en las configuraciones.")
                add = self.accept("¿Desea agregarlo?")
                self.new_archive(path=path) if add else None
            else:
                open = self.accept("¿Desea editarlo?")
                if open:
                    self.edit_archive(path)

    def restore_archive(self):
        print("Que archivo quiere restaurar")

    def exit_program(self):
        secure_exit("Saliendo...")
        
if __name__ == "__main__":
    x = System_Config_Editor()
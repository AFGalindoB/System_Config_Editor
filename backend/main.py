import os
from sys import exit as secure_exit
from cli_ui import advise, select_option, accept
from add_archive import Add_Archive
from config_manager import setup_config
from archive_manager import edit_a_path_config

class System_Config_Editor():
    def __init__(self):

        BIENVENIDA = "Bienvenid@ a System_Config_Editor"

        advise(BIENVENIDA)
        
        setup_config()

        self.main_menu()

    def main_menu(self) -> None:
        """ Menu principal del programa """

        menu_options = {
            "Agregar un archivo":Add_Archive,
            "Modificar una ruta almacenada":edit_a_path_config,
            "Editar un archivo":self.menu_edit_archive,
            "Restaurar un archivo":self.restore_archive,
            "Salir":self.exit_program 
            }
        
        menu_keys = list(menu_options.keys())
        
        while True:
            option = select_option("¿Que desea realizar?", menu_keys)
            menu_options[menu_keys[option - 1]]()
    
    def edit_archive(self, path) -> None:
        """ Abre el archivo usando el editor nano """
        name = self.archive_is_in_config(path)
        print(f"Abriendo archivo '{name["name"] if name["Is_in"] else path}'...")
        os.system(f"${{EDITOR:-nano}} {path}")

    def menu_edit_archive(self) -> None:
        raise NotImplementedError("Aun no implementado")
        path = config_manager.get_path_archive()
        
        if path != None:
            if not config_manager.archive_is_in_config(path)["Is_in"]:
                self.edit_archive(path)
                advise("El archivo no se encuentra en las configuraciones.")
                add = accept("¿Desea agregarlo?")
                Add_Archive(path=path) if add else None
            else:
                open = accept("¿Desea editarlo?")
                if open:
                    self.edit_archive(path)

    def restore_archive(self):
        print("Que archivo quiere restaurar")

    def exit_program(self):
        secure_exit("Saliendo...")
        
if __name__ == "__main__":
    x = System_Config_Editor()
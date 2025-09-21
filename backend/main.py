from sys import exit as secure_exit
from cli_ui import advise, select_option
from archive_editor import menu_edit_archive
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
            "Editar un archivo":menu_edit_archive,
            "Restaurar un archivo":self.restore_archive,
            "Salir":self.exit_program 
            }
        
        menu_keys = list(menu_options.keys())
        
        while True:
            option = select_option("¿Que desea realizar?", menu_keys)
            menu_options[menu_keys[option - 1]]()

    def restore_archive(self):
        print("Que archivo quiere restaurar")

    def exit_program(self):
        secure_exit("Saliendo...")
        
if __name__ == "__main__":
    x = System_Config_Editor()
from sys import exit as secure_exit
from cli_ui import advise, select_option
from archive_editor import Editor
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
            "Agregar un nuevo archivo a rastrear":Add_Archive,
            "Modificar informacion de un archivo rastreado":edit_a_path_config,
            "Editar un archivo":Editor,
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
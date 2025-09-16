import json
from cli_ui import advise
from config_manager import ConfigurationManager, load_config
from archive_manager import archive_is_in_config, get_path_archive

class Add_Archive:
    def __init__(self, path=None):
        """ 
        Agrega un nuevo archivo a las configuraciones 
        Args:
            path (str, optional): Path del archivo a agregar.
            Si se proporciona, no se solicita al usuario el path del archivo.
        """

        self.config_file = load_config()
        self.config_file_path = ConfigurationManager().config_file_path

        # Si no se proporciona un path, solicitarlo al usuario
        if path == None:
            path = get_path_archive(text="Ingrese el path del archivo a agregar: ")

        if path != None: # Si existe el archivo
            if not archive_is_in_config(path)["Is_in"]: # Si el archivo no esta en las configuraciones
                while True:
                    name = input("Ingrese el nombre con el que quiere guardar el archivo: ")
                    if name not in self.config_file["path_configs"].keys():
                        break
                    else:
                        advise("El nombre ya existe en las configuraciones, por favor ingrese otro.")
                self._add_archive(name, path)

    def _add_archive(self, name, path) -> None:
        print("Agregando a las configuraciones...")
        self.config_file["path_configs"][name] = path

        with open(self.config_file_path, "w") as f:
            json.dump(self.config_file, f, indent=4)
        
        advise(f"Archivo '{name}' agregado a las configuraciones.")
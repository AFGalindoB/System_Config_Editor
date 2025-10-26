from archive_manager import get_path_archive, archive_is_in_config
from add_archive import Add_Archive
from config_manager import load_config
from backup_manager import make_backup
import os
from shutil import which as is_installed
from cli_ui import advise, accept

class Editor:
    def __init__(self) -> None:
        self.path = get_path_archive(select=True) # Obtener path del archivo a editar
        self.name = archive_is_in_config("path", self.path)

        self.menu_edit_archive()

    def edit_archive(self) -> None:
        """ Abre el archivo usando el editor guardado en las configuraciones (nano por defecto) """
        config = load_config()

        editor_name = config["editor"]
        print(f"Abriendo archivo '{self.name if self.name else self.path}'...\n")
            
        if is_installed(editor_name) is None:
            advise(f"El editor '{editor_name}' no se encuentra instalado. Usando nano...")
            editor_name = "nano"
        
        os.system(f"{editor_name} {self.path}")

    def menu_edit_archive(self) -> None:
        if self.path != None:

            make_backup(self.name, self.path)
            self.edit_archive()

            if not archive_is_in_config("path", self.path, message=False):
                advise("El archivo no se encuentra en las configuraciones.")
                add = accept("¿Desea agregarlo?")
                Add_Archive(path=self.path) if add else None
            
            advise("¿Desea guardar la configuracion actual?")
            save = accept("¿Desea guardar la configuracion actual?")
            make_backup(self.name, self.path, type_backup="manual") if save else None
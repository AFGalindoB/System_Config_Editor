from archive_manager import get_path_archive, archive_is_in_config
from add_archive import Add_Archive
import os
from cli_ui import advise, accept

def edit_archive(path) -> None:
        """ Abre el archivo usando el editor nano """
        name = archive_is_in_config("path", path)
        print(f"Abriendo archivo '{name if name else path}'...", end="\n\n")
        os.system(f"${{EDITOR:-nano}} {path}")

def menu_edit_archive() -> None:
    path = get_path_archive(select=True) # Obtener path del archivo a editar
    
    if path != None:
        edit_archive(path)
        if not archive_is_in_config("path", path, message=False):
            advise("El archivo no se encuentra en las configuraciones.")
            add = accept("¿Desea agregarlo?")
            Add_Archive(path=path) if add else None
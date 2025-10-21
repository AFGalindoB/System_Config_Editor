from cli_ui import advise, select_option
from config_manager import ConfigurationManager, load_config
from archive_manager import archive_exist, edit_a_path_config
from backup_manager import make_backup
from shutil import copy2
import os

def restore_archive():
    path_manual_backups = ConfigurationManager().manual_backups_path
    path_auto_backups = ConfigurationManager().auto_backups_path
    archives_restorables = []
    paths = []
    folders_name = []

    type_option = select_option("¿Que tipo de archivo desea restaurar?: ", ["Archivo de respaldo manual", "Archivo de respaldo automatico"])
    backups_path_selected = path_manual_backups if type_option == 1 else path_auto_backups

    # Listar las carpetas y archivos disponibles para restaurar
    folders = os.listdir(backups_path_selected)
    for i0, folder in enumerate(folders):
        print(f"{i0 + 1}. {folder}")
        
        folders_name.append(folder)
        
        path_folder = os.path.join(backups_path_selected, folder)
        archives = os.listdir(path_folder)
        
        for i1, archive in enumerate(archives):
            print(f"    {i0+1}-{i1+1}. {archive}")
        
            path_archive = os.path.join(path_folder, archive)
            paths.append(path_archive)
        
        archives_restorables.append(paths)
        paths = []
    
    # Obtener el archivo a restaurar
    backup_to_restore = input("Ingrese el indice del archivo a restaurar: ")
    folder_index, archive_index = map(int, backup_to_restore.split('-'))
    
    archive_to_restore = archives_restorables[folder_index - 1][archive_index - 1]
    folder_to_restore = folders_name[folder_index - 1]
    destination = load_config()["path_configs"][folder_to_restore]

    if not archive_exist(path=destination):
        advise(f"La ruta del archivo {folder_to_restore} rastreada en las configuraciones no existe")
        edit_a_path_config(repair=True)
        destination = load_config()["path_configs"][folder_to_restore]

    archive_restorable_name = os.path.basename(archive_to_restore)
    advise(f"Restaurando archivo: {archive_restorable_name}...")

    make_backup(name=folder_to_restore, path=destination, type_auto="restore")
    copy2(archive_to_restore, destination)
    advise(f"Archivo '{archive_restorable_name}' restaurado con exito.")
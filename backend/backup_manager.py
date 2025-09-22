from shutil import copy
from config_manager import ConfigurationManager
from datetime import datetime
import os

def make_backup(name:str, path:str, backup_path:str, type_backup:str="auto") -> None:
    """
    Crea un backup del archivo en la carpeta de backups 
    Args:
        name (str): Nombre del archivo
        path (str): Path del archivo
        backup_path(str): Ruta del backup "auto" o "manual"
        type_backup (str): Tipo de backup, "auto" o "manual"
    """
    
    # Crear carpeta de backup si no existe
    new_backup_folder = os.path.join(backup_path, name)
    if not os.path.exists(new_backup_folder):
        os.mkdir(new_backup_folder)
    
    base, ext = os.path.splitext(path)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{base}_({timestamp}){ext}"
    dst = os.path.join(new_backup_folder, file_name)


    if type_backup == "auto":

        copy(path, dst)
        print(f"Backup '{file_name}' creado en: {new_backup_folder}")

def get_backups(folder_path):
    if not os.path.exists(folder_path):
        return []
    
    # Obtenemos una lista ordenada de los backups
    backups = sorted(os.listdir(folder_path), reverse=True)
    return backups

def add_auto_backup(name:str, path:str):
    raise NotImplementedError("En desarrollo")
    ## Hacer que limite a 20 los backups y valla eliminando el mas viejo para agregar uno nuevo
    paths = ConfigurationManager()
    auto_backups_path = paths.auto_backups_path
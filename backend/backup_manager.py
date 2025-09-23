from shutil import copy2
from config_manager import ConfigurationManager, load_config
from datetime import datetime
import os

def make_backup(path:str, backup_path:str, type_backup:str="auto") -> None:
    """
    Crea un backup del archivo en la carpeta de backups 
    Args:
        path (str): Path del archivo a hacer backup
        backup_path(str): Ruta de la carpeta donde se guardara el backup
        type_backup (str): Tipo de backup, "auto" o "manual"
    """
    
    base_name = os.path.basename(path)
    base, ext = os.path.splitext(base_name)

    if type_backup == "auto":
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{base}_({timestamp}){ext}"
        dst = os.path.join(backup_path, file_name)

        copy2(path, dst)
        print(f"Backup '{file_name}' creado en: {backup_path}")
    else:
        ## Implementar el guardado manual
        return
        backup_name = input("Ingrese el nombre con el que se guardara el respaldo: ")
        file_name = f"{base}_({backup_name}){ext}"

        name_folder_manual_backup = os.path.join(backup_path, backup_name)
        os.mkdir(name_folder_manual_backup)

        dst = os.path.join(name_folder_manual_backup, file_name)

def add_auto_backup(name:str, path:str, type_backup:str="auto"):
    """
    Genera la carpeta del backup y maneja el limite de backup
    Args:
        name (str): Nombre con el que se guardo el archivo en las configuraciones
        path (str): Path del archivo a hacer backup
        type_backup (str): Tipo de backup, "auto" o "manual"
        """
    paths = ConfigurationManager()
    backup_configs = load_config()["backup_configs"]
    
    # Obtiene el path de la carpeta de backups 'auto' o 'manual' segun sea el caso
    backups_path = paths.auto_backups_path if type_backup == "auto" else paths.manual_backups_path
    
    # Crear carpeta del backup con el nombre del tipo de archivo si no existe
    backup_folder = os.path.join(backups_path, name)
    if not os.path.exists(backup_folder):
        os.mkdir(backup_folder)

    backups = sorted(os.listdir(backup_folder), reverse=True)

    print(len(backups))

    while len(backups) >= backup_configs["max_auto_backups"]:
        backup_to_delete = os.path.join(backup_folder, backups[-1])
        os.remove(backup_to_delete)
        backups = sorted(os.listdir(backup_folder), reverse=True)
    
    make_backup(path, backup_folder, type_backup=type_backup)
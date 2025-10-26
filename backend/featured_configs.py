import os
from cli_ui import advise, select_option
from config_manager import  load_config, modify_config_json, ConfigurationManager

def menu():
    options = ["Agregar nueva configuracion destacada", "Cambiar a una configuracion destacada",  "Eliminar configuracion destacada", "Volver al menu principal"]
    option = select_option("¿Que desea hacer?", options)
    if option == 1:
        add_featured_config()
    elif option == 2:
        switch_to_featured_config()
    elif option == 3:
        remove_featured_config()
    elif option == 3:
        return

def add_featured_config():
    path = ConfigurationManager().manual_backups_path
    folders_name = []
    paths = []
    archives_paths = []

    # Listar las carpetas y archivos disponibles
    folders = os.listdir(path)
    for i0, folder in enumerate(folders):
        print(f"{i0 + 1}. {folder}")

        folders_name.append(folder)

        path_folder = os.path.join(path, folder)
        archives = os.listdir(path_folder)
        for i1, archive in enumerate(archives):
            print(f"    {i0+1}-{i1+1}. {archive}")

            path_archive = os.path.join(path_folder, archive)
            paths.append(path_archive)
    
        archives_paths.append(paths)
        paths = []
    
    featured_archive = input("Ingrese el indice del archivo a destacar: ")
    folder_index, archive_index = map(int, featured_archive.split('-'))

    value = archives_paths[folder_index - 1][archive_index - 1]
    key = folders_name[folder_index - 1]

    configs = load_config()
    configs["featured_configs"][key] = value
    modify_config_json(configs)
    advise(f"Configuracion destacada '{key}' agregada con exito.")

def switch_to_featured_config():
    raise NotImplementedError("Esta funcion aun no ha sido implementada.")
    configs = load_config()
    featured_configs = configs["featured_configs"]
    if not featured_configs:
        advise("No hay configuraciones destacadas disponibles.")
        return

def remove_featured_config():
    raise NotImplementedError("Esta funcion aun no ha sido implementada.")
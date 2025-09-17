import os
from cli_ui import advise, select_option
from config_manager import load_config, modify_config_json

def archive_exist(text:str=None, path:str=None) -> str|bool:
    """ 
    Verifica si un archivo existe en la ruta proporcionada
    Args:
        text (str, optional): Texto a mostrar al solicitar el path.
        path (str, optional): Path del archivo a verificar.
    Returns:
        Retorna el path si el archivo existe, de lo contrario False
    """
    if path == None:
        path = input(text)

    if path.startswith("~"): # Expandir ~ a la ruta del home
        path = os.path.expanduser(path)
    
    # Verificar si el archivo existe
    if os.path.isfile(path):
        print(f"El archivo '{path}' fue encontrado")
        return path
    else:
        advise("El archivo no existe en la ruta proporcionada.")
        return False

def archive_is_in_config(item_type, item) -> str|bool:
    ## Refactorizar para que solo retorne un valor
    """
    Verifica si el nombre o la ruta de un archivo ya se encuentra en las configuraciones
    Args:
        name (str, optional): Nombre del archivo a verificar.
        path (str, optional): Path del archivo a verificar.
    Returns:
        str|False:
        Retorna el nombre con el que se guardo el archivo en las 
        configuraciones si se encuentra, de lo contrario retorna False.
    """

    paths_in_config = load_config()["path_configs"]

    if item_type == "name":
        if item in paths_in_config.keys():
            advise(f"El nombre '{item}' se encuentra en las configuraciones.")
            return item
    else:
        if item in paths_in_config.values():

            # Buscar el nombre del con el que se guardo el archivo
            for key, value in paths_in_config.items():
                if value == item:
                    advise(f"El archivo ya se encuentra en las configuraciones. Bajo el nombre '{key}'")
                    return key
            
    return False

def get_path_archive(text=None, select=False) -> str|None:
    """
    Obtiene el path de un archivo ingresado por el usuario o seleccionado de las configuraciones
    y comprueba si existe.

    Args:
        text (str, optional): Texto a mostrar al usuario al solicitar el path.
        select (bool, optional): Si es True, permite seleccionar un archivo de las configuraciones.
    Returns:
        str|None: Retorna el path del archivo como string si existe, de lo contrario None.
    """
    
    paths_in_config = load_config()["path_configs"]

    if select:
        options = list(paths_in_config.keys()) # Obtenemos los nombres de los archivos
        options.append("Otro archivo") # Opcion para elegir otro archivo
        
        option = select_option("¿Que archivo desea elegir?", options)
    
        # Si no se selecciono "Otro archivo" obtenemos el path del archivo seleccionado
        if option < len(options):
            name = options[option - 1]
            path = paths_in_config[name]
            if archive_exist(path=path):
                return path
            else:
                advise("Ups. Parece que el archivo ya no existe en la ruta guardada en las configuraciones.")
                return None
        
    path = archive_exist("Ingrese el path del archivo: " if text == None else text)
    return path if path else None

def edit_a_path_config():
    config_data = load_config()
    while True:
        option = select_option("¿Que desea editar?",["Nombres","Rutas","Cancelar"])
        if option == 3:
            print("Abortando edicion...")
            return

        print("Rutas almacenadas:")

        for name, path in config_data["path_configs"].items():
            print(f"- {name}: {path}")
        
        name_to_edit = input("Ingrese el nombre que desea editar: ")
        
        if not archive_is_in_config("name", name_to_edit):
            advise(f"{'Nombre' if option == 1 else 'Ruta'} '{name_to_edit}' no se encuentra en las configuraciones.")
        else:
            break
    
    type_item = "name" if option == 1 else "path"
    while True:
        
        new = input(f"Ingrese el nuevo {'nombre' if option == 1 else 'path' } (Ingrese {name_to_edit} para abortar): ")
        
        if name_to_edit == new:
            print("Abortando edicion...")
            break
        
        # Verificar si la nueva ruta existe
        if option == 2:
            new = archive_exist(path=new)
            if not new:
                advise("La ruta ingresada no existe, porfavor ingrese una ruta valida.")
                continue
        
        # Verificar si el nuevo nombre o ruta ya existe en las configuraciones
        if archive_is_in_config(type_item, new):
            print("Porfavor ingrese otro.")
            continue
            
        # Realizar la edicion
        if option == 1:
            config_data["path_configs"][new] = config_data["path_configs"][name_to_edit]
            config_data["path_configs"].pop(name_to_edit)
        else:
            config_data["path_configs"][name_to_edit] = new
        modify_config_json(config_data)
        advise(f"{'Nombre' if option == 1 else 'Ruta'} cambiada de {name_to_edit} a '{new}'")
        break
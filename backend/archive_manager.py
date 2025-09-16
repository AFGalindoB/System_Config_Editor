import os
from cli_ui import advise, select_option
from config_manager import load_config

def archive_exist(text:str=None, path:str=None) -> dict:
    """ 
    Verifica si un archivo existe en la ruta proporcionada
    Args:
        text (str, optional): Texto a mostrar al solicitar el path.
        path (str, optional): Path del archivo a verificar.
    Returns:
        {"Exist":bool, "path":str} 
        Retorna True y el path si el archivo existe, de lo contrario False y un string vacio.
    """
    if path == None:
        path = input(text)

    if path.startswith("~"): # Expandir ~ a la ruta del home
        path = os.path.expanduser(path)
    
    # Verificar si el archivo existe
    if os.path.isfile(path):
        print(f"El archivo '{path}' fue encontrado")
        return {"Exist":True, "path":path}
    else:
        advise("El archivo no existe en la ruta proporcionada.")
        return {"Exist":False, "path":""}

def archive_is_in_config(path) -> dict:
    """
    Verifica si un archivo ya se encuentra en las configuraciones
    Returns:
    {"Is_in":bool, "name":str|None} 
    Retorna True y el nombre con el que se guardo el archivo en las configuraciones,
    de lo contrario False y None.
    """
    paths_in_config = load_config()["path_configs"]

    if path in paths_in_config.values():

        # Buscar el nombre del con el que se guardo el archivo
        for key, value in paths_in_config.items():
            if value == path:
                name = key
                break
        
        advise(f"El archivo ya se encuentra en las configuraciones. Bajo el nombre '{name}'")
        return {"Is_in":True, "name":name}
    else:
        return {"Is_in":False, "name":None}

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
            if archive_exist(path=path)["Exist"]:
                return path
            else:
                advise("Ups. Parece que el archivo ya no existe en la ruta guardada en las configuraciones.")
                return None
        
    path = archive_exist("Ingrese el path del archivo: " if text == None else text)
    return path["path"] if path["Exist"] else None
def advise(message:str) -> None:
    """ Muestra un mensaje en pantalla con un formato """
    print("","="*len(message),message,"="*len(message),"",sep="\n")

def select_option(title:str, options:list) -> int:
    """ Muestra un menu de opciones verifica que la entrada sea valida y la retorna"""
    while True:
        print("---",title,"---")
        for index, item in enumerate(options, start=1):
            print(f" {index}. {item}")
        try:
            option = int(input("Ingrese el numero de la opcion que quiere hacer: "))
            if 0 < option <= len(options):
                return option
            else:
                raise IndexError("Opcion inexistente")
        except (ValueError, IndexError) as e:
            error = f"Entrada invalida: {e}"
            advise(error)

def accept(text:str) -> bool:
    """ Solicita una entrada si/no y retorna True/False """
    while True:
        option = input(f"{text} (s/n): ").lower()
        if option in ["s", "n"]:
            return option == "s"
        else:
            advise("Entrada invalida, por favor ingrese 's' o 'n'.")
# System Config Editor
Este es un programa destinado a los usuarios de linux que manipulen archivos de configuracion para personalizar su entorno

## Introduccion
Este es un programa desarrollado en **Python** que se encarga de gestionar los archivos (.conf, .css etc) que use el usuario para personalizar su entorno permitiendole:

1. Administrar sus archivos de configuraciones
2. Poder editar sus archivos desde el programa usando el editor de su preferencia 
3. Tener copias de seguridad automaticas que le permitan restaurar sus archivos de configuracion en caso de fallo
4. Guardar manualmente distintas configuraciones que halla realizado
5. Poder cambiar entre distintas configuraciones que el usuario tenga
6. Poder comparar sus archivos de configuraciones para trasladar sus personalizaciones de una configuracion pasada a la nueva

## Dependencias del sistema:
- Python 3.13+
- Editor: nano (por defecto). Puedes cambiarlo al inicializar por primera vez la aplicacion (Coloca el nombre con el que invocas el editor desde la terminal)
import config_path_routes
import os
import general_functions as gf
from loguru import logger
from transformation_functions import PandasBaseTransformer as PBT
from Avion_Mantenimiento import Avion

print("Hola Mundo!")

config = gf.Procesar_configuracion("config.yml")

# Comentar las 3 siguientes lineas para ejecutar en Visual Studio.
# Seleccion parte del proceso a ejecutar:
def mostrar_menu():
    """Muestra el menú de opciones al usuario."""
    print("\nMenú de Opciones:")
    print("1. Ingresar a los procesos de gesiton de avion")


def ejecutar_opcion(opcion):
    """Ejecuta la opción seleccionada por el usuario."""
    if opcion == "1":
        logger.info("Nos permite gestionar el avión y realizar procesos...")
        gestionar_avion()
    elif opcion == "2":
        pass
    elif opcion == "3":
        pass
    elif opcion == "0":
        logger.info("Saliendo del programa...")
    else:
        print("Opción no válida. Por favor, seleccione una opción del menú.")


def gestionar_avion():
    Lector_insumo = gf.ExcelReader(path=config["path_insumos"])
    
    df_info_avion = Lector_insumo.Lectura_simple_excel(
        nom_insumo=config["directorio_aviones"]["nom_base"],
        nom_hoja=config["directorio_aviones"]["nom_hoja"],
    )
    
    avion = Avion(df_info_avion, config, matricula="ABC001")
    avion.mostrar_menu()


if __name__=="__main__":
    mostrar_menu()
    lista_opciones = ["1","2","3","4"]
    while True:
        opcion = input("Ingrese una opción: ")
        if str(opcion) in lista_opciones:
            ejecutar_opcion(opcion)
        else:
            logger.info(f"No has ingresado una opción válida. Ingresa una de las opciones disponibles: {lista_opciones}")
            
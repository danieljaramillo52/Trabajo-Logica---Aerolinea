import config_path_routes
import os
import general_functions as gf
from loguru import logger
from transformation_functions import PandasBaseTransformer as PBT
from AvionHangares import Avion, HangarAviones

config = gf.Procesar_configuracion("config.yml")

#menu = config[""]
#print("Ingrese el número de su selección:")
#for opcion, texto in menu.items():
#    print(f"{opcion}. {texto}")


class GestionFBO:
    def __init__(self, __config):
        self.config = __config

    def _mostrar_menu(self):
        dict_menu_principal = self.config["Menu"]["menu_opcion"]
        mensaje_menu = (
            """ 
            Menu principal:
            Ingrese el número de su selección:    
            1.Ingresar a los procesos de gesiton de Avion 
            2.Ingresar a los procesos de gesiton de Hangar
            3.Ingresar a los procesos de gesiton de Empleado
            4.Ingresar a los procesos de gesiton de Tripulacion
            5.Ingresar a los procesos de gesiton de Mantenimiento
            6.Ingresar a los procesos de gesiton de Servicios
            7.Ingresar a los procesos de gesiton de Vuelo
            8.Ingresar a los procesos de gesiton de Pasajero
            0.Ingresar a los procesos de gesiton de Salir
            """
        )
        list_keys = [*dict_menu_principal]
        while True:
                print(mensaje_menu)
                opcion = input("Ingrese una opción: ")
                if  (int(opcion) < 0) | (int(opcion) > 8) :
                    logger.info(f"No has ingresado una opción válida. Ingresa una delas opciones disponibles: ")
                elif int(opcion) == 0 :
                    break
                else:
                    if int(opcion) in list_keys:
                        ejecutar_opcion(opcion)
                    



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
    
    estado = avion.mostrar_menu()
    while estado:
        estado = avion.mostrar_menu()
    return 
if __name__ == "__main__":
    gestion_fbo = GestionFBO(config)
    gestion_fbo._mostrar_menu()
    #Lector_insumo = gf.ExcelReader(path=config["path_insumos"])
#
    #df_info_avion = Lector_insumo.Lectura_simple_excel(
    #    nom_insumo=config["directorio_aviones"]["nom_base"],
    #    nom_hoja=config["directorio_aviones"]["nom_hoja"],
    #)
    #hangar = HangarAviones(config, df_info_avion, PBT)

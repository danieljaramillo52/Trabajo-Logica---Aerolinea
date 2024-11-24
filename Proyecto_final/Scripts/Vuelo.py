from datetime import datetime
from typing import List
from loguru import logger
from Utils import general_functions as gf

class Vuelo:
    def __init__(self, __config, __menu_vuelo=None, __PBT=None):
        """
        Constructor de la clase Vuelo.

        Args:
            __config (dict): Diccionario de configuración del proyecto.
            __menu_vuelo (list): Menú relacionado con vuelos.
            __PBT (class): Clase para la manipulación de datos.
        """
        self.__config = __config
        self.__menu_vuelo = __menu_vuelo
        self.__PBT = __PBT
        self.__pasajeros = []
        self.__avion = None
        self.__peso_equipaje_total = 0.0
        self.__itinerarios = []
        self.__costo_total_vuelo = 0.0
        self.__verificado = False
        self.__cols_df_vuelo = self.__config["directorio_vuelos"]["dict_cols"]
        self.__df_vuelos = self._leer_info_vuelos()

    def mostrar_menu(self):
        """
        Muestra el menú relacionado con vuelos.
        """
        eleccion = self.__config["Menu"]["menu_opcion"][6]
        gf.mostrar_menu_personalizado(eleccion, self.__menu_vuelo)

    def _leer_info_vuelos(self) -> dict:
        """
        Lee los datos de los vuelos desde el archivo Excel configurado.
        :return: DataFrame con la información de los vuelos.
        """
        logger.info("Leyendo información de vuelos desde el archivo configurado...")
        lector_insumo = gf.ExcelReader(path=self.__config["path_insumos"])
        df_info_vuelos = lector_insumo.Lectura_simple_excel(
            nom_insumo=self.__config["directorio_vuelos"]["nom_base"],
            nom_hoja=self.__config["directorio_vuelos"]["nom_hoja"],
        )
        logger.info("Información de vuelos cargada correctamente.")
        print("")
        return df_info_vuelos

    def get_vuelos(self):
        """
        Proporciona el DataFrame con los datos de los vuelos.
        :return: DataFrame de vuelos.
        """
        return self.__df_vuelos

    def calcular_peso_total_equipaje(self):
        """
        Calcula el peso total del equipaje de todos los pasajeros en el vuelo.
        :return: Peso total del equipaje.
        """
        self.__peso_equipaje_total = sum(pasajero.calcular_peso_total_equipaje() for pasajero in self.__pasajeros)
        logger.info(f"Peso total del equipaje calculado: {self.__peso_equipaje_total} kg")
        return self.__peso_equipaje_total

    def agregar_pasajero(self, pasajero):
        """
        Agrega un pasajero al vuelo si hay capacidad disponible y el peso del equipaje no excede el límite permitido.
        
        Args:
            pasajero (Pasajero): Instancia de la clase Pasajero.

        """
        if self.__avion is None:
            logger.error("No se puede agregar un pasajero sin asignar un avión al vuelo.")
            return
        
        if len(self.__pasajeros) >= self.__avion.get_capacidad_pasajeros():
            logger.warning("No se puede agregar al pasajero: capacidad de pasajeros excedida.")
            return
        
        if self.calcular_peso_total_equipaje() + pasajero.calcular_peso_total_equipaje() > self.__avion.get_peso_maximo_equipaje():
            logger.warning("No se puede agregar al pasajero: peso del equipaje excedido.")
            return

        self.__pasajeros.append(pasajero)
        logger.info(f"Pasajero {pasajero.nombre} agregado al vuelo exitosamente.")

    def asignar_avion(self, avion):
        """
        Asigna un avión al vuelo.
        
        Args:
            avion (Avion): Instancia de la clase Avion.
        """
        if not avion.get_disponible():
            logger.error("El avión no está disponible para asignar al vuelo.")
            return
        
        self.__avion = avion
        logger.info(f"Avión {avion.get_modelo()} asignado al vuelo exitosamente.")

    def listar_pasajeros(self):
        """
        Lista todos los pasajeros del vuelo.
        """
        if not self.__pasajeros:
            logger.info("No hay pasajeros asignados a este vuelo.")
            return
        
        print("Lista de pasajeros en el vuelo:")
        for idx, pasajero in enumerate(self.__pasajeros, start=1):
            print(f"{idx}. {pasajero.nombre} - Documento: {pasajero.documento_identidad}")
        logger.info(f"Se listaron {len(self.__pasajeros)} pasajeros.")

    def verificar_disponibilidad_avion(self):
        """
        Verifica si el avión asignado está disponible.
        """
        if self.__avion and self.__avion.get_disponible():
            logger.info("El avión asignado está disponible para el vuelo.")
            return True
        logger.warning("El avión asignado no está disponible o no se ha asignado ningún avión.")
        return False

    def ejecutar_proceso_vuelos(self):
        """
        Ejecuta un proceso basado en la opción ingresada para los vuelos.
        """
        opcion_ingresada = input("Ingresa la opción a ejecutar:\n ")
        resultado = self.ejecutar_proceso(opcion_ingresada)
        return resultado

    def administrar_vuelos(self):
        """
        Administra los datos de vuelos seleccionando columnas específicas.
        """
        df_select = self.__PBT.Seleccionar_columnas_pd(
            df=self.__df_vuelos, cols_elegidas=[*self.__cols_df_vuelo]
        )

from datetime import datetime
from typing import List
from loguru import logger
from Utils import general_functions as gf

class Servicios:
    def __init__(self, __config, __menu_servicios=None, __PBT=None):
        """Constructor de clase

        Args:
            __config (dict): Diccionario de configuración del proyecto
            __PBT (class) : Clase que contiene métodos para la manipulación de la fuente de información de Servicios
        """
        self.__config = __config
        self.__menu_servicios = __menu_servicios
        self.__PBT = __PBT
        self.__servicios_adicionales = []
        self.__costo_total_servicios = 0.0
        self.__verificado = False
        self.__cols_df_servicios = self.__config["directorio_servicios"]["dict_cols"]
        self.__df_servicios = self._leer_info_servicios()

    def mostrar_menu(self):
        eleccion = self.__config["Menu"]["menu_opcion"][6]
        gf.mostrar_menu_personalizado(eleccion, self.__menu_servicios)

    def _leer_info_servicios(self) -> dict:
        """
        Lee los datos de los servicios desde el archivo Excel configurado.
        :return: DataFrame con la información de los servicios.
        """
        logger.info("Leyendo información de servicios desde el archivo configurado...")
        lector_insumo = gf.ExcelReader(path=self.__config["path_insumos"])
        df_info_servicios = lector_insumo.Lectura_simple_excel(
            nom_insumo=self.__config["directorio_servicios"]["nom_base"],
            nom_hoja=self.__config["directorio_servicios"]["nom_hoja"],
        )
        logger.info("Información de servicios cargada correctamente.")
        print("")
        return df_info_servicios

    def get_servicios(self):
        """
        Proporciona el DataFrame con los datos de los servicios.
        :return: DataFrame de servicios.
        """
        return self.__df_servicios

    def ejecutar_proceso_servicios(self):
        opcion_ingresada = input("Ingresa la opción a ejecutar:\n ")
        resultado = self.ejecutar_proceso(opcion_ingresada)
        return resultado

    def administrar_servicios(self):
        df_select = self.__PBT.Seleccionar_columnas_pd(
            df=self.__df_servicios, cols_elegidas=[*self.__cols_df_servicios]
        )

    def calcular_costo_total(self):
        """
        Calcula el costo total de los servicios asignados.
        :return: Costo total.
        """
        return sum(self.__costo_total_servicios)

    def verificar_servicio(self):
        """
        Marca los servicios como verificados.
        """
        self.__verificado = True
        logger.info("Servicio verificado correctamente.")

    def asignar_servicio(self, servicio, costo):
        """
        Asigna un nuevo servicio adicional y actualiza el costo total.
        Args:
            servicio (str): Nombre del servicio.
            costo (float): Costo del servicio.
        """
        self.__servicios_adicionales.append(servicio)
        self.__costo_total_servicios += costo
        logger.info(f"Servicio '{servicio}' asignado correctamente. Costo actualizado: {self.__costo_total_servicios}.")

    def eliminar_servicio(self, servicio):
        """
        Elimina un servicio adicional y ajusta el costo total.
        Args:
            servicio (str): Nombre del servicio a eliminar.
        """
        if servicio in self.__servicios_adicionales:
            self.__servicios_adicionales.remove(servicio)
            logger.info(f"Servicio '{servicio}' eliminado correctamente.")
        else:
            logger.warning(f"El servicio '{servicio}' no se encuentra en los servicios adicionales.")

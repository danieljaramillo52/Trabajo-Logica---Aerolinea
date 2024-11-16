from datetime import datetime
from typing import List
from loguru import logger
import general_functions as gf


class Hangar:
    def __init__(self, __config, __menu_hangar=None, __PBT=None):
        """Constructor de clse

        Args:
            __config (dict): Diccionario de configuración del proyecto
            __PBT (class) : Clase que contiene métodos para la manipulación de la fuente de infromación de Aviones
        Returns:
            _type_: _description_
        """
        self.__config = __config
        self.__menu_hangar = __menu_hangar
        self.__PBT = __PBT
        self.__cols_df_avion = self.__config["directorio_aviones"]["dict_cols"]
        self.__df_aviones = self._leer_info_avion()
        

    def mostrar_menu(self):
        eleccion = self.__config["Menu"]["menu_opcion"][1]
        gf.mostrar_menu_personalizado(eleccion,self.__menu_hangar)    
    
    def _leer_info_avion(self) -> dict:
        """
        Lee los datos de los aviones desde el archivo Excel configurado.
        :return: DataFrame con la información de los aviones.
        """
        logger.info("Leyendo información de aviones desde el archivo configurado...")
        lector_insumo = gf.ExcelReader(path=self.__config["path_insumos"])
        df_info_avion = lector_insumo.Lectura_simple_excel(
            nom_insumo=self.__config["directorio_aviones"]["nom_base"],
            nom_hoja=self.__config["directorio_aviones"]["nom_hoja"],
        )
        logger.info("Información de aviones cargada correctamente.")
        print("")
        return df_info_avion  
    
    def get_aviones(self):
        """
        Proporciona el DataFrame con los datos de los aviones.
        :return: DataFrame de aviones.
        """
        return self.__df_aviones
     
    def ejecutar_proceso_hangar(self):            
        opcion_ingresada = input("Ingresa la opción a ejecutar:\n ")
        resultado = self.ejecutar_proceso(opcion_ingresada)
        return resultado
    
    def administrar_aviones(self):
        df_select = self.__PBT.Seleccionar_columnas_pd(
            df=self.__df_aviones, cols_elegidas=[*self.__cols_df_avion]
        )     

class Avion:
    def __init__(self, __config, __menu_avion=None, matricula=None):
        """
        Inicializa una instancia de Avion para operar sobre un DataFrame existente.
        Puede utilizar la matrícula para buscar un avión específico o trabajar con el DataFrame completo.

        :param __config: Configuración con las columnas y otras opciones necesarias.
        :param __menu_avion: Menú relacionado con las opciones de avión.
        :param matricula: Matrícula del avión específico (opcional).
        """
        self.__menu_avion = __menu_avion
        self.__config = __config
        self.cols_direct = self.__config["directorio_aviones"]["dict_cols"]
        
        # Obtener el DataFrame de aviones desde Hangar
        self.__hangar_data = Hangar(self.__config)
        self.__df_info_hangar = self.__hangar_data.get_aviones()
        
        if matricula:
            self.matricula = matricula
            self.avion_data = self.__df_info_hangar[
                self.__df_info_hangar[self.cols_direct["matricula"]] == matricula
            ]
        else:
            self.matricula = None
            self.avion_data = None


    def mostrar_menu(self):
        eleccion = self.__config["Menu"]["menu_opcion"][1]
        gf.mostrar_menu_personalizado(eleccion,self.__menu_avion)    
           
    def ejecutar_proceso_avion(self):            
        opcion_ingresada = input("Ingresa la opción a ejecutar:\n ")
        resultado = self.ejecutar_proceso(opcion_ingresada)
        return resultado

            
    def ejecutar_proceso(self, opcion: str) -> bool:
        """
        Ejecuta la opción seleccionada por el usuario y devuelve si debe continuar gestionando procesos.

        :param opcion: Opción seleccionada por el usuario.
        :return: True si se desea continuar, False si se regresa al menú principal.
        """
        opciones = {
            "1": self.obtener_informacion_avion,
            "2": self._actualizar_horas_vuelo,
            "3": self.realizar_mantenimiento,
            "4": lambda: print(Avion.aviones_necesitan_mantenimiento(self.df_info_avi)),
            "5": lambda: print(Avion.aviones_disponibles(self.df_info_avi)),
            "0": lambda: False  # Salir del menú
        }
        if opcion in opciones:
            if opcion == "0":  # Opción para salir directamente
                return False
            else:
                resultado = opciones[opcion]()
                print("Proceso terminado. \n")
                return  True


    def obtener_informacion_avion(self):
        """
        Devuelve la información completa de un avión específico según su matrícula.
        """
        if self.avion_data is not None:
            return print(self.avion_data)
        else:
            return "No se ha especificado una matrícula o el avión no existe en el DataFrame."

    def _actualizar_horas_vuelo(self, horas):
        """
        Actualiza las horas de vuelo de un avión específico.

        :param horas: Número de horas de vuelo para actualizar.
        """
        if self.avion_data is not None:
            self.df_info_avi.loc[
                self.df_info_avi[self.cols_direct["matricula"]] == self.matricula,
                "horas_vuelo",
            ] += horas
            print(
                f"Horas de vuelo actualizadas para el avión con matrícula {self.matricula}."
            )
        else:
            print(
                "No se ha especificado una matrícula o el avión no existe en el DataFrame."
            )

    def realizar_mantenimiento(self):
        """
        Marca el avión como mantenido, actualizando las horas desde el último mantenimiento a 0.
        """
        if self.avion_data is not None:
            self.df_info_avi.loc[
                self.df_info_avi[self.cols_direct["matricula"]] == self.matricula,
                "horas_ultimo_mantenimiento",
            ] = 0
            self.df_info_avi.loc[
                self.df_info_avi[self.cols_direct["matricula"]] == self.matricula,
                "necesita_mantenimiento",
            ] = False
        else:
            print(
                "No se ha especificado una matrícula o el avión no existe en el DataFrame."
            )

    @staticmethod
    def aviones_necesitan_mantenimiento(df):
        """
        Devuelve un DataFrame con los aviones que necesitan mantenimiento.

        :param df: DataFrame que contiene la información de los aviones.
        :return: DataFrame filtrado con los aviones que necesitan mantenimiento.
        """
        return df[df["necesita_mantenimiento"] == True]

    @staticmethod
    def aviones_disponibles(df):
        """
        Devuelve un DataFrame con los aviones disponibles.

        :param df: DataFrame que contiene la información de los aviones.
        :return: DataFrame filtrado con los aviones disponibles.
        """
        return df[df["disponible"] == True]

    def verificar_mantenimiento(self):
        return self.avion_data["necesita_mantenimiento"].iloc[0] or (
            self.avion_data["horas_vuelo"].iloc[0]
            - self.avion_data["horas_ultimo_mantenimiento"].iloc[0]
            >= 400
        )

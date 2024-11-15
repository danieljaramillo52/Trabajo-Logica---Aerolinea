from datetime import datetime
from typing import List
from loguru import logger

class HangarAviones:
    def __init__(self, __config, __df_aviones, __PBT):
        """Constructor de clse

        Args:
            __config (dict): Diccionario de configuración del proyecto
            __df_aviones (pd.Dataframe): Dataframe con la información de aviones
            __PBT (class) : Clase que contiene métodos para la manipulación de la fuente de infromación de Aviones
        Returns:
            _type_: _description_
        """
        self.__config = __config
        self.__df_aviones = __df_aviones
        self.__PBT = __PBT

        self.cols_df_avion = self.__config["directorio_aviones"]["dict_cols"]

    def administrar_aviones(self):
        
        df_select = self.__PBT.Seleccionar_columnas_pd(
            df=self.__df_aviones, cols_elegidas=[*self.cols_df_avion]
        )

    def mostrar_menu(self):
        """Muestra el menú de opciones al usuario y ejecuta la opción seleccionada."""
        while True:
            print("\nMenú de Opciones:")
            print("4. Ver aviones que necesitan mantenimiento")
            print("5. Ver aviones disponibles")
            print("0. Salir")

            opcion = input("Seleccione una opción: ")
            self.ejecutar_proceso(opcion)

class Avion:
    def __init__(self, __df_info_avion, __config, matricula=None):
        """
        Inicializa una instancia de Avion para operar sobre un DataFrame existente.
        Puede utilizar la matrícula para buscar un avión específico o trabajar con el DataFrame completo.

        :param df_info_avion: DataFrame que contiene la información de los aviones.
        :param config: Configuración con las columnas y otras opciones necesarias.
        :param matricula: Matrícula del avión específico (opcional).
        """
        self.df_info_avi = __df_info_avion
        self.config = __config
        self.cols_direct = self.config["directorio_aviones"]["dict_cols"]

        if matricula:
            self.matricula = matricula
            self.avion_data = self.df_info_avi[
                self.df_info_avi[self.cols_direct["matricula"]] == matricula
            ]
        else:
            self.matricula = None
            self.avion_data = None

    def mostrar_menu(self):
            #Meter en función
            menu = self.config["Opciones"]["Avion"]["string_menu"]
            for opcion, texto in menu.items():
                print(f"{opcion}. {texto}")
            opcion_ingresada = input("Ingresa la opción a ejecutar: ")
            opcion = self.ejecutar_proceso(opcion_ingresada)
            return opcion
            

    def ejecutar_proceso(self, opcion):
        """Ejecuta la opción seleccionada por el usuario."""
        if opcion == "1":
            print(self.obtener_informacion_avion())
            print("Proceso terminado")
            Validador = input("Quieres gestionar otro proceso del avion? (si/no)")
            if Validador.lower() == "si":
                return True
            else:
                print("Ha sido redirigido al menu principal ...")
                return False
        elif opcion == "2":
            horas = float(input("Ingrese el número de horas de vuelo a actualizar: "))
            self.actualizar_horas_vuelo(horas)
            return True
        elif opcion == "3":
            self.realizar_mantenimiento()
            print("Mantenimiento realizado.")
            return True
        elif opcion == "4":
            print(Avion.aviones_necesitan_mantenimiento(self.df_info_avi))
            return True
        elif opcion == "5":
            print(Avion.aviones_disponibles(self.df_info_avi))
            return True
        elif opcion == "0" : 
            return False
        else:
            print("Opción no válida. Por favor, seleccione una opción del menú.")

    def obtener_informacion_avion(self):
        """
        Devuelve la información completa de un avión específico según su matrícula.
        """
        if self.avion_data is not None:
            return self.avion_data
        else:
            return "No se ha especificado una matrícula o el avión no existe en el DataFrame."

    def actualizar_horas_vuelo(self, horas):
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

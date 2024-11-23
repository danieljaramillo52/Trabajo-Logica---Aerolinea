from datetime import datetime
from typing import List
from loguru import logger
import general_functions as gf
import pandas as pd
from loguru import logger


class Hangar:
    def __init__(self, __config, __menu_hangar=None, __PBT=None):
        """
        Constructor de la clase Hangar.

        Args:
            __config (dict): Diccionario de configuración del proyecto.
            __menu_hangar (opcional): Menú específico del hangar.
            __PBT (opcional): Clase con métodos para manipular la información de los aviones.
        """
        self.__config = __config
        self.__menu_hangar = __menu_hangar
        self.__PBT = __PBT
        self.__eleccion = self.__config["Menu"]["menu_opcion"]["2"]
        self.__cols_df_avion = self.__config["directorio_aviones"]["dict_cols"]
        self.__dict_mensajes_filtro = self.__config["directorio_aviones"][
            "dict_mensajes"
        ]["mensajes"]
        # Inicializa __df_aviones correctamente
        self.__df_aviones = self._leer_info_avion()

    @property
    def df_aviones(self):
        """Propiedad para acceder al DataFrame de aviones."""
        return self.__df_aviones

    @df_aviones.setter
    def df_aviones(self, value):
        """Setter para validar que el valor asignado sea un DataFrame."""
        if not isinstance(value, pd.DataFrame):
            raise ValueError("El valor de df_aviones debe ser un DataFrame.")
        self.__df_aviones = value

    # Propiedad para la configuración    
    @property
    def config(self):
        return self.__config

    @property
    def dict_mensajes(self):
        return self.__dict_mensajes_filtro

    # Propiedad para las columnas del DataFrame
    @property
    def cols_df_avion(self):
        return self.__cols_df_avion

    @property
    def PBT(self):
        return self.__PBT

    def _leer_info_avion(self) -> pd.DataFrame:
        """
        Lee los datos de los aviones desde el archivo Excel configurado.

        Returns:
            pd.DataFrame: DataFrame con la información de los aviones.
        """
        config_dir_avns = self.config["directorio_aviones"]
        logger.info("Leyendo información de aviones")

        lector_insumo = gf.ExcelReader(path=self.config["path_insumos"])

        df_info_avion = lector_insumo.Lectura_simple_excel(
            nom_insumo=config_dir_avns["nom_base"],
            nom_hoja=config_dir_avns["nom_hoja"],
        )

        logger.info("Información de aviones cargada correctamente.\n")
        return df_info_avion

    def mostrar_menu(self):
        """
        Muestra el menú personalizado.
        """
        gf.mostrar_menu_personalizado(self.__eleccion, self.__menu_hangar)

    def ejecutar_proceso(self):
        """
        Ejecuta el proceso basado en la opción ingresada por el usuario.

        Returns:
            bool: Resultado del proceso ejecutado.
        """
        opcion_ingresada = input("Ingresa la opción a ejecutar: ")
        return self.ejecutar_proceso_hangar(opcion_ingresada)

    def tranformar_tipos_data(self):
        # Convertir columna al tipo necesario
        return self.PBT.Cambiar_tipo_dato_multiples_columnas_pd(
            base=self.df_aviones,
            list_columns=self.obtener_columnas_disponibles(),
            type_data=float,
        )
        
    def ejecutar_proceso_hangar(self, opcion: str) -> bool:
        """
        Ejecuta la opción seleccionada por el usuario.

        Args:
            opcion (str): Opción seleccionada.

        Returns:
            bool: True si debe continuar, False si debe detenerse.
        """  
        self.df_aviones = self.tranformar_tipos_data() 
        
        opciones = {
            "1": self._generar_reporte_estado_general,
            "2": self._filtrar_por_operacion_elegida,
            "3": self._resumen_por_tipo,
            "4": self._agregar_avion_al_hangar,
            "5": self._eliminar_avion_hangar,
            "0": lambda: False,  # Salir del menú
        }
        
        return gf.procesar_opcion(opcion=opcion, opciones=opciones)

    def _calcular_totales(self, df):
        """
        Calcula los totales de aviones, disponibles y en mantenimiento.

        Args:
            df (pd.DataFrame): DataFrame con los datos de los aviones.

        Returns:
            dict: Diccionario con los totales calculados.
        """
        cols = self.cols_df_avion
        total_aviones = len(df)
        num_disponibles = len(df[df[cols["disponible"]] == "VERDADERO"])
        num_mantenimiento = len(df[df[cols["necesita_mantenimiento"]] == "VERDADERO"])

        return {
            "Total aviones en hangar": total_aviones,
            "Número disponibles": num_disponibles,
            "Número necesitan mantenimiento": num_mantenimiento,
        }

    def _calcular_porcentajes(self, totales):
        """
        Calcula los porcentajes de aviones disponibles y en mantenimiento.

        Args:
            totales (dict): Totales calculados previamente.

        Returns:
            dict: Diccionario con los porcentajes calculados.
        """
        total_aviones = totales["Total aviones en hangar"]
        porcentaje_disponibles = (totales["Número disponibles"] / total_aviones) * 100
        porcentaje_mantenimiento = (totales["Número necesitan mantenimiento"] / total_aviones) * 100

        return {
            "Porcentaje disponibles (%)": porcentaje_disponibles,
            "Porcentaje necesitan mantenimiento (%)": porcentaje_mantenimiento,
        }

    def _calcular_estadisticas_horas(self, df):
        """
        Calcula estadísticas relacionadas con las horas de vuelo.

        Args:
            df (pd.DataFrame): DataFrame con los datos de los aviones.

        Returns:
            dict: Diccionario con las estadísticas de horas de vuelo.
        """
        cols = self.cols_df_avion
        horas_promedio_vuelo = df[cols["horas_vuelo"]].astype(int).mean()
        avion_mas_horas = df.loc[df[cols["horas_vuelo"]].idxmax(), cols["matricula"]]
        avion_menos_horas = df.loc[df[cols["horas_vuelo"]].idxmin(), cols["matricula"]]

        return {
            "Horas promedio de vuelo": horas_promedio_vuelo,
            "Avión con más horas de vuelo": avion_mas_horas,
            "Avión con menos horas de vuelo": avion_menos_horas,
        }

    def _calcular_capacidad_y_peso(self, df):
        """
        Calcula la capacidad total de pasajeros y el peso máximo cargable del hangar.

        Args:
            df (pd.DataFrame): DataFrame con los datos de los aviones.

        Returns:
            dict: Diccionario con la capacidad y peso total del hangar.
        """
        cols = self.cols_df_avion
        capacidad_total = df[cols["capacidad_pasajeros"]].sum()
        peso_maximo_total = df[cols["peso_maximo_carga"]].sum()

        return {
            "Capacidad total (pasajeros)": capacidad_total,
            "Peso máximo cargable total (kg)": peso_maximo_total,
        }

    def _generar_reporte_estado_general(self):
        """
        Genera un reporte del estado general del hangar dividiendo las responsabilidades.

        Returns:
            pd.DataFrame: DataFrame con el reporte generado.
        """
        df = self.df_aviones

        # Cálculos divididos en funciones
        totales = self._calcular_totales(df)
        porcentajes = self._calcular_porcentajes(totales)
        estadisticas_horas = self._calcular_estadisticas_horas(df)
        capacidad_y_peso = self._calcular_capacidad_y_peso(df)

        # Combina todos los cálculos
        reporte = {**totales, **porcentajes, **estadisticas_horas, **capacidad_y_peso}

        # Crear DataFrame para el reporte
        reporte_df = pd.DataFrame.from_dict(data=reporte, orient="index", columns=["valor"])

        # Mostrar el reporte en consola
        print(f"\nReporte Ampliado del Estado General del Hangar\n{'='*50}")
        print(reporte_df)
        print(f"{'='*50}\n")

        return reporte_df


    def obtener_config_operaciones(self):
        """
        Obtiene la configuración de operaciones desde el archivo de configuración.

        Returns:
            dict: Diccionario con las operaciones configuradas.
        """
        return self.config["directorio_aviones"]["config_operaciones"]

    def obtener_columnas_disponibles(self):
        """
        Obtiene la lista de columnas numéricas disponibles para filtrar.

        Returns:
            list: Lista de nombres de columnas disponibles.
        """
        return list(self.config["directorio_aviones"]["dict_cols_num"].values())

    def mostrar_opciones_columnas(self, columnas):
        """
        Muestra las opciones de columnas disponibles al usuario.

        Args:
            columnas (list): Lista de columnas disponibles.
        """
        mensaje = self.dict_mensajes["columnas_disponibles"]
        print(f"\n{mensaje}")
        for i, col in enumerate(columnas, start=1):
            print(f"{i}: {col}")

    def solicitar_opcion_usuario(self, rango):
        """
        Solicita al usuario que elija una opción dentro de un rango válido.

        Args:
            rango (range): Rango de valores permitidos.

        Returns:
            int: Opción seleccionada por el usuario.
        """

        mensaje_opcion = self.dict_mensajes["ingresa_opcion"]
        mensaje_error = self.dict_mensajes["opcion_no_valida"]
        mensaje_entrada_error = self.dict_mensajes["entrada_no_valida"]

        while True:
            try:
                opcion = int(input(f"\n{mensaje_opcion} "))
                if opcion in rango:
                    return opcion - 1  # Ajustar a índice base 0
                else:
                    print(mensaje_error)
            except ValueError:
                print(mensaje_entrada_error)

    def solicitar_operacion(self, operaciones):
        """
        Solicita al usuario que seleccione una operación de entre las disponibles.

        Args:
            operaciones (dict): Diccionario de operaciones disponibles.

        Returns:
            str: Clave de la operación seleccionada.
        """
        mensaje_seleccione = self.dict_mensajes["operacion_seleccione"]
        mensaje_error = self.dict_mensajes["operacion_no_valida"]

        print(f"\n{mensaje_seleccione}")
        print("")
        for key, description in operaciones.items():
            print(f"{key}: {description}")

        while True:
            operacion = input("\nIngrese la operación que desea aplicar: ")
            if operacion in operaciones:
                return operacion
            else:
                print(f"{mensaje_error} {list(operaciones.keys())}")

    def realizar_filtro(self, columna, operacion):
        """
        Realiza el filtro sobre el DataFrame según la operación seleccionada.

        Args:
            columna (str): Nombre de la columna a filtrar.
            operacion (str): Operación seleccionada por el usuario.

        Returns:
            pd.DataFrame: DataFrame filtrado.
        """
        if operacion == "entre_a_b_valores":
            valor_min = float(input(f"{self.dict_mensajes['ingrese_valor_min']} "))
            valor_max = float(input(f"{self.dict_mensajes['ingrese_valor_max']} "))
            return self.PBT.Filtrar_por_operacion(
                df=self.df_aviones,
                columna=columna,
                operacion=operacion,
                valor_min=valor_min,
                valor_max=valor_max,
            )
        else:
            valor_umbral = float(input(f"{self.dict_mensajes['ingrese_umbral']} "))
            return self.PBT.Filtrar_por_operacion(
                df=self.df_aviones,
                columna=columna,
                operacion=operacion,
                valor_umbral=valor_umbral,
            )

    def mostrar_resultados(self, columna, operacion, df_filtrado):
        """
        Muestra los resultados del filtro al usuario.

        Args:
            columna (str): Nombre de la columna filtrada.
            operacion (str): Operación realizada.
            df_filtrado (pd.DataFrame): DataFrame con los resultados.
        """
        mensaje_resultados = self.dict_mensajes["resultados_filtro"]
        list_col = [
            self.cols_df_avion["matricula"],
            self.cols_df_avion["tipo"],
            columna,
        ]

        print(f"\n{mensaje_resultados} '{columna}'")
        print(f"Operación: {operacion}")
        print(df_filtrado[list_col])
        
        return df_filtrado[list_col]

    def exportar_filtrado(self, df):
        config_report = self.config["Resultados"]["repor_gen_hangar"]
        return gf.exportar_a_excel(
            df=df,
            ruta_guardado=config_report["path_base"],
            nom_base=config_report["nom_base"],
            nom_hoja=config_report["nom_hoja"],
        )

    def _filtrar_por_operacion_elegida(self):
        """
        Filtra el DataFrame según la operación elegida por el usuario.
        """
        config_operaciones = self.obtener_config_operaciones()
        columnas_disponibles = self.obtener_columnas_disponibles()

        # Mostrar opciones y solicitar entrada
        self.mostrar_opciones_columnas(columnas_disponibles)
        columna_idx = self.solicitar_opcion_usuario(
            range(1, len(columnas_disponibles) + 1)
        )
        columna = self.cols_df_avion[columnas_disponibles[columna_idx]]

        operacion = self.solicitar_operacion(config_operaciones)

        # Realizar el filtro
        df_filtrado = self.realizar_filtro(columna, operacion)

        # Mostrar resultados
        df_select = self.mostrar_resultados(
            columnas_disponibles[columna_idx], operacion, df_filtrado
        )
        self.exportar_filtrado(df=df_select)
    
    def _resumen_por_tipo(self) -> pd.DataFrame:
        """
        Genera un resumen agrupado por el tipo de avión.

        Returns:
            pd.DataFrame: DataFrame con el resumen por tipo.
        """
        cols = self.cols_df_avion
        resumen = (
            self.df_aviones.groupby(cols["tipo"])
            .agg(
                total_aviones=("matricula", "count"),
                horas_promedio_vuelo=(cols["horas_vuelo"], "mean"),
                capacidad_total=("capacidad_pasajeros", "sum"),
            )
            .reset_index()
        )
        print("\nResumen por tipo de avión:")
        print(resumen)
        return resumen

    def _agregar_avion_al_hangar():
        pass
    
    def _eliminar_avion_hangar():
        pass
        
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
        self.__eleccion = self.__config["Menu"]["menu_opcion"]["1"]
        self.cols_direct = self.__config["directorio_aviones"]["dict_cols"]

        # Obtener el DataFrame de aviones desde Hangar
        self.__hangar_data = Hangar(self.__config)
        self.__df_info_hangar = self.__hangar_data.df_aviones

        if matricula:
            self.matricula = matricula
            self.avion_data = self.__df_info_hangar[
                self.__df_info_hangar[self.cols_direct["matricula"]] == matricula
            ]
        else:
            self.matricula = None
            self.avion_data = None

    def mostrar_menu(self):
        eleccion = self.__eleccion
        gf.mostrar_menu_personalizado(eleccion, self.__menu_avion)

    def ejecutar_proceso(self):
        opcion_ingresada = input("\n Ingresa la opción a ejecutar: \n\n ")
        resultado = self.ejecutar_proceso_avion(opcion_ingresada)
        return resultado

    def ejecutar_proceso_avion(self, opcion: str) -> bool:
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
            "0": lambda: False,  # Salir del menú
        }
        resultado = gf.procesar_opcion(opcion=opcion, opciones=opciones)

        return resultado

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


class Mantenimiento:
    def __init__(self, __config, __menu_mantenimiento=None):
        self.__config = __config
        self.__menu_mantenimiento = __menu_mantenimiento

    def mostrar_menu(self):
        eleccion = self.__config["Menu"]["menu_opcion"][8]
        gf.mostrar_menu_personalizado(eleccion, self.__menu_empleado)

    def ejecutar_proceso(self):
        opcion_ingresada = input("Ingresa la opción a ejecutar:\n ")
        resultado = self.ejecutar_proceso_pasajero(opcion_ingresada)
        return resultado

    def ejecutar_proceso_pasajero(self, opcion: str) -> bool:
        """
        Ejecuta la opción seleccionada por el usuario y devuelve si debe continuar gestionando procesos.

        :param opcion: Opción seleccionada por el usuario.
        :return: True si se desea continuar, False si se regresa al menú principal.
        """
        opciones = {
            "1": self.metodo1,
            "2": self.metodo2,
            "3": self.realizar_mantenimiento,
            "4": 1,
            "5": 2,
            "0": 3,
        }
        if opcion in opciones:
            if opcion == "0":  # Opción para salir directamente
                return False
            else:
                resultado = opciones[opcion]()
                print("Proceso terminado. \n")
                return True

    def metodo1():
        pass

    def metodo2():
        pass

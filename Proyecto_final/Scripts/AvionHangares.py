from datetime import datetime
from typing import List
from loguru import logger
import general_functions as gf
import pandas as pd
import numpy as np
from loguru import logger
from random import randint


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
            "4": self._agregar_avion,
            "5": self._depurar_hangar,
            "6": self._eliminar_avion_hangar,
            "7": self._exportar_hangar,
            "0": lambda: False,  # Salir del menú
        }

        return gf.procesar_opcion(opcion=opcion, opciones=opciones)

    def _exportar_hangar(self):
        """Exporta el hangar de aviones luego de los cambios.}"""
        hangar_expotar = self.df_aviones
        hangar_expotar.to_excel("Resultados/aviones_compania_final.xlsx", index=False)

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
        porcentaje_mantenimiento = (
            totales["Número necesitan mantenimiento"] / total_aviones
        ) * 100

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
        reporte_df = pd.DataFrame.from_dict(
            data=reporte, orient="index", columns=["valor"]
        )

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

    def _agregar_avion(self):
        """
        Agrega un avión al DataFrame del hangar.

        Args:
            avion (Avion): Instancia de la clase Avion que será añadida.
        """
        dict_data_nuevos_aviones = self.config["directorio_aviones"][
            "aviones_ingresar"
        ][randint(1, 10)]

        avion = Avion(config=self.config, menu_avion=None, **dict_data_nuevos_aviones)

        # Convertir los atributos del avión a un formato adecuado
        valores = avion.atributos_a_numpy_array()

        # Crear una nueva fila como DataFrame
        nueva_fila = pd.DataFrame([valores], columns=self.df_aviones.columns)

        # Agregar la nueva fila al DataFrame existente
        self.df_aviones = pd.concat([self.df_aviones, nueva_fila], ignore_index=True)

        print(f"El avión con matrícula {avion.matricula} ha sido agregado al hangar.")

    def _depurar_hangar(self):
        """
        Elimina aviones duplicados del DataFrame del hangar, manteniendo la coincidencia más reciente.

        Este método utiliza la funcionalidad de eliminación de duplicados de pandas para
        asegurarse de que no haya registros duplicados de aviones en el hangar.
        Solo se conserva la última aparición de cada avión según su matrícula u otros identificadores.

        Returns:
            pd.DataFrame: El DataFrame del hangar depurado, sin aviones duplicados.
        """
        logger.info("Hangar depurado correctamente. ")
        self.df_aviones = self.df_aviones.drop_duplicates(keep="last")
        return self.df_aviones

    def _eliminar_avion_hangar(self):
        """
        Elimina un avión del DataFrame del hangar según la matrícula proporcionada.

        Este método solicita al usuario una matrícula específica para identificar y eliminar un avión del DataFrame. La eliminación se realiza creando un nuevo DataFrame que excluye el avión con la matrícula indicada. Luego, se actualiza el DataFrame original del hangar.

        Returns:
            pd.DataFrame: El DataFrame actualizado después de eliminar el avión.
        """

        matricula = input("Ingrese una matricula de un avión para eliminar: \n")

        self.df_aviones_mod = self.df_aviones[
            self.cols_df_avion["matricula"] != matricula
        ]

        self.df_aviones = self.df_aviones_mod

        logger.info("Avion eliminado correctamente")

        return self.df_aviones


class Avion:
    """
    Clase que representa un avión con sus características y comportamientos asociados.

    Esta clase encapsula los atributos de un avión, como matrícula, tipo, modelo, fabricante,
    propietario, y otros detalles operativos, proporcionando métodos para interactuar con
    estos atributos. Incluye validaciones mediante propiedades (`property`) para asegurar
    que los valores asignados sean válidos.

    Attributes:
        config (dict): Configuración general para el avión.
        matricula (str): Matrícula única del avión.
        tipo (str): Tipo del avión (por ejemplo, Carga, Pasajeros, etc.).
        modelo (str): Modelo del avión.
        fabricante (str): Nombre del fabricante del avión.
        propietario (str): Nombre del propietario del avión.
        horas_vuelo (int | float): Total de horas de vuelo acumuladas.
        capacidad_pasajeros (int): Número máximo de pasajeros.
        peso_maximo_carga (int | float): Peso máximo de carga permitida (kg).
        disponible (str): Estado de disponibilidad ("VERDADERO" o "FALSO").
        horas_ultimo_mantenimiento (int | float): Horas desde el último mantenimiento.
        necesita_mantenimiento (str): Indica si el avión requiere mantenimiento ("VERDADERO" o "FALSO").
    """

    def __init__(
        self,
        config,
        matricula,
        tipo,
        modelo,
        fabricante,
        propietario,
        horas_vuelo,
        capacidad_pasajeros,
        peso_maximo_carga,
        disponible,
        horas_ultimo_mantenimiento,
        necesita_mantenimiento,
        menu_avion=None,
    ):
        self.__config = config
        self.__menu_avion = menu_avion
        self.__matricula = matricula
        self.__tipo = tipo
        self.__modelo = modelo
        self.__fabricante = fabricante
        self.__propietario = propietario
        self.__horas_vuelo = horas_vuelo
        self.__capacidad_pasajeros = capacidad_pasajeros
        self.__peso_maximo_carga = peso_maximo_carga
        self.__disponible = disponible
        self.__horas_ultimo_mantenimiento = horas_ultimo_mantenimiento
        self.__necesita_mantenimiento = necesita_mantenimiento

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, value):
        self.config = value

    @property
    def matricula(self):
        return self.__matricula

    @matricula.setter
    def matricula(self, value):
        if not isinstance(value, str):
            raise ValueError("La matrícula debe ser una cadena.")
        self.__matricula = value

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, value):
        if not isinstance(value, str):
            raise ValueError("El tipo debe ser una cadena.")
        self.__tipo = value

    @property
    def modelo(self):
        return self.__modelo

    @modelo.setter
    def modelo(self, value):
        if not isinstance(value, str):
            raise ValueError("El modelo debe ser una cadena.")
        self.__modelo = value

    @property
    def fabricante(self):
        return self.__fabricante

    @fabricante.setter
    def fabricante(self, value):
        if not isinstance(value, str):
            raise ValueError("El fabricante debe ser una cadena.")
        self.__fabricante = value

    @property
    def propietario(self):
        return self.__propietario

    @propietario.setter
    def propietario(self, value):
        if not isinstance(value, str):
            raise ValueError("El propietario debe ser una cadena.")
        self.__propietario = value

    @property
    def horas_vuelo(self):
        return self.__horas_vuelo

    @horas_vuelo.setter
    def horas_vuelo(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Las horas de vuelo deben ser un número positivo.")
        self.__horas_vuelo = value

    @property
    def capacidad_pasajeros(self):
        return self.__capacidad_pasajeros

    @capacidad_pasajeros.setter
    def capacidad_pasajeros(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("La capacidad de pasajeros debe ser un entero positivo.")
        self.__capacidad_pasajeros = value

    @property
    def peso_maximo_carga(self):
        return self.__peso_maximo_carga

    @peso_maximo_carga.setter
    def peso_maximo_carga(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("El peso máximo de carga debe ser un número positivo.")
        self.__peso_maximo_carga = value

    @property
    def disponible(self):
        return self.__disponible

    @disponible.setter
    def disponible(self, value):
        if value not in ["VERDADERO", "FALSO"]:
            raise ValueError("Disponible debe ser 'VERDADERO' o 'FALSO'.")
        self._disponible = value

    @property
    def horas_ultimo_mantenimiento(self):
        return self.__horas_ultimo_mantenimiento

    @horas_ultimo_mantenimiento.setter
    def horas_ultimo_mantenimiento(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(
                "Las horas desde el último mantenimiento deben ser un número positivo."
            )
        self.__horas_ultimo_mantenimiento = value

    @property
    def necesita_mantenimiento(self):
        return self.__necesita_mantenimiento

    @necesita_mantenimiento.setter
    def necesita_mantenimiento(self, value):
        if value not in ["VERDADERO", "FALSO"]:
            raise ValueError("Necesita mantenimiento debe ser 'VERDADERO' o 'FALSO'.")
        self.__necesita_mantenimiento = value

    def atributos_a_numpy_array(self) -> np.ndarray:
        """
        Convierte los atributos públicos del avión en un arreglo unidimensional de NumPy.

        Este método utiliza introspección para acceder dinámicamente a los atributos de la
        instancia. Filtra los atributos excluyendo aquellos que comienzan con '_', ya que
        se consideran privados, y luego extrae sus valores usando la función `getattr`.

        Los pasos principales son:
            1. Obtener todos los atributos de la instancia usando `vars(self)`.
            2. Filtrar los atributos que no comienzan con '_'.
            3. Extraer los valores de los atributos filtrados con `getattr`.
            4. Convertir los valores a un arreglo unidimensional de NumPy con `dtype=object`.

        Returns:
            np.ndarray: Arreglo unidimensional que contiene los valores de los atributos
            públicos del avión.
        """

        return np.array(
            [getattr(self, attr) for attr in vars(self) if not attr.startswith("_")],
            dtype=object,
        )

    def mostrar_menu(self):
        eleccion = self.config["Menu"]["menu_opcion"]["1"]
        gf.mostrar_menu_personalizado(eleccion, self.__menu_avion)

    def ejecutar_proceso(self):
        opcion_ingresada = input("\n Ingresa la opción a ejecutar: ")
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
            "2": self.actualizar_horas_vuelo(
                horas=int(input("Ingrese el número de horas de vuelo a actualizar."))
            ),
            "3": self.verificar_disponibilidad,
            "4": self,
            "5": self,
            "0": lambda: False,  # Salir del menú
        }
        resultado = gf.procesar_opcion(opcion=opcion, opciones=opciones)

        return resultado

    def atributos_a_numpy_array(self) -> np.ndarray:
        """
        Convierte los atributos públicos del avión en un arreglo unidimensional de NumPy.

        Returns:
            np.ndarray: Arreglo unidimensional con los valores de los atributos públicos.
        """
        return np.array(
            [getattr(self, attr) for attr in vars(self) if not attr.startswith("_")],
            dtype=object,
        )

    def actualizar_horas_vuelo(self, horas: float):
        if not isinstance(horas, (int, float)) or horas < 0:
            raise ValueError("Las horas deben ser un número positivo.")
        self.horas_vuelo += horas
        print(f"Horas de vuelo actualizadas. Total actual: {self.horas_vuelo}")

    def verificar_mantenimiento(self) -> bool:
        necesita = self.necesita_mantenimiento == "VERDADERO" or (
            self.horas_vuelo - self.horas_ultimo_mantenimiento >= 400
        )
        print(
            f"El avión {self._matricula} {'necesita' if necesita else 'no necesita'} mantenimiento."
        )
        return necesita

    def obtener_informacion_avion(self) -> dict:
        info = {
            "Matrícula": self._matricula,
            "Tipo": self._tipo,
            "Modelo": self._modelo,
            "Fabricante": self._fabricante,
            "Propietario": self._propietario,
            "Horas de vuelo": self._horas_vuelo,
            "Capacidad de pasajeros": self._capacidad_pasajeros,
            "Peso máximo de carga (kg)": self._peso_maximo_carga,
            "Disponible": self._disponible,
            "Horas desde último mantenimiento": self._horas_ultimo_mantenimiento,
            "Necesita mantenimiento": self._necesita_mantenimiento,
        }
        print("Información detallada del avión:")
        for key, value in info.items():
            print(f"{key}: {value}")
        return info

    def verificar_disponibilidad(self) -> bool:
        disponible = self.disponible == "VERDADERO"
        print(
            f"El avión {self.matricula} {'está disponible' if disponible else 'no está disponible'}."
        )
        return disponible


class Mantenimiento:
    def __init__(self, __config, __menu_mantenimiento=None):
        """
        Constructor de la clase Mantenimiento.

        Args:
            __config (dict): Diccionario de configuración del sistema.
            __menu_mantenimiento (opcional): Configuración del menú relacionado con mantenimiento.
        """
        self.__config = __config
        self.__menu_mantenimiento = __menu_mantenimiento
        self.df_mantenimiento = self.cargar_datos_mantenimiento()

    def cargar_datos_mantenimiento(self):
        """
        Carga los datos de mantenimiento en un DataFrame.

        Returns:
            pd.DataFrame: DataFrame con la información de mantenimiento.
        """
        # Este es un ejemplo inicial, reemplazarlo con datos reales según sea necesario.
        data = {
            "Matrícula": ["ABC001", "ABC003", "ABC005", "ABC007"],
            "Tipo": ["Privado", "Privado", "Privado", "Privado"],
            "Modelo": [
                "Airbus A320",
                "Gulfstream G550",
                "Embraer Phenom 300",
                "Boeing 737",
            ],
            "Horas Vuelo": [2000, 1500, 3000, 4000],
            "Estado de Mantenimiento": [
                "Pendiente",
                "Pendiente",
                "Completo",
                "Pendiente",
            ],
            "Costo Mantenimiento Mínimo (USD)": [4000, 3600, 5600, 6400],
            "Costo Mantenimiento Completo (USD)": [5000, 4500, 7000, 8000],
            "Costo Mantenimiento Lujo (USD)": [10000, 9000, 14000, 16000],
        }
        return pd.DataFrame(data)

    def mostrar_menu(self):
        """
        Muestra el menú de mantenimiento.
        """
        eleccion = self.__config["Menu"]["menu_opcion"][8]
        gf.mostrar_menu_personalizado(eleccion, self.__menu_mantenimiento)

    def ejecutar_proceso(self):
        """
        Ejecuta el proceso principal del menú de mantenimiento.
        """
        opcion_ingresada = input("Ingresa la opción a ejecutar:\n ")
        resultado = self.ejecutar_proceso_pasajero(opcion_ingresada)
        return resultado

    def ejecutar_proceso_pasajero(self, opcion: str) -> bool:
        """
        Ejecuta la opción seleccionada por el usuario y devuelve si debe continuar gestionando procesos.

        Args:
            opcion (str): Opción seleccionada.

        Returns:
            bool: True si se desea continuar, False si se regresa al menú principal.
        """
        opciones = {
            "1": self.mostrar_datos_mantenimiento,
            "2": self.filtrar_por_estado,
            "3": self.calcular_costos_por_tipo,
            "4": self.actualizar_estado_mantenimiento,
            "0": lambda: False,  # Salir del menú
        }
        if opcion in opciones:
            if opcion == "0":  # Opción para salir directamente
                return False
            else:
                resultado = opciones[opcion]()
                print("Proceso terminado.\n")
                return True

    def mostrar_datos_mantenimiento(self):
        """
        Muestra todos los datos de mantenimiento en el DataFrame.
        """
        print("\nDatos de Mantenimiento:")
        print(self.df_mantenimiento)

    def filtrar_por_estado(self):
        """
        Filtra los aviones por estado de mantenimiento y muestra el resultado.
        """
        estado = input(
            "\nIngrese el estado de mantenimiento a filtrar (Pendiente/Completo): "
        )
        filtrado = self.df_mantenimiento[
            self.df_mantenimiento["Estado de Mantenimiento"] == estado
        ]
        if filtrado.empty:
            print(f"No se encontraron aviones con estado '{estado}'.")
        else:
            print(f"\nAviones con estado de mantenimiento '{estado}':")
            print(filtrado)

    def calcular_costos_por_tipo(self):
        """
        Calcula el costo total de mantenimiento por tipo de avión.
        """
        costos_por_tipo = self.df_mantenimiento.groupby("Tipo")[
            ["Costo Mantenimiento Completo (USD)"]
        ].sum()
        print("\nCostos de mantenimiento por tipo de avión:")
        print(costos_por_tipo)

    def actualizar_estado_mantenimiento(self):
        """
        Actualiza el estado de mantenimiento de un avión.
        """
        matricula = input(
            "\nIngrese la matrícula del avión para actualizar el estado de mantenimiento: "
        )
        nuevo_estado = input(
            "Ingrese el nuevo estado de mantenimiento (Pendiente/Completo): "
        )

        if matricula in self.df_mantenimiento["Matrícula"].values:
            self.df_mantenimiento.loc[
                self.df_mantenimiento["Matrícula"] == matricula,
                "Estado de Mantenimiento",
            ] = nuevo_estado
            print(
                f"El estado de mantenimiento del avión con matrícula {matricula} ha sido actualizado a '{nuevo_estado}'."
            )
        else:
            print(f"No se encontró un avión con la matrícula {matricula}.")

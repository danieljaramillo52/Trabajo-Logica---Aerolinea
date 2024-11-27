from loguru import logger
import general_functions as gf
from ModuloPasajeros import Pasajeros
from AvionHangares import Avion
from typing import Optional, List, Dict


class Vuelo:
    def __init__(self, config: dict, menu=None, __PBT=None):
        """
        Constructor de la clase Vuelo.

        Args:
            __config (dict): Diccionario de configuración del proyecto.
            __menu_vuelo (list, opcional): Menú relacionado con vuelos.
            __PBT (object, opcional): Clase para la manipulación de datos.
        """
        self.__config = config
        self.__menu_vuelo = menu
        self.__PBT = __PBT
        self.__pasajeros: List[Pasajeros] = []
        self.__avion: Optional[Avion] = None
        self.__peso_equipaje_total: float = 0.0
        self.__horas_vuelo_por_avion: Dict[str, float] = {}
        self.__verificado: bool = False

    @property
    def PBT(self) -> Optional[object]:
        return self.__PBT

    @property
    def config(self) -> dict:
        return self.__config

    def mostrar_menu(self) -> None:
        """
        Muestra el menú relacionado con vuelos.
        """
        eleccion = self.__config["Menu"]["menu_opcion"]["6"]
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
        return df_info_vuelos

    def calcular_peso_total_equipaje(self) -> float:
        """
        Calcula el peso total del equipaje de todos los pasajeros en el vuelo.
        :return: Peso total del equipaje.
        """
        self.__peso_equipaje_total = sum(pasajero.calcular_peso_total_equipaje() for pasajero in self.__pasajeros)
        logger.info(f"Peso total del equipaje calculado: {self.__peso_equipaje_total} kg")
        return self.__peso_equipaje_total

    def agregar_pasajero(self, pasajero: Pasajeros) -> None:
        """
        Agrega un pasajero al vuelo si hay capacidad disponible y el peso del equipaje no excede el límite permitido.
        
        Args:
            pasajero (Pasajero): Instancia de la clase Pasajero.
        """
        if not self.__avion:
            logger.error("No se puede agregar un pasajero sin asignar un avión al vuelo.")
            return

        if len(self.__pasajeros) >= self.__avion.capacidad_pasajeros:
            logger.warning("No se puede agregar al pasajero: capacidad de pasajeros excedida.")
            return

        peso_total = self.calcular_peso_total_equipaje() + pasajero.calcular_peso_total_equipaje()
        if peso_total > self.__avion.peso_maximo_equipaje:
            logger.warning("No se puede agregar al pasajero: peso del equipaje excedido.")
            return

        self.__pasajeros.append(pasajero)
        logger.info(f"Pasajero {pasajero.nombre} agregado al vuelo exitosamente.")

    def asignar_avion(self, avion: Avion) -> None:
        """
        Asigna un avión al vuelo.
        
        Args:
            avion (Avion): Instancia de la clase Avion.
        """
        if not avion.aviones_disponibles:
            logger.error("El avión no está disponible para asignar al vuelo.")
            return

        self.__avion = avion
        logger.info(f"Avión {avion.matricula} asignado al vuelo exitosamente.")

    def listar_pasajeros(self) -> None:
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

    def verificar_disponibilidad_avion(self) -> bool:
        """
        Verifica si el avión asignado está disponible.
        :return: True si el avión está disponible, False en caso contrario.
        """
        if self.__avion and self.__avion.aviones_disponibles:
            logger.info("El avión asignado está disponible para el vuelo.")
            return True
        logger.warning("El avión asignado no está disponible o no se ha asignado ningún avión.")
        return False

    def registrar_horas_vuelo(self, matricula: str, horas: float) -> None:
        """
        Registra las horas de vuelo del avión asignado al vuelo actual.
        
        Args:
            matricula (str): Matrícula del avión.
            horas (float): Número de horas que duró el vuelo.
        """
        if horas <= 0:
            logger.error("Las horas de vuelo deben ser un valor positivo.")
            return
        
        self.__horas_vuelo_por_avion[matricula] = self.__horas_vuelo_por_avion.get(matricula, 0) + horas
        logger.info(f"Se registraron {horas} horas para el avión con matrícula {matricula}.")

    def obtener_horas_vuelo(self, matricula: str) -> float:
        """
        Retorna las horas de vuelo acumuladas para el avión dado.
        
        Args:
            matricula (str): Matrícula del avión.
        
        Returns:
            float: Horas de vuelo acumuladas.
        """
        return self.__horas_vuelo_por_avion.get(matricula, 0.0)

    def ejecutar_proceso(self):
        """
        Ejecuta un proceso basado en la opción ingresada para los vuelos.
        """
        opcion_ingresada = input("Ingresa la opción a ejecutar:\n ")
        resultado = self.ejecutar_proceso_vuelo(opcion_ingresada)
        return resultado

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
        return list(self.config["directorio_vuelos"]["dict_cols_num"].values())
    
    def ejecutar_proceso_vuelo(self, opcion: str) -> bool:
        """
        Ejecuta la opción seleccionada por el usuario.

        Args:
            opcion (str): Opción seleccionada.

        Returns:
            bool: True si debe continuar, False si debe detenerse.
        """   
        opciones = {
            "1": lambda: print(f"Peso total del equipaje: {self.calcular_peso_total_equipaje()} kg"),
            "2": lambda: self.agregar_pasajero(self._solicitar_datos_pasajero()),
            "3": lambda: print(f"Pasajeros en el vuelo:\n{self.listar_pasajeros()}"),
            "4": lambda: self.asignar_avion(self._solicitar_datos_avion()),
            "5": lambda: print(f"Disponibilidad del avión: {'Disponible' if self.verificar_disponibilidad_avion() else 'No disponible'}"),
            "0": lambda: False,
        }
        
        return gf.procesar_opcion(opcion=opcion, opciones=opciones)

    def _solicitar_datos_pasajero(self) -> Pasajeros:
        """
        Solicita los datos de un pasajero para agregarlo al vuelo.
        Returns:
            Pasajero: Una instancia de la clase Pasajero creada a partir de los datos ingresados.
        """
        nombre = input("Ingrese el nombre del pasajero: ")
        documento_identidad = input("Ingrese el documento de identidad: ")
        try:
            edad = int(input("Ingrese la edad del pasajero: "))
            if edad <= 0:
                raise ValueError("La edad debe ser mayor que 0.")
        except ValueError as e:
            logger.error(f"Entrada inválida: {e}")


        return Pasajeros(nombre=nombre, documento_identidad=documento_identidad, edad=edad)

    def _solicitar_datos_avion(self) -> Avion:
        """
        Solicita los datos de un avión para asignarlo al vuelo.
        Returns:
            Avion: Una instancia de la clase Avion creada a partir de los datos ingresados.
        """
        matricula = input("Ingrese la matrícula del avión: ")
        capacidad = int(input("Ingrese la capacidad de pasajeros: "))
        peso_max = float(input("Ingrese el peso máximo de equipaje permitido: "))
        disponible = input("¿El avión está disponible? (s/n): ").lower() == "s"

        return Avion(matricula=matricula, capacidad_pasajeros=capacidad, peso_maximo_equipaje=peso_max, disponible=disponible)
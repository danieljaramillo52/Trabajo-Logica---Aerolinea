import config_path_routes
import general_functions as gf
from loguru import logger
from transformation_functions import PandasBaseTransformer as PBT
from Scripts.ModuloVuelo import Vuelo
from Servicios import Servicios
from AvionHangares import Avion, Hangar
from Scripts.ModuloEmpleado import Empleados, Empleado
from Pasajero import Pasajero
from typing import Dict


class GestionFBO:
    def __init__(self, config: Dict):
        """
        Constructor de la clase principal GestionFBO.
        param (config): Diccionario con la configuración inicial.
        """
        self.__config = config

    @property
    def config(self) -> Dict:
        """Return: Diccionario de configuración."""
        return self.__config

    @staticmethod
    def gestionar_ciclo(clase_instancia):
        """
        Encapsula el ciclo de ejecución para una instancia de clase.

        :param clase_instancia: Instancia de la clase que debe implementar los métodos
                                `mostrar_menu` y `ejecutar_proceso`.
        """
        if not hasattr(clase_instancia, "mostrar_menu") or not hasattr(
            clase_instancia, "ejecutar_proceso"
        ):
            raise AttributeError(
                "La instancia proporcionada debe tener los métodos 'mostrar_menu' y 'ejecutar_proceso'."
            )

        estado = True
        while estado:
            clase_instancia.mostrar_menu()
            estado = clase_instancia.ejecutar_proceso()

    def _gestionar_hangar(self, menu: dict):
        #matricula = input("Ingrese una matricula de la lista a consultar: ")
        hangar = Hangar(self.config(), menu, PBT)
        self.gestionar_ciclo(hangar)

    def _gestionar_empleado(self, menu: dict):
        matricula = input("Ingrese una matricula de la lista a consultar: ")
        empleados = Empleados(self.config(), menu, matricula)
        self.gestionar_ciclo(empleados)

    def _gestionar_tripulacion(self, menu: dict):
        matricula = input("Ingrese una matricula de la lista a consultar: ")
        avion = Avion(self.config(), menu, matricula)
        self.gestionar_ciclo(avion)

    def _gestionar_mantenimiento(self, menu: dict):
        matricula = input("Ingrese una matricula de la lista a consultar: ")
        avion = Avion(self.config(), menu, matricula)
        self.gestionar_ciclo(avion)

    def _gestionar_servicios(self, menu: dict):
        matricula = input("Ingrese una matricula de la lista a consultar: ")
        avion = Avion(self.config(), menu, matricula)
        self.gestionar_ciclo(avion)

    def _gestionar_vuelo(self, menu: dict):
        matricula = input("Ingrese una matricula de la lista a consultar: ")
        avion = Avion(self.config(), menu, matricula)
        self.gestionar_ciclo(avion)

    def _gestionar_pasajero(self, menu: dict):
        pasajero = Pasajero(self.config(), menu)
        self.gestionar_ciclo(pasajero)

    def _gestionar_avion(self, menu):
        matricula = input("Ingrese una matricula de la lista a consultar: ")
        avion = Avion(self.config(), menu, matricula)
        self.gestionar_ciclo(avion)

    def _menu_principal(self, dict_menus: dict):
        """
        Muestra el menú principal y permite al usuario seleccionar una opción.

        :param dict_menus: Diccionario que contiene los submenús asociados a cada opción.
        """
        dict_menu_principal = self.__config["Menu"]["menu_opcion"]
        mensaje_menu = self.__config["Menu"]["mensaje_principal"]
        opciones_validas = [(k) for k in dict_menu_principal.keys()]

        while True:
            print(mensaje_menu)
            try:
                opcion = input("Ingrese una opción: ")
                if opcion not in opciones_validas:
                    logger.info(
                        f"No has ingresado una opción válida. Por favor, selecciona entre las opciones disponibles: {opciones_validas}"
                    )
                elif opcion == "0":
                    logger.info("Saliendo del menú principal...")
                    break
                else:
                    self._ejecutar_opcion(opcion, dict_menus)
            except ValueError:
                logger.info("Entrada no válida. Por favor, ingresa un número.")

    def _ejecutar_opcion(self, opcion: int, dict_menus: dict):
        """
        Ejecuta la acción correspondiente a la opción seleccionada.

        :param opcion: Número de la opción seleccionada por el usuario.
        :param dict_menus: Diccionario que contiene los submenús asociados a cada opción.
        """
        submenus_acciones = {
            "1": ("Avion", self._gestionar_avion),
            "2": ("Hangar", self._gestionar_hangar),
            "3": ("Empleado", self._gestionar_empleado),
            "4": ("Tripulacion", self._gestionar_tripulacion),
            "5": ("Mantenimiento", self._gestionar_mantenimiento),
            "6": ("Servicios", self._gestionar_servicios),
            "7": ("Vuelo", self._gestionar_vuelo),
            "8": ("Pasajero", self._gestionar_pasajero),
        }

        if opcion in submenus_acciones:
            submenu, accion = submenus_acciones[opcion]
            menu = dict_menus.get(submenu, {})
            if menu:
                accion(menu)
            else:
                logger.warning(f"No se encontró información para el submenú: {submenu}")
        else:
            logger.error(f"Opción {opcion} no válida o sin acción asociada.")


class GenerarMenusFBO:
    def __init__(self, gestion_fbo: GestionFBO):
        """
        Constructor de la clase GenerarMenusFBO.
        :param gestion_fbo: Instancia de la clase GestionFBO para acceder a la configuración.
        """
        self.__gestion_fbo = gestion_fbo
        self.__config = self.__gestion_fbo.config()

        # Acceso directo a las claves necesarias
        self.__direc_menu = self.__config["directorio_menu"]
        self.__lector_insumos = gf.ExcelReader(path=self.__config["path_insumos"])

    def ejecutar_proceso_menus(self) -> Dict:
        """
        Ejecuta el proceso de carga y creación de menús.
        :return: Diccionario con los menús generados.
        """
        dict_dfs_menus = self._cargar_dfs_para_menus()
        dict_menus = self._crear_dict_menus(dict_dfs_menus)
        return dict_menus

    def _cargar_dfs_para_menus(self) -> Dict:
        """
        Carga los DataFrames necesarios para generar los menús.
        :return: Diccionario con los DataFrames cargados.
        """
        dict_df_menus = {}
        dict_hojas = self.__direc_menu["nom_hojas"]

        for cada_hoja in dict_hojas.values():
            if cada_hoja == self.__config["dict_constantes"]["Salir"]:
                continue
            else:
                dict_df_menus[cada_hoja] = self.__lector_insumos.Lectura_simple_excel(
                    nom_insumo=self.__direc_menu["nom_base"],
                    nom_hoja=cada_hoja,
                )
        return dict_df_menus

    def _crear_dict_menus(self, dict_menus: Dict) -> Dict:
        """
        Crea un diccionario de menús a partir de los DataFrames cargados.
        :param dict_menus: Diccionario con los DataFrames de los menús.
        :return: Diccionario con los menús generados.
        """
        dict_menu = {}
        for cada_clave, cada_df in dict_menus.items():
            dict_menu[cada_clave] = gf.Crear_diccionario_desde_dataframe(
                df=cada_df,
                col_clave=self.__direc_menu["cols"]["num_opcion"],
                col_valor=self.__direc_menu["cols"]["opciones"],
            )
        return dict_menu

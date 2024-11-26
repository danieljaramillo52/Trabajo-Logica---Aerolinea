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
        resultado = self.ejecutar_proceso_servicio(opcion_ingresada)
        return resultado

    def ejecutar_proceso_servicio(self, opcion: str) -> bool:
        """
        Ejecuta la opción seleccionada por el usuario.

        Args:
            opcion (str): Opción seleccionada.

        Returns:
            bool: True si debe continuar, False si debe detenerse.
        """  
        opciones = {
            "1": lambda: print(f"Costo total de los servicios: ${self.calcular_costo_total():.2f}"),
            "2": lambda: self.verificar_servicio() or print("Servicio marcado como verificado."),
            "3": lambda: self.asignar_servicio(input("Nombre del servicio: "), float(input("Costo del servicio: "))),
            "4": lambda: self.eliminar_servicio(input("Nombre del servicio a eliminar: ")) or print("Servicio eliminado correctamente."),
            "0": lambda: False,  # Opción para salir
        }

        return gf.procesar_opcion(opcion=opcion, opciones=opciones)

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

    def __registrar_actividad(self, descripcion):
        """
        Registra una actividad realizada en el sistema.
        
        Args:
            descripcion (str): Descripción de la actividad realizada.
        """
        if not hasattr(self, "__historial_actividades"):
            self.__historial_actividades = []
        self.__historial_actividades.append(descripcion)

    def suministrar_combustible(self, cantidad_litros, aeronave):
        """
        Registra el suministro de combustible para una aeronave.
        
        Args:
            cantidad_litros (float): Cantidad de litros suministrados.
            aeronave (Avion): Objeto que representa la aeronave.
        """
        if cantidad_litros > 0:
            self.__registrar_actividad(f"Suministrados {cantidad_litros:.2f} litros de combustible a la aeronave {aeronave.get_matricula()}.")
            logger.info(f"Suministrados {cantidad_litros:.2f} litros de combustible a la aeronave {aeronave.get_matricula()}.")
        else:
            logger.warning("Cantidad de combustible inválida. El suministro no puede ser negativo o cero.")

    def gestionar_carga_descarga(self, equipaje_total, vuelo):
        """
        Gestiona la carga y descarga de equipaje.
        
        Args:
            equipaje_total (float): Peso total del equipaje.
            vuelo (Vuelo): Objeto que representa el vuelo.
        """
        if equipaje_total > 0:
            self.__registrar_actividad(f"Carga de {equipaje_total:.2f} kg de equipaje completada para el vuelo {vuelo.get_numero_vuelo()}.")
            logger.info(f"Carga/descarga completada con {equipaje_total:.2f} kg de equipaje para el vuelo {vuelo.get_numero_vuelo()}.")
        else:
            logger.warning("Peso de equipaje inválido. Debe ser mayor que 0.")

    def asignar_puesto_estacionamiento(self, aeronave, puesto):
        """
        Asigna un puesto de estacionamiento a una aeronave.
        
        Args:
            aeronave (Avion): Objeto que representa la aeronave.
            puesto (str): Código o número del puesto de estacionamiento.
        """
        if not puesto:
            logger.warning("El puesto de estacionamiento no puede estar vacío.")
        elif not aeronave.get_disponible():
            logger.warning(f"La aeronave {aeronave.get_matricula()} no está disponible para asignar un puesto.")
        else:
            self.__registrar_actividad(f"Aeronave {aeronave.get_matricula()} asignada al puesto {puesto}.")
            logger.info(f"Aeronave {aeronave.get_matricula()} asignada al puesto {puesto}.")

    def ofrecer_servicio_vip(self, pasajero):
        """
        Asigna servicios VIP a un pasajero específico.
        
        Args:
            pasajero (Pasajero): Objeto que representa al pasajero.
        """
        if pasajero:
            self.__registrar_actividad(f"Servicio VIP asignado al pasajero {pasajero.get_nombre()}.")
            logger.info(f"Servicio VIP asignado al pasajero {pasajero.get_nombre()}.")
        else:
            logger.warning("No se pudo asignar el servicio VIP porque el pasajero no es válido.")

    def gestionar_catering(self, vuelo, menu_personalizado):
        """
        Proporciona un catering personalizado para un vuelo.
        
        Args:
            vuelo (Vuelo): Objeto que representa el vuelo.
            menu_personalizado (str): Descripción del menú personalizado.
        """
        if vuelo and menu_personalizado:
            self.__registrar_actividad(f"Catering personalizado asignado al vuelo {vuelo.get_numero_vuelo()}: {menu_personalizado}.")
            logger.info(f"Catering personalizado para el vuelo {vuelo.get_numero_vuelo()}: {menu_personalizado}.")
        else:
            logger.warning("Datos inválidos para gestionar catering.")

    def listar_servicios_disponibles(self):
        """
        Devuelve una lista de servicios disponibles en el FBO.
        
        Returns:
            list: Lista de servicios disponibles.
        """
        servicios_disponibles = [
            "Suministro de combustible",
            "Carga y descarga de equipaje",
            "Asignar hangar",
            "Servicios VIP",
            "Catering",
            "Generar reporte"
        ]
        logger.info("Lista de servicios disponibles generada correctamente.")
        return servicios_disponibles

    def generar_reporte_servicios(self):
        """
        Genera un reporte detallado de los servicios realizados.
        
        Returns:
            str: Reporte en formato de texto.
        """
        reporte = "Reporte de Servicios:\n"
        for actividad in self.__historial_actividades:
            reporte += f"- {actividad}\n"
        logger.info("Reporte de servicios generado exitosamente.")
        return reporte


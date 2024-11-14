from datetime import datetime
from typing import List
from loguru import logger 

class Avion:
    def __init__(self, df_info_avion, config, matricula=None):
        """
        Inicializa una instancia de Avion para operar sobre un DataFrame existente.
        Puede utilizar la matrícula para buscar un avión específico o trabajar con el DataFrame completo.

        :param df_info_avion: DataFrame que contiene la información de los aviones.
        :param config: Configuración con las columnas y otras opciones necesarias.
        :param matricula: Matrícula del avión específico (opcional).
        """
        self.df_info_avi = df_info_avion
        self.config = config
        self.cols_direct = self.config["directorio_aviones"]["dict_cols"]
        
        if matricula:
            self.matricula = matricula
            self.avion_data = self.df_info_avi[self.df_info_avi[self.cols_direct['matricula']] == matricula]
        else:
            self.matricula = None
            self.avion_data = None

    def mostrar_menu(self):
        """Muestra el menú de opciones al usuario y ejecuta la opción seleccionada."""
        while True:
            print("\nMenú de Opciones:")
            print("1. Obtener información del avión")
            print("2. Actualizar horas de vuelo")
            print("3. Realizar mantenimiento")
            print("4. Ver aviones que necesitan mantenimiento")
            print("5. Ver aviones disponibles")
            print("0. Salir")
            
            opcion = input("Seleccione una opción: ")
            self.ejecutar_proceso(opcion)
    
    def ejecutar_proceso(self, opcion): 
        """Ejecuta la opción seleccionada por el usuario."""
        if opcion == "1":
            print(self.obtener_informacion_avion())
        elif opcion == "2":
            horas = float(input("Ingrese el número de horas de vuelo a actualizar: "))
            self.actualizar_horas_vuelo(horas)
        elif opcion == "3":
            self.realizar_mantenimiento()
            print("Mantenimiento realizado.")
        elif opcion == "4":
            print(Avion.aviones_necesitan_mantenimiento(self.df_info_avi))
        elif opcion == "5":
            print(Avion.aviones_disponibles(self.df_info_avi))
        elif opcion == "0":
            print("Saliendo del programa...")
            return
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
            self.df_info_avi.loc[self.df_info_avi[self.cols_direct['matricula']] == self.matricula, 'horas_vuelo'] += horas
            print(f"Horas de vuelo actualizadas para el avión con matrícula {self.matricula}.")
        else:
            print("No se ha especificado una matrícula o el avión no existe en el DataFrame.")

    def realizar_mantenimiento(self):
        """
        Marca el avión como mantenido, actualizando las horas desde el último mantenimiento a 0.
        """
        if self.avion_data is not None:
            self.df_info_avi.loc[self.df_info_avi[self.cols_direct['matricula']] == self.matricula, 'horas_ultimo_mantenimiento'] = 0
            self.df_info_avi.loc[self.df_info_avi[self.cols_direct['matricula']] == self.matricula, 'necesita_mantenimiento'] = False
        else:
            print("No se ha especificado una matrícula o el avión no existe en el DataFrame.")

    @staticmethod
    def aviones_necesitan_mantenimiento(df):
        """
        Devuelve un DataFrame con los aviones que necesitan mantenimiento.

        :param df: DataFrame que contiene la información de los aviones.
        :return: DataFrame filtrado con los aviones que necesitan mantenimiento.
        """
        return df[df['necesita_mantenimiento'] == True]

    @staticmethod
    def aviones_disponibles(df):
        """
        Devuelve un DataFrame con los aviones disponibles.

        :param df: DataFrame que contiene la información de los aviones.
        :return: DataFrame filtrado con los aviones disponibles.
        """
        return df[df['disponible'] == True]

    def verificar_mantenimiento(self):
        return self.avion_data['necesita_mantenimiento'].iloc[0] or (
            self.avion_data['horas_vuelo'].iloc[0] - self.avion_data['horas_ultimo_mantenimiento'].iloc[0] >= 400
        )


"""class Mantenimiento:
#
#    def __init__(
#        self,
#        avion,
#        lider_tecnico,
#        combustible_disponible,
#        espacio_hangar_disponible,
#        prioridad,
#    ):
#        self.__avion = avion
#        self.__mantenimiento_historial = []
#        self.__lider_tecnico = lider_tecnico
#        self.__personal_mantenimiento = []
#        self.__combustible_disponible = combustible_disponible
#        self.__espacio_hangar_disponible = espacio_hangar_disponible
#        self.__prioridad = prioridad
#        self.__horas_ultimo_mantenimiento = 0
#        self.__necesita_mantenimiento = False
#        self.__mantenimiento_historial = []
#        self.__historial_servicios = []
#
#    def registrar_mantenimiento(
#        self, descripcion: str, fecha: datetime, componentes_cambiados: List[str]
#    ):
#        mantenimiento_dict = {
#            "Descripcion": descripcion,
#            "Fecha": fecha,
#            "Repuestos": componentes_cambiados,
#        }
#        self.__mantenimiento_historial.append(mantenimiento_dict)
#
#    def obtener_historial_mantenimiento(self):
#        return self.__mantenimiento_historial
#
#    def verificar_necesidad_mantenimiento(
#        self, horas_vuelo: int, max_horas_mantenimiento: int
#    ) -> bool:
#        self.__necesita_mantenimiento = (
#            horas_vuelo - self.__horas_ultimo_mantenimiento
#        ) >= max_horas_mantenimiento
#        return self.__necesita_mantenimiento
#
#    def registrar_combutible(self, cantidad):
#        if cantidad > 0:
#            self.__combustible_disponible += cantidad
#        else:
#            print("La cantidad de combustible a registrar debe ser positiva.")
#
#    def solicitar_combutible(self, cantidad):
#        if cantidad > 0:
#            if self.__combustible_disponible >= cantidad:
#                self.__combustible_disponible -= cantidad
#            else:
#                print("No hay suficiente combustible disponible.")
#        else:
#            print("La cantidad de combustible solicitada debe ser positiva.")
#
#    def asignar_hangar(self):
#        if self.__espacio_hangar_disponible:
#            self.__espacio_hangar_disponible -= 1
#            return True
#        return False
#
#    def liberar_hangar(self):
#        self.__espacio_hangar_disponible += 1
#
#    def remolcar_aeronave(self):
#        servicio = {"Servicio": "Remolque", "Fecha": datetime.now()}
#        self.__historial_servicios.append(servicio)
#        print("El servicio de remolque ha sido realizado con éxito.")
#
#    def limpiar_aeronave(self):
#        servicio = {"Servicio": "Limpieza", "Fecha": datetime.now()}
#        self.__historial_servicios.append(servicio)
#        print("El servicio de limpieza ha sido realizado con éxito.")
#
#    def mostrar_historial_servicios(self):
#        for servicio in self.__historial_servicios:
#            print(f"Servicio: {servicio['Servicio']}, Fecha: {servicio['Fecha']}")
"""
from datetime import datetime
from typing import List
from loguru import logger
import pandas as pd
from  transformation_functions import PandasBaseTransformer as PBT
import general_functions as gf

RUTA_EXCEL_PASAJEROS = "Insumos/pasajeros.xlsx"

class Pasajeros:
    def __init__(self, menu, config):
        self.__config = config
        self.__menu_pasajero = menu
        self._cols_df_pasajeros = self.__config["directorio_pasajeros"]["dict_cols"]
        self.__df_pasajeros = self._leer_info_pasajeros()
        
    def mostrar_menu(self):
        """Muestra el menú personalizado."""
        eleccion = self.__config["Menu"]["menu_opcion"]["8"]
        gf.mostrar_menu_personalizado(eleccion, self.__menu_pasajero)

    def ejecutar_proceso(self):
        """
        Ejecuta el proceso basado en la opción ingresada por el usuario.

        Returns:
            bool: Resultado del proceso ejecutado.
        """
        opcion_ingresada = input("Ingresa la opción a ejecutar: ")
        return self.ejecutar_proceso_pasajero(opcion_ingresada)

    def ejecutar_proceso_pasajero(self, opcion: str) -> bool:
        """
        Ejecuta la opción seleccionada por el usuario.

        Args:
            opcion (str): Opción seleccionada.

        Returns:
            bool: True si debe continuar, False si debe detenerse.
        """
        opciones = {
            "1": self.informacion_pasajero,
            "2": self.agregar_pasajero,
            "3": self.actualizar_datos_pasajero,
            "0": lambda: False,  # Salir del menú
        }

        return gf.procesar_opcion(opcion=opcion, opciones=opciones)

    def _leer_info_pasajeros(self) -> pd.DataFrame:
        logger.info("Leyendo información de pasajeros desde el archivo configurado...")
        try:
            df_info_pasajeros = pd.read_excel(RUTA_EXCEL_PASAJEROS)
            logger.info("Información de pasajeros cargada correctamente.")
            return df_info_pasajeros
        except FileNotFoundError:
            logger.error("El archivo de pasajeros no existe. Verifique la ruta.")
            raise FileNotFoundError(f"No se encontró el archivo en la ruta {RUTA_EXCEL_PASAJEROS}.")

    def get_pasajeros(self):
        return self.__df_pasajeros

    def guardar_cambios(self):
        try:
            self.__df_pasajeros.to_excel(RUTA_EXCEL_PASAJEROS, index=False)
            print("Los cambios se han guardado correctamente.")
        except Exception as e:
            print(f"Error al guardar los datos en el archivo Excel: {e}")

    def agregar_pasajero(self):
        
        print("Ingrese los datos del nuevo pasajero: ")

        nombre = input("Nombre: ").strip()
        while not nombre.isalpha() or len(nombre) < 2:
            print("El nombre ingresado no es válido. Debe contener solo letras y al menos 2 caracteres.")
            nombre = input("Nombre: ").strip()

        documento_identidad = input("Documento de identidad: ").strip()
        while not documento_identidad.isdigit() or len(documento_identidad) < 8:
            print("El documento de identidad ingresado no es válido. Debe contener solo números y al menos 8 dígitos.")
            documento_identidad = input("Documento de identidad: ").strip()

        edad = input("Edad: ").strip()
        while (edad < 0) or not edad.isdigit():
            print("La edad ingresada no es válida. Debe ser un número entre 18 y 100.")
            edad = input("Edad: ").strip()
        edad = int(edad)

        equipaje = input("Peso del equipaje (kg): ").strip()
        while True:
            try:
                equipaje = float(equipaje)
                if equipaje <= 0 or equipaje > 50:
                    print("El peso del equipaje no es válido. Debe ser un número mayor o igual a 0 y menor o igual a 50.")
                    equipaje = input("Peso del equipaje (kg): ").strip()
                    continue
                break
            except ValueError:
                print("El peso ingresado no es válido o hay sobrepeso. Debe ser un número valido|.")
                equipaje = input("Peso del equipaje (kg): ").strip()

        vuelo = input("Vuelo: ").strip()
        while len(vuelo) < 3:
            print("El código del vuelo ingresado no es válido. Debe tener al menos 3 caracteres.")
            vuelo = input("Vuelo: ").strip()

        estado_reserva = input("Estado de reserva (Confirmada/Pendiente/Cancelada): ").strip().capitalize()
        while estado_reserva not in ["Confirmada", "Pendiente", "Cancelada"]:
            print("El estado de reserva ingresado no es válido. Debe ser 'Confirmada', 'Pendiente' o 'Cancelada'.")
            estado_reserva = input("Estado de reserva (Confirmada/Pendiente/Cancelada): ").strip().capitalize()

        nuevo_pasajero = {
            self._cols_df_pasajeros["nombre"]: nombre,
            self._cols_df_pasajeros["documento_identidad"]: documento_identidad,
            self._cols_df_pasajeros["edad"]: edad,
            self._cols_df_pasajeros["equipaje"]: equipaje,
            self._cols_df_pasajeros["vuelo"]: vuelo,
            self._cols_df_pasajeros["estado_reserva"]: estado_reserva,
        }

        self.__df_pasajeros = pd.concat([self.__df_pasajeros, pd.DataFrame([nuevo_pasajero])], ignore_index=True)
        print(f"El pasajero {nombre} con documento {documento_identidad} se ha agregado correctamente.")

        # Guardar cambios
        self.guardar_cambios()

    def informacion_pasajero(self, documento_identidad):
        pasajero = self.__df_pasajeros[self.__df_pasajeros[self._cols_df_pasajeros["documento_identidad"]] == documento_identidad]
        if pasajero.empty:
            print(f"No se encontró ningún pasajero con documento de identidad {documento_identidad}.")
            return

        print("Información del pasajero:")
        print(pasajero)

    def actualizar_datos_pasajero(self, documento_identidad, nombre=None, edad=None, peso=None):
        pasajero = self.__df_pasajeros[self.__df_pasajeros[self._cols_df_pasajeros["documento_identidad"]] == documento_identidad].index

        if pasajero.empty:
            print(f"No se encontró ningún pasajero con documento de identidad {documento_identidad}.")
            return

        if nombre:
            self.__df_pasajeros.at[pasajero[0], self._cols_df_pasajeros["nombre"]] = nombre
        if edad:
            self.__df_pasajeros.at[pasajero[0], self._cols_df_pasajeros["edad"]] = edad
        if peso:
            self.__df_pasajeros.at[pasajero[0], self._cols_df_pasajeros["equipaje"]] = peso

        print(f"Datos del pasajero con documento {documento_identidad} actualizados correctamente.")
        self.guardar_cambios()

    def actualizar_reserva_pasajero(self, documento_identidad, vuelo=None, estado_reserva=None):
        pasajero = self.__df_pasajeros[self.__df_pasajeros[self._cols_df_pasajeros["documento_identidad"]] == documento_identidad].index

        if pasajero.empty:
            print(f"No se encontró ningún pasajero con documento de identidad {documento_identidad}.")
            return

        if vuelo:
            self.__df_pasajeros.at[pasajero[0], self._cols_df_pasajeros["vuelo"]] = vuelo
        if estado_reserva:
            self.__df_pasajeros.at[pasajero[0], self._cols_df_pasajeros["estado_reserva"]] = estado_reserva

        print(f"Reserva del pasajero con documento {documento_identidad} actualizada correctamente.")
        self.guardar_cambios()


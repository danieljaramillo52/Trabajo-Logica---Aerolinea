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

        opcion_ingresada = input("Ingresa la opción a ejecutar: ")
        return self.ejecutar_proceso_pasajero(opcion_ingresada)

    def ejecutar_proceso_pasajero(self, opcion: str) -> bool:

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
        while int(edad) < 0 or not edad.isdigit():
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

    def informacion_pasajero(self, documento_identidad=None):

        if not documento_identidad:
            documento_identidad = input("Ingrese el documento de identidad: ").strip()


        pasajero = self.__df_pasajeros[self.__df_pasajeros[self._cols_df_pasajeros["documento_identidad"]] == documento_identidad]
        if pasajero.empty:
            print(f"No se encontró ningún pasajero con documento de identidad {documento_identidad}.")
        else:
            print("Información del pasajero:")
            print(pasajero)
            
    def informacion_pasajero(self, documento_identidad=None):
        if not documento_identidad:
            documento_identidad = input("Ingrese el documento de identidad: ").strip()
        try:
            # Asegurarse de que la columna existe
            if self._cols_df_pasajeros["documento_identidad"] not in self.__df_pasajeros.columns:
                print("Error: La columna de documento de identidad no existe en el DataFrame.")
                return
            
            # Convertir ambos valores a cadenas y eliminar espacios adicionales
            filtro_columna = self.__df_pasajeros[self._cols_df_pasajeros["documento_identidad"]].astype(str).str.strip()
            documento_identidad = documento_identidad.strip()
            
            pasajero = self.__df_pasajeros[filtro_columna == documento_identidad]
            
            if pasajero.empty:
                print(f"No se encontró ningún pasajero con documento de identidad {documento_identidad}.")
            else:
                print("Información del pasajero:")
                print(pasajero)
        except Exception as e:
            print(f"Error al buscar información del pasajero: {e}")

    def actualizar_datos_pasajero(self, documento_identidad=None, nombre=None, edad=None, peso=None):
        if not documento_identidad:
            documento_identidad = input("Ingrese el documento de identidad: ").strip()

        filtro_columna = self.__df_pasajeros[self._cols_df_pasajeros["documento_identidad"]].astype(str).str.strip()
        documento_identidad = documento_identidad.strip()
        pasajero = self.__df_pasajeros[filtro_columna == documento_identidad]

        if pasajero.empty:
            print(f"No se encontró ningún pasajero con documento de identidad {documento_identidad}.")
            return

        index = pasajero.index[0]

        if nombre is None:
            nombre = input("Nuevo nombre (Enter para no cambiar): ").strip() or self.__df_pasajeros.at[index, self._cols_df_pasajeros["nombre"]]
        if edad is None:
            edad = input("Nueva edad (Enter para no cambiar): ").strip()
            edad = int(edad) if edad else self.__df_pasajeros.at[index, self._cols_df_pasajeros["edad"]]
        if peso is None:
            peso = input("Nuevo peso (Enter para no cambiar): ").strip()
            peso = float(peso) if peso else self.__df_pasajeros.at[index, self._cols_df_pasajeros["equipaje"]]

        self.__df_pasajeros.at[index, self._cols_df_pasajeros["nombre"]] = nombre
        self.__df_pasajeros.at[index, self._cols_df_pasajeros["edad"]] = edad
        self.__df_pasajeros.at[index, self._cols_df_pasajeros["equipaje"]] = peso

        print(f"Datos actualizados correctamente para el pasajero {documento_identidad}.")
        self.guardar_cambios()


    def actualizar_reserva_pasajero(self, documento_identidad=None, vuelo=None, estado_reserva=None):
        if not documento_identidad:
            documento_identidad = input("Ingrese el documento de identidad: ").strip()
        pasajero = self.__df_pasajeros[self.__df_pasajeros[self._cols_df_pasajeros["documento_identidad"]] == documento_identidad].index
        if pasajero.empty:
            print(f"No se encontró ningún pasajero con documento de identidad {documento_identidad}.")
            return
        if vuelo is None:
            vuelo = input("Nuevo vuelo (Enter para no cambiar): ").strip() or self.__df_pasajeros.at[pasajero[0], self._cols_df_pasajeros["vuelo"]]
        if estado_reserva is None:
            estado_reserva = input("Nuevo estado de reserva (Enter para no cambiar): ").strip().capitalize()
            if not estado_reserva:
                estado_reserva = self.__df_pasajeros.at[pasajero[0], self._cols_df_pasajeros["estado_reserva"]]
        self.__df_pasajeros.at[pasajero[0], self._cols_df_pasajeros["vuelo"]] = vuelo
        self.__df_pasajeros.at[pasajero[0], self._cols_df_pasajeros["estado_reserva"]] = estado_reserva
        print(f"Reserva actualizada correctamente para el pasajero {documento_identidad}.")
        self.guardar_cambios()


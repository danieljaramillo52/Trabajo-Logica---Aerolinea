import pandas as pd
from loguru import logger

RUTA_EXCEL_PASAJEROS = "Insumos/pasajeros.xlsx"
"""
directorio_pasajeros: 
  nom_base: "pasajeros_sin_asiento.xlsx"
  nom_hoja: "Directorio_Pasajeros"
  dict_cols: 
    "nombre": "Nombre"
    "documento_identidad": "Documento_Identidad"
    "edad": "Edad"
    "equipaje": "Equipaje"
    "vuelo": "Vuelo"
    "estado_reserva": "Estado_Reserva"
"""

class Pasajeros:
    def __init__(self, config):
        self.__config = config
        self._cols_df_pasajeros = self.__config["directorio_pasajeros"]["dict_cols"]
        self.__df_pasajeros = self._leer_info_pasajeros()

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

    class Pasajero:
        def __init__(self, nombre, documento_identidad, edad, equipaje, vuelo, estado_reserva):
            self.__nombre = nombre
            self.__documento_identidad = documento_identidad
            self.__edad = edad
            self.__equipaje = equipaje
            self.__vuelo = vuelo
            self.__estado_reserva = estado_reserva

        def calcular_peso_total_equipaje(self):
            """
            Devuelve el peso del equipaje del pasajero.
            """
            return self.__equipaje

        def actualizar_datos(self, nombre=None, documento_identidad=None, edad=None):
            """
            Actualiza los datos del pasajero.
            """
            if nombre:
                self.__nombre = nombre
            if documento_identidad:
                self.__documento_identidad = documento_identidad
            if edad:
                self.__edad = edad

        def actualizar_equipaje(self, equipaje):
            """
            Actualiza el peso del equipaje del pasajero.
            """
            self.__equipaje = equipaje

        def actualizar_reserva(self, vuelo=None, estado_reserva=None):
            """
            Actualiza la información de la reserva del pasajero.
            """
            if vuelo:
                self.__vuelo = vuelo
            if estado_reserva:
                self.__estado_reserva = estado_reserva

        def pasajero_to_dict(self):
            """
            Devuelve los datos del pasajero como un diccionario.
            """
            return {
                "nombre": self.__nombre,
                "documento_identidad": self.__documento_identidad,
                "edad": self.__edad,
                "equipaje": self.__equipaje,
                "vuelo": self.__vuelo,
                "estado_reserva": self.__estado_reserva,
            }


import pandas as pd

RUTA_EXCEL_TRIPULACION = "Insumos/tripulacion.xlsx"

class Tripulacion:
    def __init__(self, id_tripulacion, nombre, id_empleado, rol, documento_licencia, horas_vuelo):
        self.__id_tripulacion = id_tripulacion
        self.__nombre = nombre
        self.__id_empleado = id_empleado
        self.__rol = rol
        self.__documento_licencia = documento_licencia
        self.__horas_vuelo = horas_vuelo

    def tripulacion_to_dict(self):
        return {
            "id_tripulacion": self.__id_tripulacion,
            "nombre": self.__nombre,
            "id_empleado": self.__id_empleado,
            "rol": self.__rol,
            "documento_licencia": self.__documento_licencia,
            "horas_vuelo": self.__horas_vuelo
        }
    
    def tripulacion_from_dict(self, data):
        self.__id_tripulacion = data.get("id_tripulacion", "")
        self.__nombre = data.get("nombre", "")
        self.__id_empleado = data.get("id_empleado", "")
        self.__rol = data.get("rol", "")
        self.__documento_licencia = data.get("documento_licencia", "")
        self.__horas_vuelo = data.get("horas_vuelo", 0)


class AdminTripulacion:
    def __init__(self):
        self.ruta_excel = RUTA_EXCEL_TRIPULACION

    def validar_id_tripulacion(self):
        while True:
            id_tripulacion = input("Ingrese el ID de la tripulación: ").strip()
            if len(id_tripulacion) > 0:
                return id_tripulacion
            print("El ID de la tripulación no puede estar vacío.")

    def validar_nombre(self):
        while True:
            nombre = input("Ingrese el nombre: ").strip()
            if nombre.replace(" ", "").isalpha() and len(nombre) > 1:
                return nombre
            print("El nombre debe contener solo letras y al menos dos caracteres.")

    def validar_id_empleado(self):
        while True:
            id_empleado = input("Ingrese el ID del empleado: ").strip()
            if id_empleado.isalnum():
                return id_empleado
            print("El ID del empleado debe ser alfanumérico.")

    def validar_documento_licencia(self):
        while True:
            documento_licencia = input("Ingrese el documento/licencia: ").strip()
            if len(documento_licencia) > 0:
                return documento_licencia
            print("El documento/licencia no puede estar vacío.")

    def validar_horas_vuelo(self):
        while True:
            horas_vuelo = input("Ingrese las horas de vuelo: ").strip()
            if horas_vuelo.isdigit() and int(horas_vuelo) >= 0:
                return int(horas_vuelo)
            print("Las horas de vuelo deben ser un número entero positivo.")

    def agregar_tripulacion(self):
        id_tripulacion = self.validar_id_tripulacion()
        tripulacion = []
        
        print("\n--- Datos del piloto ---")
        piloto = self.crear_miembro_tripulacion(id_tripulacion, "Piloto")
        tripulacion.append(piloto)

        print("\n--- Datos del copiloto ---")
        copiloto = self.crear_miembro_tripulacion(id_tripulacion, "Copiloto")
        tripulacion.append(copiloto)

        while True:
            print("\n--- Datos de la azafata ---")
            azafata = self.crear_miembro_tripulacion(id_tripulacion, "Azafata")
            tripulacion.append(azafata)
            
            continuar = input("¿Desea agregar otra azafata? (S/N): ").strip().lower()
            if continuar != "s":
                break

        self.guardar_tripulacion([miembro.tripulacion_to_dict() for miembro in tripulacion])
        print("\nTripulación agregada correctamente y guardada en el archivo Excel.")

    def crear_miembro_tripulacion(self, id_tripulacion, rol):
        nombre = self.validar_nombre()
        id_empleado = self.validar_id_empleado()
        documento_licencia = self.validar_documento_licencia()
        horas_vuelo = self.validar_horas_vuelo()
        return Tripulacion(id_tripulacion, nombre, id_empleado, rol, documento_licencia, horas_vuelo)

    def guardar_tripulacion(self, tripulacion):
        try:
            try:
                df_existente = pd.read_excel(self.ruta_excel)
            except FileNotFoundError:
                df_existente = pd.DataFrame(columns=["id_tripulacion", "nombre", "id_empleado", "rol", "documento_licencia", "horas_vuelo"])
            
            df_nuevo = pd.DataFrame(tripulacion)
            df_combinado = pd.concat([df_existente, df_nuevo], ignore_index=True)
            
            df_combinado.to_excel(self.ruta_excel, index=False)
        except Exception as e:
            print(f"Error al guardar la tripulación en el archivo Excel: {e}")

    def listar_tripulacion(self):
        try:
            df = pd.read_excel(self.ruta_excel)
            if df.empty:
                print("No hay tripulaciones registradas.")
            else:
                print("\n--- Lista de tripulaciones ---")
                print(df)
        except FileNotFoundError:
            print(f"No se encontró el archivo en {self.ruta_excel}.")
        except Exception as e:
            print(f"Error al leer el archivo Excel: {e}")

    def actualizar_miembro_tripulacion(self):
        try:
            df = pd.read_excel(self.ruta_excel)

            id_empleado = input("Ingrese el ID del empleado que desea modificar: ").strip()

            if id_empleado not in df["id_empleado"].values:
                print(f"No se encontró ningún miembro con el ID de empleado {id_empleado}.")
                return

            print("\n--- Datos actuales del miembro ---")
            print(df[df["id_empleado"] == id_empleado])

            nombre = self.validar_nombre()
            rol = "Azafata" if id_empleado.startswith("A") else "Piloto"
            documento_licencia = self.validar_documento_licencia()
            horas_vuelo = self.validar_horas_vuelo()

            df.loc[df["id_empleado"] == id_empleado, ["nombre", "rol", "documento_licencia", "horas_vuelo"]] = [nombre, rol, documento_licencia, horas_vuelo]

            df.to_excel(self.ruta_excel, index=False)
            print("\nDatos actualizados correctamente y guardados en el archivo Excel.")
        except FileNotFoundError:
            print(f"No se encontró el archivo en {self.ruta_excel}.")
        except Exception as ex:
            print(f"Error al actualizar el archivo Excel: {ex}")


if __name__ == "__main__":
    manager = AdminTripulacion()
    while True:
        print("\n--- Menú de Gestión de Tripulación ---")
        print("1. Agregar tripulación")
        print("2. Listar tripulación")
        print("3. Actualizar miembro de la tripulación")
        print("4. Salir")

        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            manager.agregar_tripulacion()
        elif opcion == "2":
            manager.listar_tripulacion()
        elif opcion == "3":
            manager.actualizar_miembro_tripulacion()
        elif opcion == "4":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

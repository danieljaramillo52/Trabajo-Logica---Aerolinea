import pandas as pd
from ModuloEmpleado import Empleados

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
    def __init__(self, empleados_manager):
        self.ruta_excel = RUTA_EXCEL_TRIPULACION
        self.empleados_manager = empleados_manager

    def obtener_empleado_por_id(self, id_empleado):
        df_empleados = self.empleados_manager.get_empleados()
        empleado_filtrado = df_empleados[df_empleados[self.empleados_manager._cols_df_empleados["id_empleado"]] == id_empleado]
        if empleado_filtrado.empty:
            return None
        return empleado_filtrado.iloc[0].to_dict()

    def crear_miembro_tripulacion(self, id_tripulacion, rol):
        while True:
            id_empleado = input(f"Ingrese el ID del empleado para el rol {rol}: ").strip()
            datos_empleado = self.obtener_empleado_por_id(id_empleado)
            if not datos_empleado:
                print(f"No se encontró ningún empleado con el ID {id_empleado}. Intente nuevamente.")
                continue
            if datos_empleado["rol"] != rol:
                print(f"El empleado con ID {id_empleado} tiene el rol {datos_empleado['rol']} en lugar de {rol}. Intente con otro ID.")
                continue
            return Tripulacion(
                id_tripulacion=id_tripulacion,
                nombre=datos_empleado["nombre"],
                id_empleado=datos_empleado["id_empleado"],
                rol=datos_empleado["rol"],
                documento_licencia=datos_empleado["documento_licencia"],
                horas_vuelo=datos_empleado["horas_vuelo"]
            )

    def agregar_tripulacion(self):
        id_tripulacion = input("Ingrese el ID de la tripulación: ").strip()
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

    def guardar_tripulacion(self, tripulacion):
        try:
            try:
                df_existente = pd.read_excel(self.ruta_excel)
            except FileNotFoundError:
                df_existente = pd.DataFrame(columns=["id_tripulacion", "nombre", "id_empleado", "rol", "documento_licencia", "horas_vuelo"])
            df_nuevo = pd.DataFrame(tripulacion)
            df_combinado = pd.concat([df_existente, df_nuevo], ignore_index=True)
            df_combinado.to_excel(self.ruta_excel, index=False)
        except Exception as ex:
            print(f"Error al guardar la tripulación en el archivo Excel: {ex}")

    def listar_tripulacion(self):
        try:
            df = pd.read_excel(self.ruta_excel)
            if df.empty:
                print("No hay tripulaciones registradas.")
            else:
                print("\n--- Lista de tripulaciones ---")
                print(df)
        except Exception as ex:
            print(f"Error al leer el archivo Excel: {ex}")

    def actualizar_miembro_tripulacion(self):
        try:
            df = pd.read_excel(self.ruta_excel)
            id_empleado = input("Ingrese el ID del empleado que desea modificar: ").strip()
            if id_empleado not in df["id_empleado"].values:
                print(f"No se encontró ningún miembro con el ID de empleado {id_empleado}.")
                return
            print("\n--- Datos actuales del miembro ---")
            print(df[df["id_empleado"] == id_empleado])
            nombre = input("Ingrese el nuevo nombre: ").strip()
            documento_licencia = input("Ingrese el nuevo documento/licencia: ").strip()
            horas_vuelo = int(input("Ingrese las nuevas horas de vuelo: ").strip())
            df.loc[df["id_empleado"] == id_empleado, ["nombre", "documento_licencia", "horas_vuelo"]] = [nombre, documento_licencia, horas_vuelo]
            df.to_excel(self.ruta_excel, index=False)
            print("\nDatos actualizados correctamente y guardados en el archivo Excel.")
        except FileNotFoundError:
            print(f"No se encontró el archivo en {self.ruta_excel}.")
        except Exception as ex:
            print(f"Error al actualizar el archivo Excel: {ex}")


if __name__ == "__main__":
    empleados_admin = Empleados(config={"directorio_empleados": {"dict_cols": {"id_empleado": "id_empleado"}}})
    admin = AdminTripulacion(empleados_admin)
    while True:
        print("\n--- Menú de Gestión de Tripulación ---")
        print("1. Agregar tripulación")
        print("2. Listar tripulación")
        print("3. Actualizar miembro de la tripulación")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            admin.agregar_tripulacion()
        elif opcion == "2":
            admin.listar_tripulacion()
        elif opcion == "3":
            admin.actualizar_miembro_tripulacion()
        else:
            print("Opción no válida. Intente nuevamente.")

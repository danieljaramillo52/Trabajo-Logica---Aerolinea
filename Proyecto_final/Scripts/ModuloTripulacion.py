import pandas as pd
from ModuloEmpleado import Empleados
import general_functions as gf
from transformation_functions import PandasBaseTransformer as PBT 

RUTA_EXCEL_TRIPULACION = "Insumos/tripulacion.xlsx"


class Tripulacion:
    def __init__(
        self, id_tripulacion, nombre, id_empleado, Rol, documento_licencia, horas_vuelo
    ):
        self.__id_tripulacion = id_tripulacion
        self.__nombre = nombre
        self.__id_empleado = id_empleado
        self.__Rol = Rol
        self.__documento_licencia = documento_licencia
        self.__horas_vuelo = horas_vuelo

    def tripulacion_to_dict(self):
        return {
            "id_tripulacion": self.__id_tripulacion,
            "Nombre": self.__nombre,
            "ID_Empleado": self.__id_empleado,
            "Rol": self.__Rol,
            "Documento_Licencia": self.__documento_licencia,
            "Horas_Vuelo": self.__horas_vuelo,
        }

    def tripulacion_from_dict(self, data):
        self.__id_tripulacion = data.get("id_tripulacion", "")
        self.__nombre = data.get("Nombre", "")
        self.__id_empleado = data.get("ID_Empleado", "")
        self.__Rol = data.get("Rol", "")
        self.__documento_licencia = data.get("Documento_Licencia", "")
        self.__horas_vuelo = data.get("Horas_Vuelo", 0)


class AdminTripulacion:
    def __init__(self, config, menu_tripulacion: dict, empleados_manager: "Empleados"):
        self.ruta_excel = RUTA_EXCEL_TRIPULACION
        self.empleados_manager = empleados_manager
        self.__config = config 
        self.__menu_tripulacion = menu_tripulacion

    def mostrar_menu(self):
        """Muestra el menú personalizado."""
        eleccion = self.__config["Menu"]["menu_opcion"]["4"]
        gf.mostrar_menu_personalizado(eleccion, self.__menu_tripulacion)

    def ejecutar_proceso(self):
        """
        Ejecuta el proceso basado en la opción ingresada por el usuario.

        Returns:
            bool: Resultado del proceso ejecutado.
        """
        opcion_ingresada = input("Ingresa la opción a ejecutar: ")
        return self.ejecutar_proceso_tripulacion(opcion_ingresada)

    def ejecutar_proceso_tripulacion(self, opcion: str) -> bool:
        """
        Ejecuta la opción seleccionada por el usuario.

        Args:
            opcion (str): Opción seleccionada.

        Returns:
            bool: True si debe continuar, False si debe detenerse.
        """
        opciones = {
            "1": self.agregar_tripulacion,
            "2": self.listar_tripulacion,
            "3": self.actualizar_miembro_tripulacion,
            "4": self,
            "5": self,
            "6": self,
            "0": lambda: False,  # Salir del menú
        }

        return gf.procesar_opcion(opcion=opcion, opciones=opciones)

    def obtener_empleado_por_id(self, id_empleado):
        df_empleados = self.empleados_manager.get_empleados()
        empleado_filtrado = df_empleados[
            df_empleados[self.empleados_manager._cols_df_empleados["ID_Empleado"]]
            == id_empleado
        ]
        if empleado_filtrado.empty:
            return None
        return empleado_filtrado.iloc[0].to_dict()

    def crear_miembro_tripulacion(self, id_tripulacion, Rol):
        while True:
            id_empleado = input(
                f"Ingrese el ID del empleado para el Rol {Rol}: "
            ).strip()
            datos_empleado = self.obtener_empleado_por_id(id_empleado)
            if not datos_empleado:
                print(
                    f"No se encontró ningún empleado con el ID {id_empleado}. Intente nuevamente."
                )
                continue
            if datos_empleado["Rol"] != Rol:
                print(
                    f"El empleado con ID {id_empleado} tiene el Rol {datos_empleado['Rol']} en lugar de {Rol}. Intente con otro ID."
                )
                continue
            return Tripulacion(
                id_tripulacion=id_tripulacion,
                nombre=datos_empleado["Nombre"],
                id_empleado=datos_empleado["ID_Empleado"],
                Rol=datos_empleado["Rol"],
                documento_licencia=datos_empleado["Documento_Licencia"],
                horas_vuelo=datos_empleado["Horas_Vuelo"],
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
        self.guardar_tripulacion(
            [miembro.tripulacion_to_dict() for miembro in tripulacion]
        )
        print("\nTripulación agregada correctamente y guardada en el archivo Excel.")

    def guardar_tripulacion(self, tripulacion):
        try:
            try:
                df_existente = pd.read_excel(self.ruta_excel)
            except FileNotFoundError:
                df_existente = pd.DataFrame(
                    columns=[
                        "id_tripulacion",
                        "Nombre",
                        "ID_Empleado",
                        "Rol",
                        "Documento_Licencia",
                        "Horas_Vuelo",
                    ]
                )
            df_nuevo = pd.DataFrame(tripulacion)
            df_combinado = pd.concat([df_existente, df_nuevo], axis=0, ignore_index=True)
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
            id_empleado = input(
                "Ingrese el ID del empleado que desea modificar: "
            ).strip()
            if id_empleado not in df["ID_Empleado"].values:
                print(
                    f"No se encontró ningún miembro con el ID de empleado {id_empleado}."
                )
                return
            print("\n--- Datos actuales del miembro ---")
            print(df[df["ID_Empleado"] == id_empleado])
            nombre = input("Ingrese el nuevo nombre: ").strip()
            documento_licencia = input("Ingrese el nuevo documento/licencia: ").strip()
            horas_vuelo = int(input("Ingrese las nuevas horas de vuelo: ").strip())
            df.loc[
                df["ID_Empleado"] == id_empleado,
                ["Nombre", "Documento_Licencia", "Horas_Vuelo"],
            ] = [nombre, documento_licencia, horas_vuelo]
            df.to_excel(self.ruta_excel, index=False)
            print("\nDatos actualizados correctamente y guardados en el archivo Excel.")
        except FileNotFoundError:
            print(f"No se encontró el archivo en {self.ruta_excel}.")
        except Exception as ex:
            print(f"Error al actualizar el archivo Excel: {ex}")

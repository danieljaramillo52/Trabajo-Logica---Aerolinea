from datetime import datetime
from typing import List
from loguru import logger
import pandas as pd
from  transformation_functions import PandasBaseTransformer as PBT
import general_functions as gf

RUTA_EXCEL = "Insumos/empleados.xlsx"

class Empleados:
    def __init__(self, config, __menu_empleados=None):
        self.__config = config
        self.__menu_empleados = __menu_empleados
        self._cols_df_empleados = self.__config["directorio_empleados"]["dict_cols"]
        self.__df_empleados = self._leer_info_empleados()

    def get_config(self):
        return self.__config
    
    def mostrar_menu(self):
        eleccion = self.__config["Menu"]["menu_opcion"][3]
        gf.mostrar_menu_personalizado(eleccion, self.__menu_empleados)

    def _leer_info_empleados(self) -> dict:
        logger.info("Leyendo información de empleados desde el archivo configurado...")
        lector_insumo = gf.ExcelReader(path=self.get_config()["path_insumos"])
        df_info_empleados = lector_insumo.Lectura_simple_excel(
            nom_insumo=self.__config["directorio_empleados"]["nom_base"],
            nom_hoja=self.__config["directorio_empleados"]["nom_hoja"],
        )
        logger.info("Información de empleados cargada correctamente.")
        print("")
        return df_info_empleados

    def get_empleados(self):
        """
        Proporciona el DataFrame con los datos de los empleados.
        :return: DataFrame de empleados.
        """
        return self.__df_empleados
    
    def get_config(self):
        return self.__config

    def ejecutar_proceso_empleados(self):
        opcion_ingresada = input("Ingresa la opción a ejecutar:\n ")
        resultado = self.ejecutar_proceso(opcion_ingresada)
        return resultado

    def administrar_empleados(self):
        df_select = PBT.Seleccionar_columnas_pd(
            df=self._df_empleados, cols_elegidas=[*self._cols_df_empleados]
        )        

    def empleado_to_dict(self, nuevo_empleado:'Empleado'):
        cols = self.get_config()["directorio_empleados"]["dict_cols"]
        return {
            cols["Nombre"]: self.__nombre,
            cols["ID_Empleado"]: self.__id_empleado,
            cols["Rol"]: self.__rol,
            cols["Documento_Licencia"]: self.__documento_licencia,
            cols["Horas_Vuelo"]: self.__horas_vuelo,
            cols["Estado_Empleado"]: self.__estado_empleado,
            cols["Correo_Electronico"]: self.__correo_electronico,
            cols["Disponible"]: self.__disponible_para_vuelo,
            cols["Ubicacion"]: self.__ubicacion,
        }

    def agregar_empleado(self):
        nombre = input("Ingrese el nombre del nuevo empleado: ")
        id_empleado = input("Ingrese el id del empleado: ")
        rol = input("Ingrese el rol a desempeñar: ")
        documento_licencia = input("Ingrese el documento o licencia: ")
        horas_vuelo = input("Ingrese las horas de vuelo certificadas: ")
        estado_empleado = "Activo"
        correo_electronico = input("Ingrese el correo electronico: ")
        disponible_para_vuelo = input("ingrese su disponibilidad para vuelo (FALSO/VERDADERO): ")
        ubicacion = input("Ingrese la ubicacion del empleado: ")

        nuevo_empleado = Empleado(
            nombre,
            id_empleado,
            rol,
            documento_licencia,
            horas_vuelo,
            estado_empleado,
            correo_electronico,
            disponible_para_vuelo,
            ubicacion,
        )
        
        dict_nuevo_empleado = self.empleado_to_dict(nuevo_empleado)
        df_nuevo_empleado = pd.DataFrame([dict_nuevo_empleado])
        df_actualizado = PBT.concatenate_dataframes(
            [self.get_empleados(), df_nuevo_empleado]
        )
       
        return df_actualizado.to_excel(RUTA_EXCEL, index=False)        
        
    
    def informacion_empleado(self):
        while True:
            try:
                eleccion = int(input("""Desea consultar el empleado por:
                            1 : Código del empleado
                            2 : Nombre del empleado
                            3 : Rol del empleado
                            4 : Documento/Licencia
                            \nSeleccione una opción (1-4): """))
                if eleccion <1 or eleccion >4:
                    raise ValueError("Opción no válida, intente nuevamente.")
                break
            except ValueError as ex:
                print(ex)

        valor = input("Ingrese el valor de búsqueda: ")
        columnas = {
            1: "id_empleado",
            2: "Nombre",
            3: "rol",
            4: "documento_licencia"
        }
        columna_clave = columnas.get(eleccion)

        # Filtrar en el diccionario
        empleados_filtrados = []
        for emp_filt in range(len(self.__df_empleados[columna_clave])):
            if str(self.__df_empleados[columna_clave][emp_filt]) == valor:
                empleado = {col: self.__df_empleados[col][emp_filt] for col in self.__df_empleados}
                empleados_filtrados.append(empleado)

        if empleados_filtrados:
            print("Información del empleado:")
            for emp in empleados_filtrados:
                print(emp)
        else:
            print("No se encontró ningun empleado")

    def actualizar_informacion_empleado(self, id_empleado):
        empleado_x_id = self.__df_empleados[self.__df_empleados[self._cols_df_empleados["id_empleado"]] == id_empleado].index

        if empleado_x_id.empty:
            print(f"No se encontró un empleado con ID {empleado_x_id}.")
            return

        # Mostrar información actual del empleado
        empleado_actual = self.__df_empleados.loc[empleado_x_id[0]]
        print("Información actual del empleado:")
        print(empleado_actual)

        # Mostrar las columnas disponibles para modificar
        columnas_disponibles = [col for col in self.__df_empleados.columns if col != self._cols_df_empleados["id_empleado"]]
        print("Columnas disponibles para modificar:")
        for ide, columna in enumerate(columnas_disponibles, start=1):
            print(f"{ide}. {columna}")

        # Seleccionar columna
        while True:
            try:
                opcion = int(input("Seleccione el número de la columna que desea modificar: "))
                if opcion < 1 or opcion > len(columnas_disponibles):
                    raise ValueError("Opción fuera de rango, intente nuevamente.")
                columna_seleccionada = columnas_disponibles[opcion - 1]
                break
            except ValueError as e:
                print(e)

        # Solicitar nuevo valor
        nuevo_valor = input(f"Ingrese el nuevo valor para '{columna_seleccionada}' (valor actual: {empleado_actual[columna_seleccionada]}): ").strip()
        if nuevo_valor:
            self.__df_empleados.at[empleado_x_id[0], columna_seleccionada] = nuevo_valor
            print(f"Se ha actualizado la columna '{columna_seleccionada}' del empleado con ID {id_empleado}.")
        else:
            print("No se realizaron cambios.")

        # Guardar cambios
        self.__df_empleados.to_excel(RUTA_EXCEL, index=False)
        print("Los cambios se han guardado correctamente.")

            
    def incrementar_horas_vuelo(self, id_empleado, horas):
        if horas <= 0:
            print("Por favor, ingrese un número válido de horas para incrementar.")
            return

        empleado_x_id = self.__df_empleados[self.__df_empleados[self._cols_df_empleados["id_empleado"]] == id_empleado].index

        if empleado_x_id.empty:
            print(f"No se encontró un empleado con ID {id_empleado}.")
            return

        self.__df_empleados.at[empleado_x_id[0], self._cols_df_empleados["horas_vuelo"]] += horas
        print(f"Se han incrementado {horas} horas de vuelo al empleado con ID {id_empleado}.")
        print(self.__df_empleados.loc[empleado_x_id])

        # Guardar cambios en el archivo Excel
        
        self.__df_empleados.to_excel(RUTA_EXCEL, index=False)


    def actualizar_estado_empleado(self, id_empleado, nuevo_estado):
        empleado_x_id = self.__df_empleados[self.__df_empleados[self._cols_df_empleados["id_empleado"]] == id_empleado].index

        if empleado_x_id.empty:
            print(f"No se encontró un empleado con ID {id_empleado}.")
            return

        self.__df_empleados.at[empleado_x_id[0], self._cols_df_empleados["estado_empleado"]] = nuevo_estado
        print(f"El estado del empleado con ID {id_empleado} se ha actualizado a '{nuevo_estado}'.")
        print(self.__df_empleados.loc[empleado_x_id])

        self.__df_empleados.to_excel(RUTA_EXCEL, index=False)

    def verificar_disponibilidad_para_vuelo(self, id_empleado):
        
        empleado = self.__df_empleados[self.__df_empleados[self._cols_df_empleados["id_empleado"]] == id_empleado].index

        if empleado.empty:
            print(f"No se encontró un empleado con ID {id_empleado}.")
            return

        # Obtener disponibilidad
        disponibilidad = self.__df_empleados.loc[empleado[0], self._cols_df_empleados["disponible"]]
        if disponibilidad.strip().upper() == "True":
            print(f"El empleado con ID {id_empleado} está disponible para vuelo.")
        else:
            print(f"El empleado con ID {id_empleado} NO está disponible para vuelo.")


class Empleado:
    def __init__(
        self,
        config,
        nombre,
        id_empleado,
        rol,
        documento_licencia,
        horas_vuelo,
        estado_empleado,
        correo_electronico,
        disponible,
        ubicacion,
    ):
        self.__nombre = nombre
        self.__id_empleado = id_empleado
        self.__rol = rol
        self.__documento_licencia = documento_licencia
        self.__horas_vuelo = horas_vuelo
        self.__estado_empleado = estado_empleado
        self.__certificaciones = []
        self.__correo_electronico = correo_electronico
        self.__disponible_para_vuelo = disponible
        self.__ubicacion = ubicacion
        



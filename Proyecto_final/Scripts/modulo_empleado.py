from datetime import datetime
from typing import List
from loguru import logger
import pandas as pd
from  transformation_functions import PandasBaseTransformer as PBT
import general_functions as gf

class Empleados:
    def __init__(self, config, __menu_empleados=None):
        self.__config = config
        self.__menu_empleados = __menu_empleados
        self._cols_df_empleados = self.__config["directorio_empleados"]["dict_cols"]
        self.__df_empleados = self._leer_info_empleados()

    def mostrar_menu(self):
        eleccion = self.__config["Menu"]["menu_opcion"][3]
        gf.mostrar_menu_personalizado(eleccion, self.__menu_empleados)

    def _leer_info_empleados(self) -> dict:
        logger.info("Leyendo información de empleados desde el archivo configurado...")
        lector_insumo = gf.ExcelReader(path=self.__config["path_insumos"])
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

    def agregar_empleado(self):
        nombre = input("Ingrese el nombre del nuevo empleado")
        id_empleado = input("Ingrese el id del empleado")
        rol = input("Ingrese el rol a desempeñar")
        documento_licencia = input("Ingrese el documento o licencia")
        horas_vuelo = input("Ingrese las horas de vuelo certificadas")
        estado_empleado = "Activo"
        correo_electronico = input("Ingrese el correo electronico")
        disponible_para_vuelo = input("ingrese su disponibilidad (FALSO/VERDADERO)")
        ubicacion = input("Ingrese la ubicacion del empleado")

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
        
        dict_nuevo_empleado = nuevo_empleado.empleado_to_dict()
        df_nuevo_empleado = pd.DataFrame([dict_nuevo_empleado])
        df_actualizado = PBT.concatenate_dataframes(
            [self.get_empleados(), df_nuevo_empleado]
        )
       
        df_actualizado.to_excel("Insumos/empleados.xlsx", index=False)
        
        return 


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
        

    def empleado_to_dict(self):
        cols = self.get_config()["directorio_empleados"]["dict_cols"]
        return {
            cols["Nombre"]: self.__nombre,
            cols["id_empleado"]: self.__id_empleado,
            cols["rol"]: self.__rol,
            cols["documento_licencia"]: self.__documento_licencia,
            cols["horas_vuelo"]: self.__horas_vuelo,
            cols["estado_empleado"]: self.__estado_empleado,
            cols["correo_electronico"]: self.__correo_electronico,
            cols["disponible"]: self.__disponible_para_vuelo,
            cols["ubicacion"]: self.__ubicacion,
        }
        
    def actualizar_empleado(self):
        pass
    
    def actiualizar_datos(self):
        pass

    def disponible_para_vuelo(self):
        return self.__disponible_para_vuelo["Disponible"]

    def incrementar_horas_vuelo(self, horas):
        self.__horas_vuelo += horas

    def actualizar_estado_empleado(self, estado):
        self.__estado_empleado = estado



from datetime import datetime
from typing import List
from loguru import logger
import pandas as pd
import general_functions as gf
from transformation_functions import PandasBaseTransformer as PBT

config = {
    "path_insumos": "Insumos/",
    
    "directorio_aviones": {
        "nom_base": "aviones_compania_final.xlsx",
        "nom_hoja": "Directorio_Aviones",
        "dict_cols": {
            "matricula": "matricula",
            "tipo": "tipo",
            "modelo": "modelo",
            "fabricante": "fabricante",
            "propietario": "propietario",
            "horas_vuelo": "horas_vuelo",
            "capacidad_pasajeros": "capacidad_pasajeros",
            "peso_maximo_equipaje": "peso_maximo_equipaje",
            "disponible": "disponible",
            "horas_ultimo_mantenimiento": "horas_ultimo_mantenimiento",
            "necesita_mantenimiento": "necesita_mantenimiento"
        }
    },

    "directorio_empleados": {
        "nom_base": "empleados.xlsx",
        "nom_hoja": "Directorio_Empleados",
        "dict_cols": {
            "Nombre": "Nombre",
            "id_empleado": "ID_Empleado",
            "rol": "Rol",
            "documento_licencia": "Documento_Licencia",
            "horas_vuelo": "Horas_Vuelo",
            "estado_empleado": "Estado_Empleado",
            "certificaciones": "Certificaciones",
            "correo_electronico": "Correo_Electronico",
            "disponible": "Disponible",
            "ubicacion": "Ubicacion",
        }
    },
    
    "Menu": {
        "mensaje_principal": """
        Menu principal:
        Ingrese el número de su selección:
        1.Ingresar a los procesos de gestión de Avión
        2.Ingresar a los procesos de gestión de Hangar
        3.Ingresar a los procesos de gestión de Empleado
        4.Ingresar a los procesos de gestión de Tripulación
        5.Ingresar a los procesos de gestión de Mantenimiento
        6.Ingresar a los procesos de gestión de Servicios
        7.Ingresar a los procesos de gestión de Vuelo
        8.Ingresar a los procesos de gestión de Pasajero
        0.Salir
        """,
        
        "menu_opcion": {
            1: "Avion",
            2: "Hangar",
            3: "Empleado",
            4: "Tripulacion",
            5: "Mantenimiento",
            6: "Servicios",
            7: "Vuelo",
            8: "Pasajero",
            0: "Salir"
        }
    },
    
    "opcion_regresar": {
        0: "Regresar al menu principal"
    },
    
    "directorio_menu": {
        "nom_base": "base_menus.xlsx",
        "nom_hojas": {
            1: "Avion",
            2: "Hangar",
            3: "Empleado",
            4: "Tripulacion",
            5: "Mantenimiento",
            6: "Servicios",
            7: "Vuelo",
            8: "Pasajero",
            0: "Salir"
        },
        "cols": {
            "num_opcion": "num_opcion",
            "opciones": "opciones"
        }
    },
    
    "dict_constantes": {
        "Salir": "Salir"
    }
}

class Empleados:

    def __init__(self, config, __menu_empleados=None, __PBT=None):
        self.__config = config
        self.__menu_empleados = __menu_empleados
        self.__PBT = __PBT
        self.__cols_df_empleados = self.__config["directorio_empleados"]["dict_cols"]
        self.__df_empleados = self._leer_info_empleado()
        

    def mostrar_menu(self):
        eleccion = self.__config["Menu"]["menu_opcion"][3]
        gf.mostrar_menu_personalizado(eleccion,self.__menu_empleados)    
    
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
     
    def ejecutar_proceso_empleados(self):            
        opcion_ingresada = input("Ingresa la opción a ejecutar:\n ")
        resultado = self.ejecutar_proceso(opcion_ingresada)
        return resultado
    
    def administrar_empleados(self):
        df_select = self.__PBT.Seleccionar_columnas_pd(
            df=self.__df_empleados, cols_elegidas=[*self.__cols_df_empleados]
        )

    def empleado_to_dict(self):
        return {
            "Nombre": self.nombre,
            "ID Empleado": self.id_empleado,
            "Rol": self.rol,
            "Documento Licencia": self.documento_licencia,
            "Horas Vuelo": self.horas_vuelo,
            "Estado": self.estado_empleado,
            "Certificaciones": self.certificaciones,
            "Correo Electronico": self.correo_electronico,
            "Disponible": self.disponible,
            "Ubicacion": self.ubicacion
        }

    def agregar_empleado(self):
        nombre = input("Ingrese el nombre del nuevo empleado")
        id_empleado = input("Ingrese el id del empleado")
        rol = input("Ingrese el rol a desempeñar")
        documento_licencia = input("Ingrese el documento o licencia")
        horas_vuelo = input("Ingrese las horas de vuelo certificadas")
        estado_empleado = "Activo"
        certificaciones = []
        correo_electronico = input("Ingrese el correo electronico")
        disponible_para_vuelo = {
            "Disponible": input("ingrese FALSO o VERDADERO"),
            "Ubicacion": input("Ingrese la ubicacion del empleado")
        }
        nuevo_empleado = Empleado(nombre, id_empleado, rol, documento_licencia, horas_vuelo, 
                                   estado_empleado, certificaciones, correo_electronico, 
                                  disponible_para_vuelo["Disponible", "Ubicacion"])
        dict_nuevo_empleado = nuevo_empleado.empleado_to_dict()
        df_nuevo_empleado = pd.DataFrame.from_dict(dict_nuevo_empleado)
        df_actualizado = PBT.concatenate_dataframes(self.__df_empleados, df_nuevo_empleado)
        return (df_actualizado.to_excel("Insumos/empleados.xlsx", index=False))
        

class Empleado:

    def __init__(self, nombre, id_empleado, rol, documento_licencia, horas_vuelo, estado_empleado, correo_electronico, disponible, ubicacion):
        self.__nombre = nombre
        self.__id_empleado = id_empleado
        self.__rol = rol
        self.__documento_licencia = documento_licencia
        self.__horas_vuelo = horas_vuelo
        self.__estado_empleado = estado_empleado
        self.__certificaciones = []
        self.__correo_electronico = correo_electronico
        self.__disponible_para_vuelo = {
            "Disponible": disponible,
            "Ubicacion": ubicacion
        }

    def actualizar_certificaciones(self, certificacion, fecha_emision, institucion_emisora):
        certificacion_dict = {
            "Certificacion" : certificacion,
            "Fecha" : fecha_emision,
            "Emisor" : institucion_emisora
        }
        self.__certificaciones.append(certificacion_dict)

    def disponible_para_vuelo(self):
        return self.__disponible_para_vuelo["Disponible"]

    def incrementar_horas_vuelo(self, horas):
        self.__horas_vuelo += horas

    def actualizar_estado_empleado(self, estado):
        self.__estado_empleado = estado


empleados = Empleados(config, {}, {})

empleados.__df_empleados._leer_info_empleados()

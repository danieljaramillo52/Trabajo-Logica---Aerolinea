import general_functions as gf

class Empleados:

    def __init__(self):
        self.__

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

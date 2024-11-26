from datetime import datetime
from typing import List

class GestionFBO:

    def __init__(self):
        self.__aviones = []
        self.__vuelos = []
        self.__empleados = []
        self.__servicios_mantenimiento = []

    def registrar_avion(self, avion):
        self.__aviones.append(avion)

    def programar_servicio_mantenimiento(self, mantenimiento):
        self.__servicios_mantenimiento.append(mantenimiento)

    def programar_vuelo(self, vuelo):
        self.__vuelos.append(vuelo)


class Avion:

    def __init__(self, matricula, tipo, modelo, fabricante, propietario, horas_vuelo, capacidad_pasajeros, peso_maximo_equipaje, disponible, horas_ultimo_mantenimiento, necesita_mantenimiento):
        self.__matricula = matricula
        self.__descripcion = {
            "Tipo": tipo,
            "Modelo": modelo,
            "Fabricante": fabricante,
            "Propietario": propietario
        }
        self.__horas_vuelo = horas_vuelo
        self.__capacidad_pasajeros = capacidad_pasajeros
        self.__peso_maximo_equipaje = peso_maximo_equipaje
        self.__disponible = disponible
        self.__horas_ultimo_mantenimiento = horas_ultimo_mantenimiento
        self.__necesita_mantenimiento = necesita_mantenimiento

    def verificar_disponibilidad(self):
        return self.__disponible

    def set_disponibilidad(self, disponible):
        self.__disponible = disponible

    def get_peso_maximo_equipaje(self):
        return self.__peso_maximo_equipaje

    def get_capacidad_pasajeros(self):
        return self.__capacidad_pasajeros

    def verificar_mantenimiento(self):
        return self.__necesita_mantenimiento or (self.__horas_vuelo - self.__horas_ultimo_mantenimiento >= 400)


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


class Mantenimiento:
    def __init__(self, avion, lider_tecnico, combustible_disponible, espacio_hangar_disponible, prioridad):
        self.__avion = avion
        self.__mantenimiento_historial = []
        self.__lider_tecnico = lider_tecnico
        self.__personal_mantenimiento = []
        self.__combustible_disponible = combustible_disponible
        self.__espacio_hangar_disponible = espacio_hangar_disponible
        self.__prioridad = prioridad
        self.__horas_ultimo_mantenimiento = 0
        self.__necesita_mantenimiento = False
        self.__historial_servicios = []

    def registrar_mantenimiento(self, descripcion: str, fecha: datetime, componentes_cambiados: List[str]):
        mantenimiento_dict = {
            "Descripcion" : descripcion,
            "Fecha" : fecha,
            "Repuestos" : componentes_cambiados
        }
        self.__mantenimiento_historial.append(mantenimiento_dict)

    def obtener_historial_mantenimiento(self):
        return self.__mantenimiento_historial

    def verificar_necesidad_mantenimiento(self, horas_vuelo: int, max_horas_mantenimiento: int) -> bool:
        self.__necesita_mantenimiento = (horas_vuelo - self.__horas_ultimo_mantenimiento) >= max_horas_mantenimiento
        return self.__necesita_mantenimiento
    
    def registrar_combutible(self, cantidad):
        if cantidad > 0:
            self.__combustible_disponible += cantidad
        else:
            print("La cantidad de combustible a registrar debe ser positiva.")

    def solicitar_combutible(self, cantidad):
        if cantidad > 0:
            if self.__combustible_disponible >= cantidad:
                self.__combustible_disponible -= cantidad
            else:
                print("No hay suficiente combustible disponible.")
        else:
            print("La cantidad de combustible solicitada debe ser positiva.")

    def asignar_hangar(self):
        if self.__espacio_hangar_disponible:
            self.__espacio_hangar_disponible -= 1
            return True
        return False

    def liberar_hangar(self):
        self.__espacio_hangar_disponible += 1

    def remolcar_aeronave(self):
        servicio = {
            "Servicio" : "Remolque",
            "Fecha" : datetime.now()
        }
        self.__historial_servicios.append(servicio)
        print("El servicio de remolque ha sido realizado con éxito.")

    def limpiar_aeronave(self):
        servicio = {
            "Servicio" : "Limpieza",
            "Fecha" : datetime.now()
        }
        self.__historial_servicios.append(servicio)
        print("El servicio de limpieza ha sido realizado con éxito.")

    def mostrar_historial_servicios(self):
        for servicio in self.__historial_servicios:
            print(f"Servicio: {servicio['Servicio']}, Fecha: {servicio['Fecha']}")
        

class Pasajero:

    def __init__(self, nombre, documento_identidad, edad, peso, vuelo, numero_asiento, estado_reserva):
        self.__nombre = nombre
        self.__documento_identidad = documento_identidad
        self.__edad = edad
        self.__equipaje = peso
        self.__vuelo = vuelo
        self.__estado_reserva = estado_reserva

    def calcular_peso_total_equipaje(self):
        return self.__equipaje["Peso"]

    def actualizar_datos(self, nombre=None, documento_identidad=None, edad=None):
        if nombre:
            self.__nombre = nombre
        if documento_identidad:
            self.__documento_identidad = documento_identidad
        if edad:
            self.__edad = edad

    def actualizar_equipaje(self, peso):
        self.__equipaje = peso

    def actualizar_reserva(self, vuelo, numero_asiento, estado_reserva):
        self.__vuelo = vuelo
        self.__numero_asiento = numero_asiento
        self.__estado_reserva = estado_reserva


class Tripulacion:

    def __init__(self, id_tripulacion, nombre, id_empleado, rol, documento_licencia, horas_vuelo):
        self.__id_tripulacion = id_tripulacion
        self.__nombre = nombre
        self.__id_empleado = id_empleado
        self.__rol = rol
        self.__documento_licencia = documento_licencia
        self.__horas_vuelo = horas_vuelo

    def actualizar_datos(self, nombre=None, rol=None, documento_licencia=None, horas_vuelo=None):
        if nombre:
            self.__nombre = nombre
        if rol:
            self.__rol = rol
        if documento_licencia:
            self.__documento_licencia = documento_licencia
        if horas_vuelo:
            self.__horas_vuelo = horas_vuelo


class Vuelo:

    def __init__(self, id_vuelo, tripulacion, contratante_vuelo, origen, destino, fecha_hora_salida, fecha_hora_llegada, avion, gerente_operaciones):
        self.__id_vuelo = id_vuelo
        self.__tripulacion = tripulacion
        self.__contratante_vuelo = contratante_vuelo
        self.__origen = origen
        self.__destino = destino
        self.__fecha_hora_salida = fecha_hora_salida
        self.__fecha_hora_llegada = fecha_hora_llegada
        self.__avion = avion
        self.__pasajeros = []
        self.__peso_equipaje_total = 0
        self.__gerente_operaciones = gerente_operaciones

    def calcular_peso_total_equipaje(self):
        self.__peso_equipaje_total = sum(pasajero.calcular_peso_total_equipaje() for pasajero in self.__pasajeros)
        return self.__peso_equipaje_total

    def agregar_pasajero(self, pasajero):
        if len(self.__pasajeros) < self.__avion.get_capacidad_pasajeros() and (self.calcular_peso_total_equipaje() + pasajero.calcular_peso_total_equipaje()) <= self.__avion.get_peso_maximo_equipaje():
            self.__pasajeros.append(pasajero)

    def asignar_avion(self, avion):
        self.__avion = avion


class Servicios:

    def __init__(self, id_vuelo, verificado, costo_total_servicios):
        self.__id_vuelo = id_vuelo
        self.__servicios_adicionales = []
        self.__verificado = verificado
        self.__costo_total_servicios = costo_total_servicios

    def calcular_costo_total(self):
        return sum(self.__costo_total_servicios)

    def verificar_servicio(self):
        self.__verificado = True

    def asignar_servicio(self, servicio, costo):
        self.__servicios_adicionales.append(servicio)
        self.__costo_total_servicios += costo

    def eliminar_servicio(self, servicio):
        if servicio in self.__servicios_adicionales:
            self.__servicios_adicionales.remove(servicio)
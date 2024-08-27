import uuid
print("Bienvenido a FBO, Vuele con nosotros hacia sus destinos soñados")
class avion:
    def __init__(self, pasajeros, peso):
        self.pasajeros = pasajeros
        self.peso = peso
        self.vuelos = []

    async def informacionvuelo(self, destino, origen, fecha, capacidad, pasajeros):
        vuelo = {
            "Id de vuelo" : uuid.uuid4(),
            "Destino" : destino,
            "Origen" : origen,
            "Fecha" : fecha,
            "Capacidad" : capacidad,
            "Pasajeros" : pasajeros,  
        }
        self.vuelos.append(vuelo)
        print(f"El vuelo con destino a {destino} sale desde {origen} con {pasajeros} abordados")

    async def calcularpeso(self, cantidadpeso):
        self.peso = cantidadpeso
    
class pasajero:
    def __init__(self, nombre, edad, equipaje):
        self.nombre = nombre
        self.edad = edad
        self.equipaje = equipaje


import general_functions as gf 

class Pasajero:
    def __init__(self, __config, __menu_pasajero=None):
        self.__config = __config
        self.__menu_pasajero = __menu_pasajero
        
    def mostrar_menu(self):
        eleccion = self.__config["Menu"]["menu_opcion"][8]
        gf.mostrar_menu_personalizado(eleccion,self.__menu_pasajero)    
    
    def ejecutar_proceso(self):            
        opcion_ingresada = input("Ingresa la opción a ejecutar:\n ")
        resultado = self.ejecutar_proceso_pasajero(opcion_ingresada)
        return resultado
    
    def ejecutar_proceso_pasajero(self, opcion: str) -> bool:
        """
        Ejecuta la opción seleccionada por el usuario y devuelve si debe continuar gestionando procesos.

        :param opcion: Opción seleccionada por el usuario.
        :return: True si se desea continuar, False si se regresa al menú principal.
        """
        opciones = {
            "1": self.metodo1,
            "2": self.metodo2,
            "3": self.realizar_mantenimiento,
            "4": 1,
            "5": 2,
            "0": 3
        }
        if opcion in opciones:
            if opcion == "0":  # Opción para salir directamente
                return False
            else:
                resultado = opciones[opcion]()
                print("Proceso terminado. \n")
                return  True

    def metodo1():
        pass
    
    def metodo2(): 
        pass
        


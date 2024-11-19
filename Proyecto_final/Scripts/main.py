import config_path_routes
import general_functions as gf
from gestion_fbo import GestionFBO, GenerarMenusFBO

CONFIG = "config.yml"

if __name__ == "__main__":
    
    # Procesar configuración inicial
    config = gf.Procesar_configuracion(CONFIG)

    lector_insumos =gf.ExcelReader(path=config["path_insumos"])
    
    df = lector_insumos.Lectura_simple_excel(nom_insumo=config["directorio_aviones"]["nom_base"], nom_hoja=config["directorio_aviones"]["nom_hoja"])
    
    # Crear instancia de la clase principal
    gestion_fbo = GestionFBO(config)
    

    # Crear instancia de la clase GenerarMenusFBO
    generador_menus = GenerarMenusFBO(gestion_fbo)
    dict_menus = generador_menus.ejecutar_proceso_menus()
    gestion_fbo._menu_principal(dict_menus=dict_menus)


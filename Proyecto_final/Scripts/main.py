import config_path_routes
import logger_function
import os
from datetime import datetime
from loguru import logger
import general_functions as gf
from transformation_functions import PandasBaseTransformer as PBT
from gestion_fbo import GestionFBO, GenerarMenusFBO

CONFIG = "config.yml"

if __name__ == "__main__":
    
    logger.info(f"Incio de un nuevo proceso:  {datetime.now()}")
    
    # Procesar configuración inicial
    config = gf.Procesar_configuracion(CONFIG)
    
    ## Crear instancia de la clase principal
    gestion_fbo = GestionFBO(config)
    #
    # Crear instancia de la clase GenerarMenusFBO
    generador_menus = GenerarMenusFBO(gestion_fbo)
    dict_menus = generador_menus.ejecutar_proceso_menus()
    gestion_fbo._menu_principal(dict_menus=dict_menus)
    
from loguru import logger 
import os

# Crear la carpeta `logger` si no existe
log_dir = "logger"
os.makedirs(log_dir, exist_ok=True)

    # Configurar Loguru
logger.add(
    os.path.join(log_dir, "Registro.log"), # Ruta del archivo de log
        rotation="10 MB",                      # Rotar el archivo cuando alcance 10 MB
        retention="7 days",                    # Retener logs durante 7 días
        compression="zip",                     # Comprimir logs rotados
        level="DEBUG",                         # Nivel mínimo de logging
        backtrace=True,                        # Agregar detalles de excepciones
        diagnose=True                          # Diagnóstico avanzado de errores
    )
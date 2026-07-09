"""
logger_config.py

Configura el logging del proyecto. En vez de usar print() para los
errores (que se pierden al cerrar la consola), todo evento importante
queda guardado en logs/software_fj.log.

Niveles usados:
  INFO  -> eventos normales (cliente registrado, reserva creada, etc.)
  ERROR -> excepciones ya controladas
"""

import logging
import os

CARPETA_LOGS = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(CARPETA_LOGS, exist_ok=True)

RUTA_LOG = os.path.join(CARPETA_LOGS, "software_fj.log")


def obtener_logger() -> logging.Logger:
    """Devuelve el logger del sistema, creándolo la primera vez."""
    logger = logging.getLogger("software_fj")

    # Si ya tiene handlers no volvemos a agregar (evita líneas duplicadas
    # cuando varios módulos importan esta función).
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        manejador_archivo = logging.FileHandler(RUTA_LOG, encoding="utf-8")
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        manejador_archivo.setFormatter(formato)
        logger.addHandler(manejador_archivo)

    return logger

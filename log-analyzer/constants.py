"""
constants.py
------------
Constantes utilizadas en todo el proyecto.
"""

# Título del menú principal
MENU_TITLE = (
    "==========================================\n"
    "            LOG ANALYZER\n"
    "=========================================="
)

# Opciones del menú principal
MENU_OPTIONS = (
    "1. Seleccionar archivo\n"
    "2. Salir"
)

# Niveles de severidad válidos
SEVERITY_LEVELS = (
    "INFO",
    "WARNING",
    "ERROR",
)

# Alias por compatibilidad (algunos módulos pueden referirse así)
VALID_LEVELS = SEVERITY_LEVELS

# Formato esperado para las fechas
DATE_FORMAT = "%Y-%m-%d"
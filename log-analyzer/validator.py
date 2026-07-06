"""
validator.py
-------------
Responsabilidad de este módulo (Iteración 3):
Aplicar las reglas de negocio sobre los datos extraídos por analyzer.py,
y decidir si una línea es válida o inválida.
"""

from datetime import datetime

from constants import SEVERITY_LEVELS, DATE_FORMAT


def es_fecha_valida(fecha_texto: str) -> bool:
    """
    Verifica si un texto representa una fecha real en formato YYYY-MM-DD,
    usando datetime.strptime() (no solo regex), para validar formato
    y existencia calendárica a la vez.
    """
    try:
        datetime.strptime(fecha_texto, DATE_FORMAT)
        return True
    except ValueError:
        return False


def validar_linea(datos_linea: dict) -> dict:
    """
    Recibe el diccionario de analyzer.analizar_linea() y determina si
    la línea es válida, aplicando las reglas del proyecto en orden fijo.
    """
    severidad = datos_linea["severidad"]
    fecha_texto = datos_linea["fecha_texto"]
    mensaje = datos_linea["mensaje"]

    tiene_fecha = fecha_texto is not None
    fecha_es_valida = es_fecha_valida(fecha_texto) if tiene_fecha else None

    if severidad is None:
        return {"es_valida": False, "tiene_fecha": tiene_fecha, "fecha_es_valida": fecha_es_valida, "motivo_invalidez": "sin_severidad"}

    if severidad not in SEVERITY_LEVELS:
        return {"es_valida": False, "tiene_fecha": tiene_fecha, "fecha_es_valida": fecha_es_valida, "motivo_invalidez": "severidad_invalida"}

    if tiene_fecha and not fecha_es_valida:
        return {"es_valida": False, "tiene_fecha": tiene_fecha, "fecha_es_valida": fecha_es_valida, "motivo_invalidez": "fecha_invalida"}

    if mensaje is None:
        return {"es_valida": False, "tiene_fecha": tiene_fecha, "fecha_es_valida": fecha_es_valida, "motivo_invalidez": "sin_mensaje"}

    return {"es_valida": True, "tiene_fecha": tiene_fecha, "fecha_es_valida": fecha_es_valida, "motivo_invalidez": None}


def validar_archivo(datos_lineas: list[dict]) -> list[dict]:
    """Aplica validar_linea() a cada elemento producido por analyzer.analizar_archivo()."""
    return [validar_linea(datos) for datos in datos_lineas]
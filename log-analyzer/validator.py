"""
validator.py
-------------
Responsabilidad de este módulo (Iteración 3):
Aplicar las REGLAS DE NEGOCIO definidas por el desarrollador sobre los
datos ya extraídos por analyzer.py, y decidir si una línea es válida
o inválida.

Reglas aplicadas (definidas por el desarrollador, no por la IA):
    - Inválida si no tiene severidad.
    - Inválida si la severidad no es INFO, WARNING o ERROR.
    - Inválida si tiene fecha pero esa fecha es inválida.
    - Inválida si no tiene mensaje.
    - Válida (y contada aparte) si no tiene fecha pero sí severidad y mensaje.
"""

from datetime import datetime

from constants import SEVERITY_LEVELS, DATE_FORMAT


def es_fecha_valida(fecha_texto: str) -> bool:
    """
    Verifica si un texto representa una fecha real en formato YYYY-MM-DD.

    Decisión de diseño:
    Usamos datetime.strptime() en vez de solo una expresión regular,
    porque una regex confirmaría que el TEXTO tiene forma de fecha
    (ej. "2025-13-40") pero no que esa fecha exista realmente en el
    calendario. strptime() valida formato Y validez calendárica en un
    solo paso.
    """
    try:
        datetime.strptime(fecha_texto, DATE_FORMAT)
        return True
    except ValueError:
        # strptime lanza ValueError tanto si el formato no coincide
        # (ej. "10-01-2025") como si la fecha no existe (ej. "2025-13-40").
        # Para las reglas de este proyecto, ambos casos significan lo mismo:
        # "fecha inválida".
        return False


def validar_linea(datos_linea: dict) -> dict:
    """
    Recibe el diccionario producido por analyzer.analizar_linea() y
    determina si la línea es válida, aplicando las reglas del proyecto.

    Retorna:
        {
            "es_valida": bool,
            "tiene_fecha": bool,
            "fecha_es_valida": bool | None,  # None si no había fecha
            "motivo_invalidez": str | None,
        }

    Decisión de diseño:
    Se revisan las reglas en un orden fijo y se retorna en el primer
    motivo de invalidez encontrado. No es necesario acumular varios
    motivos a la vez (el enunciado pide "el" motivo, no una lista),
    así que devolver el primero que aplique mantiene la función simple.
    """
    severidad = datos_linea["severidad"]
    fecha_texto = datos_linea["fecha_texto"]
    mensaje = datos_linea["mensaje"]

    tiene_fecha = fecha_texto is not None
    fecha_es_valida = es_fecha_valida(fecha_texto) if tiene_fecha else None

    # Regla 1: sin severidad -> inválida.
    if severidad is None:
        return {
            "es_valida": False,
            "tiene_fecha": tiene_fecha,
            "fecha_es_valida": fecha_es_valida,
            "motivo_invalidez": "sin_severidad",
        }

    # Regla 2: severidad presente pero no reconocida -> inválida.
    if severidad not in SEVERITY_LEVELS:
        return {
            "es_valida": False,
            "tiene_fecha": tiene_fecha,
            "fecha_es_valida": fecha_es_valida,
            "motivo_invalidez": "severidad_invalida",
        }

    # Regla 3: hay fecha pero es inválida -> inválida.
    if tiene_fecha and not fecha_es_valida:
        return {
            "es_valida": False,
            "tiene_fecha": tiene_fecha,
            "fecha_es_valida": fecha_es_valida,
            "motivo_invalidez": "fecha_invalida",
        }

    # Regla 4: sin mensaje -> inválida.
    if mensaje is None:
        return {
            "es_valida": False,
            "tiene_fecha": tiene_fecha,
            "fecha_es_valida": fecha_es_valida,
            "motivo_invalidez": "sin_mensaje",
        }

    # Si no se activó ninguna regla de invalidez, la línea es válida.
    # Esto incluye el caso explícito del enunciado: severidad + mensaje,
    # sin fecha -> válida, pero con tiene_fecha=False para que report.py
    # la cuente como "evento sin fecha".
    return {
        "es_valida": True,
        "tiene_fecha": tiene_fecha,
        "fecha_es_valida": fecha_es_valida,
        "motivo_invalidez": None,
    }


def validar_archivo(datos_lineas: list[dict]) -> list[dict]:
    """
    Aplica validar_linea() a cada diccionario de una lista producida
    por analyzer.analizar_archivo().
    """
    return [validar_linea(datos) for datos in datos_lineas]
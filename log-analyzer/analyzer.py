"""
analyzer.py
-----------
Responsabilidad de este módulo (Iteración 2):
Recorrer las líneas del archivo y extraer de cada una sus componentes:
severidad, fecha (si existe) y mensaje.

Este módulo NO decide si una línea es válida o no (eso es trabajo de
validator.py, Iteración 3). Su única tarea es "descomponer" una línea
de texto en sus partes.
"""

import re

# Patrón para capturar la severidad entre corchetes al inicio de la línea.
# Ejemplo: "[INFO] 2025-01-10 mensaje" -> grupo 1 = "INFO", grupo 2 = resto.
# Usamos \w+ (no solo INFO|WARNING|ERROR) a propósito: si alguien escribe
# "[DEBUG]" queremos CAPTURARLO igual, para que validator.py pueda
# rechazarlo como "severidad inválida". Si el regex solo aceptara los
# tres valores válidos, "DEBUG" pasaría desapercibido como si no hubiera
# severidad en absoluto, y esa es una decisión distinta con otro
# significado (línea sin severidad vs. severidad inválida).
PATRON_SEVERIDAD = re.compile(r"^\[(\w+)\]\s*(.*)$")

# Patrón para detectar un "candidato a fecha": tres grupos de dígitos
# separados por guiones, al inicio del texto restante.
# Ejemplo: "2025-01-10 mensaje" -> grupo 1 = "2025-01-10", grupo 2 = resto.
# Importante: este patrón NO valida que la fecha sea real (no rechaza
# "2025-13-45"). Eso es intencional: aquí solo identificamos que "algo
# con forma de fecha" está presente. La validación real con
# datetime.strptime() ocurre en validator.py (Iteración 3).
PATRON_FECHA_CANDIDATA = re.compile(r"^(\d+-\d+-\d+)\s*(.*)$")


def analizar_linea(linea: str) -> dict:
    """
    Analiza una única línea de log y extrae sus componentes.

    Retorna un diccionario:
        {
            "severidad": str | None,
            "fecha_texto": str | None,
            "mensaje": str | None,
        }

    Decisión de diseño:
    Cada campo ausente se representa como None, nunca como string
    vacío (""). Esto hace inequívoco, en validator.py, escribir
    `if datos["mensaje"] is None:` en vez de tener que comparar contra
    "" y preguntarse si un mensaje vacío intencional sería diferente
    de uno ausente (no lo es, en este proyecto, pero el código queda
    más claro expresándolo así).
    """
    linea_limpia = linea.strip()

    # Caso borde: línea vacía o solo espacios.
    # No tiene severidad, fecha ni mensaje que extraer.
    if not linea_limpia:
        return {"severidad": None, "fecha_texto": None, "mensaje": None}

    severidad = None
    resto = linea_limpia

    coincidencia_severidad = PATRON_SEVERIDAD.match(linea_limpia)
    if coincidencia_severidad:
        severidad = coincidencia_severidad.group(1)
        resto = coincidencia_severidad.group(2).strip()
    # Si no hay corchetes al inicio, "severidad" queda en None y "resto"
    # sigue siendo la línea completa: puede que exista fecha y mensaje
    # de todas formas, aunque la línea ya sea inválida por falta de
    # severidad (esa decisión la toma validator.py, no este módulo).

    fecha_texto = None
    mensaje = resto

    coincidencia_fecha = PATRON_FECHA_CANDIDATA.match(resto)
    if coincidencia_fecha:
        fecha_texto = coincidencia_fecha.group(1)
        mensaje = coincidencia_fecha.group(2).strip()

    # Si después de quitar severidad y fecha no queda texto, no hay mensaje.
    mensaje = mensaje if mensaje else None

    return {
        "severidad": severidad,
        "fecha_texto": fecha_texto,
        "mensaje": mensaje,
    }


def analizar_archivo(lineas: list[str]) -> list[dict]:
    """
    Aplica analizar_linea() a cada línea de una lista de líneas.

    Decisión de diseño:
    Esta función es intencionalmente una línea de código (además de la
    firma y el docstring). No hay lógica que "envolver" aquí: es una
    aplicación directa de analizar_linea() a toda la lista. Mantenerla
    como función separada (en vez de hacer el bucle directo en main.py)
    conserva la regla de que main.py no contiene lógica de negocio.
    """
    return [analizar_linea(linea) for linea in lineas]
"""
report.py
---------
Responsabilidad de este módulo (a partir de la Iteración 4):
Tomar los resultados de validación de TODAS las líneas y generar:
    1. Las estadísticas del análisis (conteos por severidad, líneas
       inválidas, líneas sin fecha, fechas inválidas, total de eventos).
    2. El reporte final, impreso en consola de forma clara y organizada.

Por qué separar "calcular estadísticas" de "imprimir el reporte":
Aunque ambas cosas viven en el mismo archivo, se implementarán como
funciones distintas. Calcular las estadísticas es lógica pura (recibe
datos, retorna números); imprimir es solo presentación. Mantenerlas
separadas permite, por ejemplo, escribir una prueba automatizada para
generar_estadisticas() sin necesitar capturar texto de consola.

Estado actual: ESQUELETO (Iteración 1).
La implementación real se agrega en la Iteración 4.
"""


def generar_estadisticas(resultados_validacion: list[dict]) -> dict:
    """
    Recorre los resultados de validación de todas las líneas y calcula
    los contadores pedidos en el proyecto.

    Parámetros:
        resultados_validacion: lista de diccionarios, uno por línea,
        tal como los produce validator.validar_linea().

    Retorna (a partir de la Iteración 4):
        Un diccionario con, como mínimo:
        {
            "total_eventos": int,
            "conteo_por_severidad": {"INFO": int, "WARNING": int, "ERROR": int},
            "lineas_invalidas": int,
            "lineas_sin_fecha": int,
            "fechas_invalidas": int,
        }

    Estado actual: no implementado todavía.
    """
    raise NotImplementedError("generar_estadisticas() se implementará en la Iteración 4")


def mostrar_reporte(estadisticas: dict, nombre_archivo: str, tiempo_ejecucion: float) -> None:
    """
    Imprime en consola el reporte final del análisis, de forma clara
    y organizada.

    Parámetros:
        estadisticas: diccionario producido por generar_estadisticas().
        nombre_archivo: nombre del archivo analizado (para mostrarlo
        en el encabezado del reporte, como pide el enunciado).
        tiempo_ejecucion: segundos que tardó el análisis, para la
        mejora adicional de "medir el tiempo de ejecución".

    Estado actual: no implementado todavía.
    """
    raise NotImplementedError("mostrar_reporte() se implementará en la Iteración 4")
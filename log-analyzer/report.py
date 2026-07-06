"""
report.py
---------
Responsabilidad de este módulo (Iteración 4):
Tomar los resultados de validación de todas las líneas y generar:
    1. Las estadísticas del análisis.
    2. El reporte final, impreso en consola de forma clara y organizada.
"""

from collections import Counter

from constants import SEVERITY_LEVELS


def generar_estadisticas(datos_lineas: list[dict], resultados_validacion: list[dict]) -> dict:
    """
    Calcula los contadores pedidos en el proyecto.

    Parámetros:
        datos_lineas: lista producida por analyzer.analizar_archivo()
        (se necesita para saber la severidad real de cada línea).
        resultados_validacion: lista producida por
        validator.validar_archivo() (misma posición/índice que
        datos_lineas, línea por línea).

    Retorna:
        {
            "total_eventos": int,
            "conteo_por_severidad": {"INFO": int, "WARNING": int, "ERROR": int},
            "lineas_invalidas": int,
            "lineas_sin_fecha": int,
            "fechas_invalidas": int,
        }

    Decisión de diseño:
    Recibimos DOS listas (datos_lineas y resultados_validacion) en vez
    de una sola combinada, porque analyzer.py y validator.py ya
    producen cada una la suya, y combinarlas antes obligaría a crear
    una tercera estructura intermedia solo para este propósito. Como
    ambas listas mantienen el mismo orden de líneas, se pueden recorrer
    en paralelo con zip() sin perder información.
    """
    conteo_por_severidad = Counter()
    lineas_invalidas = 0
    lineas_sin_fecha = 0
    fechas_invalidas = 0
    # "Total de eventos analizados": interpretamos "evento" como toda
    # línea válida (según la definición del enunciado: una línea sin
    # fecha pero con severidad y mensaje SÍ es un evento válido).
    # Las líneas inválidas no se cuentan como eventos.
    total_eventos = 0

    for datos, resultado in zip(datos_lineas, resultados_validacion):
        severidad = datos["severidad"]

        if resultado["fecha_es_valida"] is False:
            fechas_invalidas += 1

        if not resultado["es_valida"]:
            lineas_invalidas += 1
            continue  # Una línea inválida no se cuenta como evento.

        # A partir de aquí, la línea es válida.
        total_eventos += 1

        if severidad in SEVERITY_LEVELS:
            conteo_por_severidad[severidad] += 1

        if not resultado["tiene_fecha"]:
            lineas_sin_fecha += 1

    return {
        "total_eventos": total_eventos,
        # Se construye explícitamente con las 3 severidades en orden,
        # aunque su conteo sea 0, para que el reporte siempre muestre
        # las tres categorías (mejor que un Counter que podría omitir
        # una severidad si nunca apareció).
        "conteo_por_severidad": {
            nivel: conteo_por_severidad.get(nivel, 0) for nivel in SEVERITY_LEVELS
        },
        "lineas_invalidas": lineas_invalidas,
        "lineas_sin_fecha": lineas_sin_fecha,
        "fechas_invalidas": fechas_invalidas,
    }


def mostrar_reporte(estadisticas: dict, nombre_archivo: str, fecha_hora_analisis: str, tiempo_ejecucion: float) -> None:
    """
    Imprime en consola el reporte final del análisis.

    Parámetros:
        estadisticas: diccionario producido por generar_estadisticas().
        nombre_archivo: nombre del archivo analizado.
        fecha_hora_analisis: momento en que se ejecutó el análisis,
        ya formateado como texto.
        tiempo_ejecucion: segundos que tardó el análisis (float).

    Decisión de diseño:
    Esta función solo imprime; no calcula nada. Recibe todos los datos
    ya listos para no mezclar lógica de cálculo con presentación
    (principio de responsabilidad única, igual que en el resto del
    proyecto).
    """
    total = estadisticas["total_eventos"]
    por_severidad = estadisticas["conteo_por_severidad"]

    print("\n" + "=" * 40)
    print("REPORTE FINAL - LOG ANALYZER")
    print("=" * 40)
    print(f"Archivo analizado : {nombre_archivo}")
    print(f"Fecha de análisis : {fecha_hora_analisis}")
    print(f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos")
    print("-" * 40)
    print(f"Total de eventos válidos : {total}")
    print("Eventos por severidad:")
    for nivel in SEVERITY_LEVELS:
        print(f"    {nivel:<8}: {por_severidad[nivel]}")
    print("-" * 40)
    print(f"Líneas inválidas    : {estadisticas['lineas_invalidas']}")
    print(f"Líneas sin fecha    : {estadisticas['lineas_sin_fecha']}")
    print(f"Fechas inválidas    : {estadisticas['fechas_invalidas']}")
    print("=" * 40)
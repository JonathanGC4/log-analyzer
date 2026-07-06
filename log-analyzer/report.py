"""
report.py
---------
Responsabilidad de este módulo (Iteración 4):
Calcular estadísticas a partir de los resultados de validación, e
imprimir el reporte final en consola.
"""

from collections import Counter

from constants import SEVERITY_LEVELS


def generar_estadisticas(datos_lineas: list[dict], resultados_validacion: list[dict]) -> dict:
    """
    Calcula los contadores pedidos en el proyecto, recorriendo en
    paralelo los datos extraídos y sus resultados de validación.
    """
    conteo_por_severidad = Counter()
    lineas_invalidas = 0
    lineas_sin_fecha = 0
    fechas_invalidas = 0
    total_eventos = 0  # "evento" = línea válida, según la definición del enunciado.

    for datos, resultado in zip(datos_lineas, resultados_validacion):
        severidad = datos["severidad"]

        if resultado["fecha_es_valida"] is False:
            fechas_invalidas += 1

        if not resultado["es_valida"]:
            lineas_invalidas += 1
            continue

        total_eventos += 1

        if severidad in SEVERITY_LEVELS:
            conteo_por_severidad[severidad] += 1

        if not resultado["tiene_fecha"]:
            lineas_sin_fecha += 1

    return {
        "total_eventos": total_eventos,
        "conteo_por_severidad": {nivel: conteo_por_severidad.get(nivel, 0) for nivel in SEVERITY_LEVELS},
        "lineas_invalidas": lineas_invalidas,
        "lineas_sin_fecha": lineas_sin_fecha,
        "fechas_invalidas": fechas_invalidas,
    }


def mostrar_reporte(estadisticas: dict, nombre_archivo: str, fecha_hora_analisis: str, tiempo_ejecucion: float) -> None:
    """Imprime en consola el reporte final del análisis. Solo presenta, no calcula."""
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
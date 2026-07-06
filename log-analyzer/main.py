"""
main.py
-------
Punto de entrada del programa. Flujo: file_manager -> analyzer -> validator -> report.
"""

import time
from datetime import datetime

from constants import MENU_TITLE, MENU_OPTIONS
import file_manager
import analyzer
import validator
import report


def mostrar_menu() -> None:
    print("\n" + MENU_TITLE)
    print(MENU_OPTIONS)


def analizar_archivo() -> None:
    ruta_archivo = file_manager.select_file()

    if ruta_archivo is None:
        print("\nNo se seleccionó ningún archivo. Operación cancelada.")
        return

    lineas = file_manager.read_lines(ruta_archivo)

    if not lineas:
        print("El archivo está vacío o no se pudo leer.")
        return

    inicio = time.perf_counter()

    datos_lineas = analyzer.analizar_archivo(lineas)
    resultados_validacion = validator.validar_archivo(datos_lineas)
    estadisticas = report.generar_estadisticas(datos_lineas, resultados_validacion)

    tiempo_ejecucion = time.perf_counter() - inicio

    nombre_archivo = file_manager.get_file_name(ruta_archivo)
    fecha_hora_analisis = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report.mostrar_reporte(estadisticas, nombre_archivo, fecha_hora_analisis, tiempo_ejecucion)


def main() -> None:
    while True:
        mostrar_menu()
        opcion = input("\nElige una opción: ").strip()

        if opcion == "1":
            analizar_archivo()
        elif opcion == "2":
            print("\nSaliendo del programa. ¡Hasta luego!")
            break
        else:
            print("\nOpción no válida. Por favor elige 1 o 2.")


if __name__ == "__main__":
    main()
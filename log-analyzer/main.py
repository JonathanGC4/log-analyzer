"""
main.py
-------
Punto de entrada del programa. Su única responsabilidad es manejar
el FLUJO de la aplicación: mostrar el menú, leer la opción del usuario
y llamar a las funciones de los demás módulos en el orden correcto.

A partir de la Iteración 4, el flujo completo es:
    file_manager -> analyzer -> validator -> report
"""

import time
from datetime import datetime

from constants import MENU_TITLE, MENU_OPTIONS
import file_manager
import analyzer
import validator
import report


def mostrar_menu() -> None:
    """Imprime el menú principal en consola."""
    print("\n" + MENU_TITLE)
    print(MENU_OPTIONS)


def analizar_archivo() -> None:
    """
    Flujo completo de la opción 1 del menú:
    seleccionar archivo -> leer -> analizar -> validar -> reportar.

    Decisión de diseño:
    main.py encadena las salidas de cada módulo como entradas del
    siguiente (lineas -> datos_lineas -> resultados_validacion ->
    estadisticas), sin transformar los datos él mismo. Toda la lógica
    real vive en los módulos; aquí solo se define EL ORDEN en que se
    ejecutan.
    """
    ruta_archivo = file_manager.select_file()

    if ruta_archivo is None:
        print("\nNo se seleccionó ningún archivo. Operación cancelada.")
        return

    lineas = file_manager.read_lines(ruta_archivo)

    if not lineas:
        # Cubre archivo vacío y errores de lectura (ya reportados
        # dentro de file_manager con un mensaje específico).
        print("El archivo está vacío o no se pudo leer.")
        return

    # Se mide el tiempo de ejecución solo alrededor del análisis en sí
    # (no de la selección del archivo, que depende de cuánto tarde el
    # usuario en elegir uno, y no del rendimiento del programa).
    inicio = time.perf_counter()

    datos_lineas = analyzer.analizar_archivo(lineas)
    resultados_validacion = validator.validar_archivo(datos_lineas)
    estadisticas = report.generar_estadisticas(datos_lineas, resultados_validacion)

    tiempo_ejecucion = time.perf_counter() - inicio

    nombre_archivo = file_manager.get_file_name(ruta_archivo)
    fecha_hora_analisis = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report.mostrar_reporte(estadisticas, nombre_archivo, fecha_hora_analisis, tiempo_ejecucion)


def main() -> None:
    """
    Bucle principal del programa. Se repite mostrando el menú hasta
    que el usuario elige salir.
    """
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
# Log Analyzer

Aplicación de consola en Python que analiza archivos de texto (`.txt`)
que simulan registros (logs) de una aplicación. Detecta el nivel de
severidad, la fecha y el mensaje de cada línea, valida su estructura
según reglas definidas por el desarrollador, y genera un reporte final
con estadísticas claras.

## Objetivo del proyecto

Este proyecto es un ejercicio académico cuyo propósito es demostrar el
uso de la Inteligencia Artificial como **herramienta de apoyo al
desarrollo** (vibecoding) — no como reemplazo del desarrollador. Todas
las reglas de negocio (qué hace válida o inválida a una línea) fueron
definidas por el desarrollador; la IA se usó para traducir esas reglas
a código, explicando cada decisión de diseño en el camino.

## Requisitos

- Python 3.10 o superior (usa la sintaxis `list[str]` y `str | None`).
- `tkinter` (incluido con Python en la mayoría de instalaciones; en
  Linux puede requerir `sudo apt-get install python3-tk`).
- No se necesitan dependencias externas (ver `requirements.txt`).

## Estructura del proyecto
log-analyzer/
├── main.py            # Punto de entrada: menú y flujo del programa
├── analyzer.py         # Extrae severidad, fecha y mensaje de cada línea
├── validator.py        # Aplica las reglas de validación
├── report.py           # Calcula estadísticas y muestra el reporte final
├── file_manager.py     # Selección (tkinter) y lectura de archivos
├── constants.py        # Constantes: severidades válidas, formato de fecha, textos de menú
├── test_logs/
│   ├── logs_correctos.txt
│   ├── logs_incorrectos.txt
│   └── logs_mixtos.txt
├── README.md
├── REFLEXION.md
├── requirements.txt
└── .gitignore
Cada módulo tiene una responsabilidad única:
- **file_manager.py** — todo lo relacionado al sistema de archivos.
- **analyzer.py** — descompone una línea en sus partes (severidad, fecha, mensaje), sin decidir si son válidas.
- **validator.py** — decide si una línea es válida, aplicando las reglas del negocio.
- **report.py** — calcula estadísticas y las imprime en consola.
- **main.py** — orquesta el flujo completo, sin contener lógica de negocio.

## Cómo ejecutarlo

```bash
python main.py
```

Se mostrará un menú:
1.Seleccionar archivo
2.Salir

Al elegir `1`, se abre un explorador de archivos para seleccionar un
`.txt`. El programa lo analiza y muestra un reporte final en consola.

## Reglas de validación

Una línea se considera **inválida** cuando:
- No tiene nivel de severidad.
- El nivel de severidad no es `INFO`, `WARNING` o `ERROR`.
- Tiene una fecha, pero esa fecha es inválida (formato o mes/día inexistente).
- No tiene mensaje.

Una línea **sin fecha**, pero con severidad y mensaje, se considera
**válida** y además se cuenta aparte como "evento sin fecha".

Las fechas válidas deben tener el formato `YYYY-MM-DD`, y se validan
con `datetime.strptime()` — no solo con expresiones regulares — para
garantizar que la fecha exista realmente en el calendario (por ejemplo,
`2025-13-40` tiene el formato correcto pero no es una fecha real).

## Archivos de prueba

La carpeta `test_logs/` incluye tres archivos para verificar el
comportamiento del programa:

| Archivo | Contenido |
|---|---|
| `logs_correctos.txt` | Todas las líneas válidas |
| `logs_incorrectos.txt` | Todas las líneas inválidas, una por cada regla |
| `logs_mixtos.txt` | Combinación real de líneas válidas e inválidas |

## Uso de Inteligencia Artificial en este proyecto

Este proyecto se desarrolló con apoyo de un asistente de IA para
escribir y explicar el código, pero todas las decisiones de diseño y
las reglas de negocio fueron definidas por el desarrollador. El detalle
completo de este proceso está documentado en `REFLEXION.md`.
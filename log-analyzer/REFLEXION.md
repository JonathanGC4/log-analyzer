# Reflexión técnica: uso de la IA en el desarrollo de Log Analyzer

## Propósito de este documento

Este proyecto fue diseñado para demostrar el uso de la Inteligencia
Artificial como **herramienta de apoyo al desarrollo** (vibecoding), y
no como un reemplazo del desarrollador. Este documento explica cómo se
dividieron las responsabilidades entre el desarrollador y la IA durante
la construcción de Log Analyzer.

## Qué decisiones tomé yo (el desarrollador)

Todas las **reglas de negocio** del programa fueron definidas por mí
antes de escribir cualquier código, y se respetaron sin cambios durante
todo el desarrollo:

- Los tres niveles de severidad válidos: `INFO`, `WARNING`, `ERROR`.
- El formato de fecha aceptado: `YYYY-MM-DD`.
- Las condiciones exactas que hacen inválida a una línea (sin
  severidad, severidad no reconocida, fecha inválida, sin mensaje).
- La regla especial de que una línea sin fecha (pero con severidad y
  mensaje) es válida, y se cuenta aparte como "evento sin fecha".
- La arquitectura modular del proyecto (qué archivo se encarga de qué).
- El orden de las iteraciones de desarrollo.

También decidí, en cada paso, si aceptaba o pedía cambios sobre el
código que la IA proponía, revisando cada función antes de guardarla
como archivo definitivo.

## Cómo se usó la IA

La IA se usó como asistente de programación para:

- Traducir las reglas de negocio que yo definí a código Python.
- Proponer una arquitectura modular (separar `analyzer.py`,
  `validator.py`, `report.py`, `file_manager.py`) que respetara el
  principio de responsabilidad única.
- Explicar, en comentarios y en la conversación, el porqué de cada
  decisión técnica (por ejemplo, por qué usar `datetime.strptime()` en
  vez de solo expresiones regulares para validar fechas).
- Simular el flujo del programa con datos de prueba antes de guardar
  archivos definitivos, para detectar errores temprano.
- Ayudarme a diagnosticar problemas del entorno (por ejemplo, que
  `python3` no es un comando válido en Windows y hay que usar `python`,
  o que la extensión `.txt` puede quedar oculta al guardar un archivo).

En ningún momento la IA decidió por sí sola una regla de negocio nueva:
cuando encontró una ambigüedad (por ejemplo, qué hacer si una línea
viola varias reglas a la vez), propuso una opción razonada y me la
presentó como decisión a confirmar, no como un hecho ya resuelto.

## Dificultades encontradas

- **Diferencias entre `analyzer.py` y `validator.py`:** al principio no
  era obvio por qué separar "extraer los datos de una línea" de
  "decidir si es válida". Entender que son dos preguntas distintas
  ("¿qué contiene esta línea?" vs. "¿esta línea cumple las reglas?")
  ayudó a que el código fuera más fácil de probar por partes.
- **Validación de fechas:** confirmar que `2025-13-40` es inválida por
  el mes, no solo por el formato, requirió usar `datetime.strptime()`
  en vez de una expresión regular simple.
- **Entorno de Windows:** el comando `python3` no funcionaba porque
  Windows solo reconoce `python`, y además Python no estaba instalado
  realmente (solo existía el acceso directo a la Microsoft Store).
  Hubo que instalarlo manualmente y asegurarse de marcar la opción
  "Add python.exe to PATH" durante la instalación.

## Aprendizajes

- La separación de responsabilidades entre módulos hace que el código
  sea mucho más fácil de probar: cada función se pudo verificar de
  forma aislada con datos de ejemplo antes de integrarla al flujo
  completo.
- Usar `datetime.strptime()` en vez de solo regex es una decisión que
  vale la pena documentar explícitamente, porque no es obvia a primera
  vista por qué una regex no es suficiente para validar fechas reales.
- Probar con archivos reales (`test_logs/logs_correctos.txt`,
  `logs_incorrectos.txt`, `logs_mixtos.txt`) antes de considerar el
  proyecto terminado permitió confirmar que las reglas se comportaban
  como se esperaba en casos concretos, no solo en teoría.
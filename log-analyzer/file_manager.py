"""
file_manager.py
----------------
Responsabilidad:
- Permitir al usuario seleccionar un archivo.
- Leer el contenido del archivo.
- Obtener el nombre del archivo.
"""

from pathlib import Path
from tkinter import Tk, filedialog


def select_file() -> str | None:
    """
    Abre un explorador de archivos para seleccionar un archivo .txt.
    Devuelve la ruta del archivo o None si el usuario cancela.
    """
    root = Tk()
    root.withdraw()          # Oculta la ventana principal de Tkinter
    root.attributes("-topmost", True)

    file_path = filedialog.askopenfilename(
        title="Selecciona un archivo de logs",
        filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
    )

    root.destroy()

    if file_path == "":
        return None

    return file_path


def read_lines(file_path: str) -> list[str]:
    """
    Lee todas las líneas del archivo.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.readlines()
    except Exception as error:
        print(f"\nError al leer el archivo: {error}")
        return []


def get_file_name(file_path: str) -> str:
    """
    Devuelve únicamente el nombre del archivo.
    """
    return Path(file_path).name
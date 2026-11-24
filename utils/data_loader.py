"""Lectura de los datos de prueba guardados en archivos externos (carpeta data/)."""

import csv
import json
from pathlib import Path

CARPETA_DATOS = Path(__file__).resolve().parent.parent / "data"


def leer_json(nombre_archivo):
    """Lee un archivo JSON de la carpeta data/ y devuelve su contenido."""
    with open(CARPETA_DATOS / nombre_archivo, encoding="utf-8") as archivo:
        return json.load(archivo)


def leer_csv(nombre_archivo):
    """Lee un archivo CSV de la carpeta data/ y devuelve una lista de diccionarios
    (uno por fila, con los encabezados como claves)."""
    with open(CARPETA_DATOS / nombre_archivo, encoding="utf-8", newline="") as archivo:
        return list(csv.DictReader(archivo))


def generar_ids(casos, clave="id"):
    """Devuelve los nombres que se muestran en el reporte para cada caso parametrizado."""
    return [caso[clave] for caso in casos]

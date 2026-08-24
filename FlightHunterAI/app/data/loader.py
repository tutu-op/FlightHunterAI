import csv
from pathlib import Path

RUTA = Path(__file__).parent / "airports.csv"


def cargar_aeropuertos():

    aeropuertos = []

    with open(RUTA, encoding="utf-8") as archivo:

        lector = csv.DictReader(archivo)

        for fila in lector:

            if fila["iata_code"]:

                aeropuertos.append({
                    "nombre": fila["name"],
                    "ciudad": fila["municipality"],
                    "pais": fila["iso_country"],
                    "iata": fila["iata_code"],
                    "latitud": fila["latitude_deg"],
                    "longitud": fila["longitude_deg"]
                })

    return aeropuertos
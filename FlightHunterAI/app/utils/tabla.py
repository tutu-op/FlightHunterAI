from rich.table import Table
from rich.console import Console


console = Console()


def mostrar_vuelos(vuelos):

    tabla = Table(title="FlightHunter AI")

    tabla.add_column("Proveedor")
    tabla.add_column("Aerolínea")
    tabla.add_column("Origen")
    tabla.add_column("Destino")
    tabla.add_column("Precio")
    tabla.add_column("Escalas")

    for vuelo in vuelos:

        tabla.add_row(

            vuelo.proveedor,

            vuelo.aerolinea,

            vuelo.origen,

            vuelo.destino,

            f"${vuelo.precio:,.0f}",

            str(vuelo.escalas)

        )

    console.print(tabla)
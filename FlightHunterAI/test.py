from app.services.buscador import BuscadorVuelos
from app.utils.tabla import mostrar_vuelos


buscador = BuscadorVuelos()

vuelos = buscador.buscar("GDL", "NRT")

mostrar_vuelos(vuelos)
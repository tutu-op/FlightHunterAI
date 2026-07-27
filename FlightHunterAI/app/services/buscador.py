from app.providers.manager import ProviderManager
from app.services.comparador import Comparador


class BuscadorVuelos:

    def __init__(self):
        self.manager = ProviderManager()

    def buscar(
        self,
        origen,
        destino,
        fecha_salida,
        fecha_regreso=None,
        adultos=1
    ):

        vuelos = []

        for provider in self.manager.obtener_providers():

            try:

                vuelos.extend(
                    provider.buscar(
                        origen,
                        destino,
                        fecha_salida,
                        fecha_regreso,
                        adultos
                    )
                )

            except Exception as e:
                print(f"Error en {provider.__class__.__name__}: {e}")

        vuelos = Comparador.eliminar_duplicados(vuelos)
        vuelos = Comparador.ordenar_por_precio(vuelos)

        return vuelos
from app.providers.manager import ProviderManager
from app.services.comparador import Comparador
import traceback


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

            print(f"\n========== Consultando {provider.__class__.__name__} ==========")

            try:

                resultado = provider.buscar(
                    origen,
                    destino,
                    fecha_salida,
                    fecha_regreso,
                    adultos
                )

                print(f"{provider.__class__.__name__} devolvió {len(resultado)} vuelos")

                vuelos.extend(resultado)

            except Exception:

                print(f"Error en {provider.__class__.__name__}")
                traceback.print_exc()

        vuelos = Comparador.eliminar_duplicados(vuelos)
        vuelos = Comparador.ordenar_por_precio(vuelos)

        return vuelos
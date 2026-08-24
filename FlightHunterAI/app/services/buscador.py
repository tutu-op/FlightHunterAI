from app.providers.manager import ProviderManager
from app.services.comparador import Comparador
from app.services.iata import obtener_codigo
from app.services.evaluador import Evaluador
from app.services.scoring import FlightHunterScore

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

        # Convertir ciudad -> código IATA
        origen = obtener_codigo(origen)
        destino = obtener_codigo(destino)

        print(f"Origen convertido: {origen}")
        print(f"Destino convertido: {destino}")

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

            except Exception as e:
                print(f"Error en {provider.__class__.__name__}: {e}")

        # Eliminar vuelos duplicados
        vuelos = Comparador.eliminar_duplicados(vuelos)

        # Evaluar los vuelos
        vuelos = Evaluador.evaluar(vuelos)

        # Calcular FlightHunter Score
        vuelos = [FlightHunterScore.calcular(v) for v in vuelos]

        # Ordenar por Score (descendente) y luego por precio (ascendente)
        vuelos.sort(
            key=lambda v: (-v.score, v.precio)
        )

        return vuelos
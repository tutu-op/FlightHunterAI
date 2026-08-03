import httpx

from app.providers.provider import Provider
from app.models.vuelo import Vuelo
from app.config import DUFFEL_API_KEY


class DuffelProvider(Provider):

    def buscar(
        self,
        origen,
        destino,
        fecha_salida,
        fecha_regreso=None,
        adultos=1
    ):

        headers = {
            "Authorization": f"Bearer {DUFFEL_API_KEY}",
            "Duffel-Version": "v2",
            "Content-Type": "application/json"
        }

        body = {
            "data": {
                "slices": [
                    {
                        "origin": origen,
                        "destination": destino,
                        "departure_date": fecha_salida
                    }
                ],
                "passengers": [
                    {
                        "type": "adult"
                    } for _ in range(adultos)
                ],
                "cabin_class": "economy"
            }
        }

        try:

            respuesta = httpx.post(
                "https://api.duffel.com/air/offer_requests",
                headers=headers,
                json=body,
                timeout=30
            )

            print("STATUS:", respuesta.status_code)

            if respuesta.status_code != 201:
                print(respuesta.text)
                return []

            datos = respuesta.json()

            vuelos = []

            ofertas = datos.get("data", {}).get("offers", [])

            print(f"Se recibieron {len(ofertas)} ofertas.")

            for oferta in ofertas:

                try:

                    slice_ = oferta["slices"][0]
                    segmentos = slice_["segments"]
                    primer_segmento = segmentos[0]
                    ultimo_segmento = segmentos[-1]

                    vuelos.append(

                        Vuelo(

                            proveedor="Duffel",

                            aerolinea=oferta["owner"]["name"],

                            origen=origen,

                            destino=destino,

                            fecha_salida=fecha_salida,

                            fecha_regreso=fecha_regreso,

                            salida=primer_segmento["departing_at"],

                            llegada=ultimo_segmento["arriving_at"],

                            precio=float(oferta["total_amount"]),

                            moneda=oferta["total_currency"],

                            escalas=len(segmentos) - 1,

                            enlace=None

                        )

                    )

                except Exception as e:

                    print("Error procesando oferta:", e)

            print(f"Se convirtieron {len(vuelos)} vuelos.")

            return vuelos

        except Exception as e:

            print("ERROR GENERAL:", e)

            return []
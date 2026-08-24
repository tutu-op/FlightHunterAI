import httpx

from app.config import DUFFEL_API_KEY


class OfertaDuffel:

    @staticmethod
    def obtener(offer_id):

        headers = {
            "Authorization": f"Bearer {DUFFEL_API_KEY}",
            "Duffel-Version": "v2",
            "Content-Type": "application/json"
        }

        try:

            respuesta = httpx.get(
                f"https://api.duffel.com/air/offers/{offer_id}",
                headers=headers,
                timeout=30
            )

            print("STATUS OFERTA:", respuesta.status_code)

            if respuesta.status_code != 200:

                print("ERROR DUFFEL:")
                print(respuesta.text)

                return None

            datos = respuesta.json()

            return datos.get("data")

        except Exception as e:

            print("ERROR CONSULTANDO OFERTA:", e)

            return None

    @staticmethod
    def crear_reserva(offer_id, pasajero):

        print(
            "FECHA DE NACIMIENTO RECIBIDA:",
            pasajero.get("fecha_nacimiento")
        )

        # Verificar nuevamente la oferta
        oferta = OfertaDuffel.obtener(offer_id)

        if not oferta:

            print("La oferta ya no está disponible.")

            return None

        precio = oferta.get("total_amount")
        moneda = oferta.get("total_currency")

        print("PRECIO ACTUAL:", precio)
        print("MONEDA:", moneda)

        passengers_oferta = oferta.get("passengers", [])

        if not passengers_oferta:

            print("La oferta no tiene pasajeros asociados.")

            return None

        passenger_id = passengers_oferta[0].get("id")

        print("PASSENGER ID DE LA OFERTA:", passenger_id)

        headers = {
            "Authorization": f"Bearer {DUFFEL_API_KEY}",
            "Duffel-Version": "v2",
            "Content-Type": "application/json"
        }

        body = {

            "data": {

                "type": "instant",

                "selected_offers": [
                    offer_id
                ],

                "passengers": [

                    {
                        "id": passenger_id,

                        "type": "adult",

                        "title": pasajero.get("titulo", "mr"),

                        "given_name": pasajero.get("nombre"),

                        "family_name": pasajero.get("apellido"),

                        "born_on": pasajero.get("fecha_nacimiento"),

                        "gender": pasajero.get("genero", "m"),

                        "email": pasajero.get("email"),

                        "phone_number": pasajero.get("telefono"),

                        "identity_documents": []
                    }

                ],

                "payments": [

                    {
                        "amount": precio,

                        "currency": moneda,

                        "type": "balance"
                    }

                ]
            }
        }

        print("BODY ENVIADO A DUFFEL:")
        print(body)

        try:

            respuesta = httpx.post(
                "https://api.duffel.com/air/orders",
                headers=headers,
                json=body,
                timeout=30
            )

            print(
                "STATUS CREAR RESERVA:",
                respuesta.status_code
            )

            print("RESPUESTA DUFFEL:")
            print(respuesta.text)

            if respuesta.status_code not in [200, 201]:

                return None

            datos = respuesta.json()

            return datos.get("data")

        except Exception as e:

            print("ERROR CREANDO RESERVA:", e)

            return None
from app.data.aeropuertos import AEROPUERTOS


def buscar_ciudades(texto: str):

    texto = texto.lower().strip()

    resultados = []

    for ciudad, codigo in AEROPUERTOS.items():

        if ciudad.startswith(texto):

            resultados.append({

                "ciudad": ciudad.title(),

                "codigo": codigo

            })

    return resultados[:8]
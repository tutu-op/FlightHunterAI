from app.data.aeropuertos import AEROPUERTOS


def obtener_codigo(texto: str) -> str:
    """
    Convierte una ciudad o un código IATA al código IATA correspondiente.
    """

    if not texto:
        return ""

    texto = texto.strip().lower()

    return AEROPUERTOS.get(texto, texto.upper())
from pydantic import BaseModel


class Vuelo(BaseModel):

    proveedor: str

    aerolinea: str

    origen: str

    destino: str

    fecha_salida: str

    fecha_regreso: str | None = None

    salida: str

    llegada: str

    precio: float

    moneda: str

    escalas: int

    duracion: str | None = None

    enlace: str | None = None

    codigo_aerolinea: str | None = None

    offer_id: str | None = None

    score: int | None = None

    razones: list[str] = []

    
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

    enlace: str | None = None
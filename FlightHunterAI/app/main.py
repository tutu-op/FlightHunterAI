from fastapi import FastAPI
from app.services.buscador import BuscadorVuelos

app = FastAPI(
    title="FlightHunter AI",
    description="Buscador inteligente de vuelos",
    version="1.0.0"
)

buscador = BuscadorVuelos()


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a FlightHunter AI",
        "estado": "Activo"
    }


@app.get("/health")
def health():
    return {
        "status": "OK"
    }


@app.get("/vuelos")
def buscar(
    origen: str,
    destino: str,
    fecha_salida: str,
    fecha_regreso: str | None = None,
    adultos: int = 1
):
    return buscador.buscar(
        origen,
        destino,
        fecha_salida,
        fecha_regreso,
        adultos
    )
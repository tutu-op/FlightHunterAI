from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, HTTPException
from fastapi import Body

from app.services.oferta import OfertaDuffel
from app.services.buscador import BuscadorVuelos
from app.services.buscador_ciudades import buscar_ciudades
from app.data.airport_service import AirportService

app = FastAPI(
    title="FlightHunter AI",
    version="2.0"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

buscador = BuscadorVuelos()

airport_service = AirportService()

@app.get("/", response_class=HTMLResponse)
def inicio(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


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
@app.get("/ciudades")
def ciudades(q: str):

    return buscar_ciudades(q)


@app.get("/aeropuertos")
def buscar_aeropuertos(buscar: str):

    resultados = airport_service.buscar(buscar)

    return resultados[:10]



@app.get("/oferta/{offer_id}")
def obtener_oferta(offer_id: str):

    oferta = OfertaDuffel.obtener(offer_id)

    if not oferta:

        return {
            "ok": False,
            "mensaje": "La oferta ya no está disponible."
        }

    return {
        "ok": True,
        "offer_id": oferta.get("id"),
        "precio": oferta.get("total_amount"),
        "moneda": oferta.get("total_currency"),
        "expira": oferta.get("expires_at")
    }

@app.post("/reserva/preparar/{offer_id}")
def preparar_reserva(offer_id: str):

    oferta = OfertaDuffel.obtener(offer_id)

    if not oferta:

        return {
            "ok": False,
            "mensaje": "La oferta ya no está disponible."
        }

    return {
        "ok": True,
        "mensaje": "Oferta lista para reservar.",
        "offer_id": oferta.get("id"),
        "precio": oferta.get("total_amount"),
        "moneda": oferta.get("total_currency"),
        "expira": oferta.get("expires_at")
    }


@app.post("/reserva/crear/{offer_id}")
def crear_reserva(
    offer_id: str,
    pasajero: dict = Body(...)
):

    reserva = OfertaDuffel.crear_reserva(
        offer_id,
        pasajero
    )

    if not reserva:

        return {
            "ok": False,
            "mensaje": "No fue posible crear la reserva."
        }

    # --- Extraer origen y destino del primer slice/segmento ---
    slices = reserva.get("slices", [])
    primer_slice = slices[0] if slices else {}
    segmentos = primer_slice.get("segments", [])
    primer_segmento = segmentos[0] if segmentos else {}

    origen = primer_segmento.get("origin", {}).get("iata_code", "?")
    destino = primer_segmento.get("destination", {}).get("iata_code", "?")

    # --- Extraer datos del pasajero ---
    pasajeros_reserva = reserva.get("passengers", [])
    primer_pasajero = pasajeros_reserva[0] if pasajeros_reserva else {}

    nombre_completo = (
        f"{primer_pasajero.get('given_name', '')} "
        f"{primer_pasajero.get('family_name', '')}"
    ).strip()

    # --- Estado del pago ---
    payment_status = reserva.get("payment_status", {})
    pagado = payment_status.get("awaiting_payment") is False

    estado_texto = "Confirmada" if pagado else "Pendiente de pago"

    return {
        "ok": True,
        "order_id": reserva.get("id"),
        "referencia": reserva.get("booking_reference"),
        "vuelo": f"{origen} → {destino}",
        "pasajero": nombre_completo,
        "precio": reserva.get("total_amount"),
        "moneda": reserva.get("total_currency"),
        "estado": estado_texto
    }
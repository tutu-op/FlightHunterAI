from app.providers.provider import Provider
from app.models.vuelo import Vuelo


class MockProvider(Provider):

    def buscar(
        self,
        origen,
        destino,
        fecha_salida,
        fecha_regreso=None,
        adultos=1
    ):

        return [

            Vuelo(
                proveedor="Mock",
                aerolinea="ANA",
                codigo_aerolinea="NH",
                origen=origen,
                destino=destino,
                fecha_salida=fecha_salida,
                fecha_regreso=fecha_regreso,
                salida="2026-10-15 08:00",
                llegada="2026-10-16 15:30",
                precio=14800,
                moneda="MXN",
                escalas=1,
                enlace=None
            ),

            Vuelo(
                proveedor="Mock",
                aerolinea="Delta",
                codigo_aerolinea="DL",
                origen=origen,
                destino=destino,
                fecha_salida=fecha_salida,
                fecha_regreso=fecha_regreso,
                salida="2026-10-15 07:20",
                llegada="2026-10-16 16:00",
                precio=15200,
                moneda="MXN",
                escalas=1,
                enlace=None
            ),

            Vuelo(
                proveedor="Mock",
                aerolinea="United",
                codigo_aerolinea="UA",
                origen=origen,
                destino=destino,
                fecha_salida=fecha_salida,
                fecha_regreso=fecha_regreso,
                salida="2026-10-15 06:00",
                llegada="2026-10-16 18:10",
                precio=15600,
                moneda="MXN",
                escalas=2,
                enlace=None
            )

        ]
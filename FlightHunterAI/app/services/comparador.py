from app.models.vuelo import Vuelo


class Comparador:

    @staticmethod
    def ordenar_por_precio(vuelos: list[Vuelo]):

        return sorted(vuelos, key=lambda x: x.precio)

    @staticmethod
    def eliminar_duplicados(vuelos: list[Vuelo]):

        resultado = []
        vistos = set()

        for vuelo in vuelos:

            llave = (
                vuelo.aerolinea,
                vuelo.salida,
                vuelo.llegada,
                vuelo.precio
            )

            if llave not in vistos:
                vistos.add(llave)
                resultado.append(vuelo)

        return resultado
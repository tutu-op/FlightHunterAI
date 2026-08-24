from app.data.loader import cargar_aeropuertos


class AirportService:

    def __init__(self):

        print("Cargando aeropuertos...")

        self.aeropuertos = cargar_aeropuertos()

        print(f"Se cargaron {len(self.aeropuertos)} aeropuertos.")

        # Índice por código IATA
        self.iata = {}

        for aeropuerto in self.aeropuertos:

            self.iata[aeropuerto["iata"]] = aeropuerto

    def buscar_por_iata(self, codigo):

        return self.iata.get(codigo.upper())

    def buscar_por_ciudad(self, ciudad):

        ciudad = ciudad.lower()

        return [

            aeropuerto

            for aeropuerto in self.aeropuertos

            if ciudad in aeropuerto["ciudad"].lower()

        ]

    def buscar_por_nombre(self, nombre):

        nombre = nombre.lower()

        return [

            aeropuerto

            for aeropuerto in self.aeropuertos

            if nombre in aeropuerto["nombre"].lower()

        ]

    def buscar(self, texto):

        texto = texto.strip()

        if len(texto) == 3:

            aeropuerto = self.buscar_por_iata(texto)

            if aeropuerto:

                return [aeropuerto]

        resultados = self.buscar_por_ciudad(texto)

        if resultados:

            return resultados

        return self.buscar_por_nombre(texto)
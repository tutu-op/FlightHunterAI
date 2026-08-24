from datetime import datetime


class Evaluador:

    @staticmethod
    def evaluar(vuelos):

        if not vuelos:
            return vuelos

        precio_minimo = min(v.precio for v in vuelos)

        for vuelo in vuelos:

            score = 100
            razones = []

            # -------------------------
            # Escalas
            # -------------------------

            if vuelo.escalas == 0:
                razones.append("✅ Vuelo directo")

            elif vuelo.escalas == 1:
                score -= 8
                razones.append("🟡 Una escala")

            else:
                score -= 20
                razones.append(f"⚠ {vuelo.escalas} escalas")

            # -------------------------
            # Precio
            # -------------------------

            diferencia = vuelo.precio - precio_minimo

            if diferencia == 0:
                razones.append("💲 Mejor precio")

            elif diferencia <= 30:
                score -= 3
                razones.append("💰 Precio muy competitivo")

            elif diferencia <= 80:
                score -= 8

            else:
                score -= 15

            # -------------------------
            # Horario de salida
            # -------------------------

            try:

                hora = datetime.fromisoformat(
                    vuelo.salida.replace("Z", "")
                ).hour

                if hora < 6:
                    score -= 10
                    razones.append("🌙 Sale de madrugada")

                elif hora <= 20:
                    razones.append("☀ Buen horario")

            except:
                pass

            if score < 0:
                score = 0

            vuelo.score = score
            vuelo.razones = razones

        vuelos.sort(key=lambda x: x.score, reverse=True)

        return vuelos
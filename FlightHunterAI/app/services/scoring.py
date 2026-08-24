class FlightHunterScore:

    @staticmethod
    def calcular(vuelo):

        score = 100
        razones = []

        # Precio
        if vuelo.precio < 250:
            score += 8
            razones.append("💰 Precio excelente")

        elif vuelo.precio < 500:
            score += 3
            razones.append("💵 Buen precio")

        else:
            score -= 8
            razones.append("💸 Precio elevado")

        # Escalas
        if vuelo.escalas == 0:
            score += 10
            razones.append("✈ Vuelo directo")

        elif vuelo.escalas == 1:
            score += 5
            razones.append("🛫 Solo una escala")

        else:
            score -= vuelo.escalas * 5
            razones.append("🔁 Muchas escalas")

        # Aerolíneas reconocidas
        premium = [
            "ANA",
            "Japan Airlines",
            "Delta Air Lines",
            "American Airlines",
            "United Airlines",
            "Air Canada",
            "Lufthansa",
            "Emirates",
            "Qatar Airways",
            "Singapore Airlines"
        ]

        if vuelo.aerolinea in premium:
            score += 8
            razones.append("⭐ Aerolínea confiable")

        score = max(0, min(score, 100))

        vuelo.score = score
        vuelo.razones = razones

        return vuelo
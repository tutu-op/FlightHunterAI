from datetime import datetime


def calcular_duracion(salida, llegada):

    try:

        salida = datetime.fromisoformat(salida)
        llegada = datetime.fromisoformat(llegada)

        diferencia = llegada - salida

        minutos = int(diferencia.total_seconds() / 60)

        horas = minutos // 60
        minutos = minutos % 60

        return f"{horas} h {minutos} min"

    except:

        return ""
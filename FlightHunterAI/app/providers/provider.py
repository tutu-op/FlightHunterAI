from abc import ABC, abstractmethod


class Provider(ABC):

    @abstractmethod
    def buscar(
        self,
        origen: str,
        destino: str,
        fecha_salida: str,
        fecha_regreso: str | None = None,
        adultos: int = 1
    ):
        pass
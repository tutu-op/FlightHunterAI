
from app.providers.duffel import DuffelProvider


class ProviderManager:

    def __init__(self):

        self.providers = [

            DuffelProvider()
        ]

    def obtener_providers(self):

        return self.providers
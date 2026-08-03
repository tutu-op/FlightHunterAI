from app.providers.mock import MockProvider
from app.providers.duffel import DuffelProvider


class ProviderManager:

    def __init__(self):

        self.providers = [

            MockProvider(),

            DuffelProvider()

        ]

    def obtener_providers(self):

        return self.providers
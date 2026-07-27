from app.providers.mock import MockProvider


class ProviderManager:

    def __init__(self):

        self.providers = [

            MockProvider()

        ]

    def obtener_providers(self):

        return self.providers
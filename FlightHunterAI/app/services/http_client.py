import httpx


class HTTPClient:

    def __init__(self):

        self.client = httpx.Client(timeout=20)

    def get(self, url, headers=None, params=None):

        return self.client.get(
            url,
            headers=headers,
            params=params
        )

    def post(self, url, headers=None, json=None):

        return self.client.post(
            url,
            headers=headers,
            json=json
        )
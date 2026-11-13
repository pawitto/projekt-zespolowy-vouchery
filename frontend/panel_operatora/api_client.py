# Komunikacja HTTP z istniejacym backendem FastAPI.
# Obecny backend nie udostepnia jeszcze centralnych endpointow operatora.
import os

import requests


class KlientApi:
    def __init__(self, adresBazowy: str | None = None):
        self.adresBazowy = (adresBazowy or os.getenv("VOUCHERHUB_API_URL", "http://127.0.0.1:8000")).rstrip("/")
        self.sesja = requests.Session()
        self.sesja.headers.update({"Accept": "application/json"})

    def pobierzOfertyPubliczne(self) -> list[dict]:
        odpowiedz = self.sesja.get(f"{self.adresBazowy}/api/v1/offers", timeout=10)
        odpowiedz.raise_for_status()
        return odpowiedz.json()

    def pobierzSzczegolyOferty(self, identyfikator: int) -> dict:
        odpowiedz = self.sesja.get(f"{self.adresBazowy}/api/v1/offers/{identyfikator}", timeout=10)
        odpowiedz.raise_for_status()
        return odpowiedz.json()

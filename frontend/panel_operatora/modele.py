# Modele danych prototypu VoucherHub.
# Wymagania: Python 3.11+.
from dataclasses import dataclass
from datetime import date


@dataclass
class Oferta:
    identyfikator: int
    partner: str
    nazwa: str
    cena: int
    limitUzyc: int
    aktywna: bool = True
    pakiet: bool = False


@dataclass
class Voucher:
    kod: str
    transakcjaId: int
    partner: str
    oferta: str
    limitUzyc: int
    liczbaUzyc: int
    dataWaznosci: date
    status: str = "ACTIVE"

    @property
    def pozostalo(self) -> int:
        return max(0, self.limitUzyc - self.liczbaUzyc)

    @property
    def statusWidoczny(self) -> str:
        if self.status == "CANCELLED":
            return "CANCELLED"
        if self.status == "USED" or self.pozostalo == 0:
            return "USED"
        if self.dataWaznosci < date.today():
            return "EXPIRED"
        return "ACTIVE"


@dataclass
class Transakcja:
    identyfikator: int
    nazwa: str
    kanal: str
    kwota: int
    zwrocona: bool = False


@dataclass
class Rezerwacja:
    identyfikator: str
    partner: str
    nazwa: str
    termin: str
    status: str

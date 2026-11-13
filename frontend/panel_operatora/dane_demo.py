# Zrodlo danych testowych oraz przykladowe operacje na voucherach.
# Wszystkie zmiany sa lokalne. Nie zapisuje sie ich w PostgreSQL.
from datetime import date, timedelta

from modele import Oferta, Rezerwacja, Transakcja, Voucher


class DaneDemo:
    def __init__(self):
        dzisiaj = date.today()
        self.oferty = [
            Oferta(1, "A – Masaże", "Masaż relaksacyjny", 180, 1),
            Oferta(2, "B – Fitness", "Karnet 10 wejść", 220, 10),
            Oferta(3, "C – Hotel", "Nocleg weekendowy", 540, 1),
            Oferta(4, "A / B / C", "Pakiet pobyt + masaż + trening", 800, 1, pakiet=True),
        ]
        self.transakcje = [
            Transakcja(1001, "Masaż relaksacyjny", "WWW", 180),
            Transakcja(1002, "Karnet 10 wejść", "Stacjonarnie", 220),
            Transakcja(1003, "Pakiet pobyt + masaż + trening", "WWW", 800),
            Transakcja(1004, "Masaż demonstracyjny – anulowany", "Stacjonarnie", 180),
        ]
        self.vouchery = [
            Voucher("VH-A111-0001", 1001, "A – Masaże", "Masaż relaksacyjny", 1, 0, dzisiaj + timedelta(days=90)),
            Voucher("VH-B222-0002", 1002, "B – Fitness", "Karnet 10 wejść", 10, 3, dzisiaj + timedelta(days=120)),
            Voucher("VH-C333-0003", 1003, "C – Hotel", "Nocleg weekendowy", 1, 0, dzisiaj + timedelta(days=180)),
            Voucher("VH-A444-0004", 1003, "A – Masaże", "Masaż relaksacyjny", 1, 0, dzisiaj + timedelta(days=180)),
            Voucher("VH-B555-0005", 1003, "B – Fitness", "Trening personalny", 1, 0, dzisiaj + timedelta(days=180)),
            Voucher("VH-A666-0006", 1004, "A – Masaże", "Kod demonstracyjny anulowany", 1, 0, dzisiaj + timedelta(days=30), "CANCELLED"),
        ]
        self.rezerwacje = [
            Rezerwacja("RES-C-031", "C – Hotel", "Weekendowy pobyt", "2026-12-12", "Potwierdzona"),
            Rezerwacja("RES-A-041", "A – Masaże", "Masaż relaksacyjny", "2026-12-13", "Oczekuje"),
        ]
        self.historia = [
            ("VH-B222-0002", "B – Fitness", "3 realizacje (dane demonstracyjne)"),
        ]

    def pobierzVoucher(self, kod: str) -> Voucher:
        for voucher in self.vouchery:
            if voucher.kod == kod:
                return voucher
        raise ValueError("Nie znaleziono vouchera.")

    def pobierzTransakcje(self, identyfikator: int) -> Transakcja:
        for transakcja in self.transakcje:
            if transakcja.identyfikator == identyfikator:
                return transakcja
        raise ValueError("Nie znaleziono transakcji.")

    def zrealizujVoucher(self, kod: str) -> None:
        voucher = self.pobierzVoucher(kod)
        if voucher.statusWidoczny != "ACTIVE":
            raise ValueError("Voucher nie jest aktywny.")
        voucher.liczbaUzyc += 1
        if voucher.pozostalo == 0:
            voucher.status = "USED"
        self.historia.append((kod, voucher.partner, "Realizacja demonstracyjna"))

    def anulujVoucher(self, kod: str) -> None:
        voucher = self.pobierzVoucher(kod)
        if sum(v.transakcjaId == voucher.transakcjaId for v in self.vouchery) > 1:
            raise ValueError("Anulowanie pojedynczego vouchera z pakietu wymaga uzgodnienia.")
        if voucher.statusWidoczny != "ACTIVE":
            raise ValueError("Anulować można tylko aktywny voucher.")
        voucher.status = "CANCELLED"

    def zwrocTransakcje(self, identyfikator: int) -> None:
        transakcja = self.pobierzTransakcje(identyfikator)
        powiazane = [v for v in self.vouchery if v.transakcjaId == identyfikator]
        if transakcja.zwrocona or not powiazane:
            raise ValueError("Zwrot tej transakcji nie jest możliwy.")
        if any(v.liczbaUzyc > 0 or v.statusWidoczny == "USED" for v in powiazane):
            raise ValueError("Zwrot jest niemożliwy po wykorzystaniu części zakupu.")
        if any(v.statusWidoczny == "CANCELLED" for v in powiazane):
            raise ValueError("Transakcja zawiera anulowany kod; zasady wymagają uzgodnienia.")
        for voucher in powiazane:
            voucher.status = "CANCELLED"
        transakcja.zwrocona = True

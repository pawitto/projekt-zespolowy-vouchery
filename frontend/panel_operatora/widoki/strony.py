# Widoki operatora. Logika danych pozostaje w klasie DaneDemo.
from PySide6.QtWidgets import (
    QComboBox, QHBoxLayout, QLabel, QMessageBox, QPushButton,
    QTableWidget, QVBoxLayout, QWidget,
)

from dane_demo import DaneDemo
from widoki.elementy import utworzStrone, utworzTabele, wypelnijTabele


class StronaStartowa(QWidget):
    def __init__(self, dane: DaneDemo):
        super().__init__()
        self.dane = dane
        uklad = QVBoxLayout(self)
        naglowek = QLabel("Panel główny")
        naglowek.setObjectName("naglowekStrony")
        self.podsumowanie = QLabel()
        uklad.addWidget(naglowek)
        uklad.addWidget(self.podsumowanie)
        uklad.addStretch()
        self.odswiez()

    def odswiez(self):
        aktywne = sum(v.statusWidoczny == "ACTIVE" for v in self.dane.vouchery)
        self.podsumowanie.setText(
            f"Oferty: {len(self.dane.oferty)}     "
            f"Vouchery: {len(self.dane.vouchery)}     "
            f"Aktywne kody: {aktywne}\n\n"
            "Wersja demonstracyjna. Dane znajdują się wyłącznie w pamięci aplikacji."
        )


class StronaOfert(QWidget):
    def __init__(self, dane: DaneDemo):
        super().__init__()
        self.dane = dane
        uklad = utworzStrone("Oferty voucherowe")
        self.filtr = QComboBox()
        self.filtr.addItems(["Wszyscy partnerzy", "A – Masaże", "B – Fitness", "C – Hotel", "A / B / C"])
        self.filtr.currentIndexChanged.connect(self.odswiez)
        self.tabela = utworzTabele(["Partner", "Oferta", "Cena", "Limit", "Status"])
        uklad.addWidget(self.filtr)
        uklad.addWidget(self.tabela)
        self.setLayout(uklad)
        self.odswiez()

    def odswiez(self):
        partner = self.filtr.currentText()
        wiersze = [
            [o.partner, o.nazwa, f"{o.cena} zł", str(o.limitUzyc), "Aktywna" if o.aktywna else "Wyłączona"]
            for o in self.dane.oferty
            if partner == "Wszyscy partnerzy" or o.partner == partner
        ]
        wypelnijTabele(self.tabela, wiersze)


class StronaVoucherow(QWidget):
    def __init__(self, dane: DaneDemo, poZmianie):
        super().__init__()
        self.dane = dane
        self.poZmianie = poZmianie
        uklad = utworzStrone("Vouchery")
        filtry = QHBoxLayout()
        self.filtr = QComboBox()
        self.filtr.addItems(["Wszystkie", "ACTIVE", "USED", "EXPIRED", "CANCELLED"])
        self.filtr.currentIndexChanged.connect(self.odswiez)
        filtry.addWidget(QLabel("Status:"))
        filtry.addWidget(self.filtr)
        uklad.addLayout(filtry)
        self.tabela = utworzTabele(["Kod", "Partner", "Oferta", "Pozostało", "Ważność", "Status"])
        uklad.addWidget(self.tabela)
        self.szczegoly = QLabel("Zaznacz voucher, aby zobaczyć jego historię użyć.")
        self.tabela.itemSelectionChanged.connect(self.pokazHistorie)
        uklad.addWidget(self.szczegoly)
        przyciski = QHBoxLayout()
        realizuj = QPushButton("Zrealizuj (demo)")
        anuluj = QPushButton("Anuluj (demo)")
        realizuj.clicked.connect(self.zrealizuj)
        anuluj.clicked.connect(self.anuluj)
        przyciski.addWidget(realizuj)
        przyciski.addWidget(anuluj)
        uklad.addLayout(przyciski)
        self.setLayout(uklad)
        self.widoczneKody = []
        self.odswiez()

    def odswiez(self):
        stan = self.filtr.currentText()
        vouchery = [v for v in self.dane.vouchery if stan == "Wszystkie" or v.statusWidoczny == stan]
        self.widoczneKody = [v.kod for v in vouchery]
        wiersze = [[v.kod, v.partner, v.oferta, f"{v.pozostalo}/{v.limitUzyc}", str(v.dataWaznosci), v.statusWidoczny] for v in vouchery]
        wypelnijTabele(self.tabela, wiersze)

    def pokazHistorie(self):
        wiersz = self.tabela.currentRow()
        if 0 <= wiersz < len(self.widoczneKody):
            kod = self.widoczneKody[wiersz]
            wpisy = [w[2] for w in self.dane.historia if w[0] == kod]
            self.szczegoly.setText("Historia: " + ("; ".join(wpisy) if wpisy else "brak realizacji"))
        else:
            self.szczegoly.setText("Zaznacz voucher, aby zobaczyć jego historię użyć.")

    def wybranyKod(self) -> str | None:
        wiersz = self.tabela.currentRow()
        if wiersz < 0 or wiersz >= len(self.widoczneKody):
            QMessageBox.information(self, "Wybór vouchera", "Należy zaznaczyć voucher w tabeli.")
            return None
        return self.widoczneKody[wiersz]

    def zrealizuj(self):
        kod = self.wybranyKod()
        if kod is None:
            return
        try:
            self.dane.zrealizujVoucher(kod)
        except ValueError as blad:
            QMessageBox.warning(self, "Realizacja", str(blad))
            return
        self.poZmianie()

    def anuluj(self):
        kod = self.wybranyKod()
        if kod is None:
            return
        odpowiedz = QMessageBox.question(self, "Anulowanie demonstracyjne", f"Anulować kod {kod} w danych testowych?")
        if odpowiedz != QMessageBox.StandardButton.Yes:
            return
        try:
            self.dane.anulujVoucher(kod)
        except ValueError as blad:
            QMessageBox.warning(self, "Anulowanie", str(blad))
            return
        self.poZmianie()


class StronaTransakcji(QWidget):
    def __init__(self, dane: DaneDemo, poZmianie):
        super().__init__()
        self.dane = dane
        self.poZmianie = poZmianie
        uklad = utworzStrone("Transakcje i pełne zwroty")
        self.tabela = utworzTabele(["Numer", "Zakup", "Kanał", "Kwota", "Stan zwrotu"])
        uklad.addWidget(self.tabela)
        zwroc = QPushButton("Pełny zwrot (demo)")
        zwroc.clicked.connect(self.zwroc)
        uklad.addWidget(zwroc)
        self.setLayout(uklad)
        self.odswiez()

    def odswiez(self):
        wypelnijTabele(self.tabela, [
            [str(t.identyfikator), t.nazwa, t.kanal, f"{t.kwota} zł", "Zwrócona" if t.zwrocona else "Brak zwrotu"]
            for t in self.dane.transakcje
        ])

    def zwroc(self):
        wiersz = self.tabela.currentRow()
        if wiersz < 0:
            QMessageBox.information(self, "Wybór transakcji", "Należy zaznaczyć transakcję.")
            return
        numer = self.dane.transakcje[wiersz].identyfikator
        odpowiedz = QMessageBox.question(self, "Pełny zwrot demonstracyjny", f"Zwrócić całą transakcję {numer}?")
        if odpowiedz != QMessageBox.StandardButton.Yes:
            return
        try:
            self.dane.zwrocTransakcje(numer)
        except ValueError as blad:
            QMessageBox.warning(self, "Zwrot", str(blad))
            return
        self.poZmianie()


class StronaRezerwacji(QWidget):
    def __init__(self, dane: DaneDemo):
        super().__init__()
        self.dane = dane
        uklad = utworzStrone("Rezerwacje partnerów – podgląd")
        self.tabela = utworzTabele(["Identyfikator", "Partner", "Usługa", "Termin", "Status"])
        uklad.addWidget(self.tabela)
        self.setLayout(uklad)
        self.odswiez()

    def odswiez(self):
        wypelnijTabele(self.tabela, [[r.identyfikator, r.partner, r.nazwa, r.termin, r.status] for r in self.dane.rezerwacje])


class StronaRozliczen(QWidget):
    def __init__(self, dane: DaneDemo):
        super().__init__()
        self.dane = dane
        uklad = utworzStrone("Rozliczenia – widok demonstracyjny")
        self.tabela = utworzTabele(["Partner", "Zrealizowane wejścia"])
        uklad.addWidget(QLabel("Kwoty do rozliczenia wymagają uzgodnienia zasad podziału ceny pakietów."))
        uklad.addWidget(self.tabela)
        self.setLayout(uklad)
        self.odswiez()

    def odswiez(self):
        partnerzy = ["A – Masaże", "B – Fitness", "C – Hotel"]
        wypelnijTabele(self.tabela, [[p, str(sum(v.liczbaUzyc for v in self.dane.vouchery if v.partner == p))] for p in partnerzy])

# Okno glowne prototypu operatora VoucherHub.
from pathlib import Path

from PySide6.QtWidgets import (
    QHBoxLayout, QLabel, QListWidget, QMainWindow, QStackedWidget,
    QVBoxLayout, QWidget,
)

from dane_demo import DaneDemo
from widoki.strony import (
    StronaOfert, StronaRezerwacji, StronaRozliczen,
    StronaStartowa, StronaTransakcji, StronaVoucherow,
)


class OknoGlowne(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VoucherHub – panel operatora (demo)")
        self.resize(1100, 730)
        self.dane = DaneDemo()
        self.nawigacja = QListWidget()
        self.nawigacja.addItems(["Panel główny", "Oferty", "Vouchery", "Transakcje", "Rezerwacje", "Rozliczenia"])
        self.nawigacja.setFixedWidth(215)
        self.nawigacja.setObjectName("nawigacja")
        self.widoki = QStackedWidget()
        self.strony = [
            StronaStartowa(self.dane),
            StronaOfert(self.dane),
            StronaVoucherow(self.dane, self.odswiezWidoki),
            StronaTransakcji(self.dane, self.odswiezWidoki),
            StronaRezerwacji(self.dane),
            StronaRozliczen(self.dane),
        ]
        for strona in self.strony:
            self.widoki.addWidget(strona)

        panel = QWidget()
        uklad = QHBoxLayout(panel)
        uklad.setContentsMargins(0, 0, 0, 0)
        uklad.setSpacing(0)
        menu = QWidget()
        menu.setObjectName("menu")
        ukladMenu = QVBoxLayout(menu)
        logo = QLabel("VoucherHub")
        logo.setObjectName("logo")
        ukladMenu.addWidget(logo)
        ukladMenu.addWidget(self.nawigacja)
        informacja = QLabel("Operator – dane demonstracyjne")
        informacja.setObjectName("informacjaMenu")
        ukladMenu.addWidget(informacja)
        uklad.addWidget(menu)
        uklad.addWidget(self.widoki, 1)
        self.setCentralWidget(panel)
        self.nawigacja.currentRowChanged.connect(self.pokazStrone)
        self.nawigacja.setCurrentRow(0)
        styl = Path(__file__).with_name("styl.qss").read_text(encoding="utf-8")
        self.setStyleSheet(styl)

    def pokazStrone(self, numer: int):
        if numer >= 0:
            self.widoki.setCurrentIndex(numer)
            self.strony[numer].odswiez()

    def odswiezWidoki(self):
        for strona in self.strony:
            strona.odswiez()

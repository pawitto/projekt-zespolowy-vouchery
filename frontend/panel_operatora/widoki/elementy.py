# Wspolne elementy interfejsu operatora.
from PySide6.QtWidgets import QHeaderView, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout


def utworzTabele(naglowki: list[str]) -> QTableWidget:
    tabela = QTableWidget(0, len(naglowki))
    tabela.setHorizontalHeaderLabels(naglowki)
    tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    tabela.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    tabela.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
    tabela.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    tabela.verticalHeader().setVisible(False)
    tabela.setAlternatingRowColors(True)
    return tabela


def wypelnijTabele(tabela: QTableWidget, wiersze: list[list[str]]) -> None:
    tabela.setRowCount(len(wiersze))
    for numerWiersza, wiersz in enumerate(wiersze):
        for numerKolumny, wartosc in enumerate(wiersz):
            tabela.setItem(numerWiersza, numerKolumny, QTableWidgetItem(str(wartosc)))


def utworzStrone(tytul: str) -> QVBoxLayout:
    uklad = QVBoxLayout()
    uklad.setContentsMargins(20, 20, 20, 20)
    uklad.setSpacing(12)
    naglowek = QLabel(tytul)
    naglowek.setObjectName("naglowekStrony")
    uklad.addWidget(naglowek)
    return uklad

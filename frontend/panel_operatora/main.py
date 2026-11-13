# Uruchomienie panelu operatora VoucherHub.
# Wymagania: Python 3.11+, PySide6.
import sys

from PySide6.QtWidgets import QApplication

from okno_glowne import OknoGlowne


def main():
    aplikacja = QApplication(sys.argv)
    okno = OknoGlowne()
    okno.show()
    return aplikacja.exec()


if __name__ == "__main__":
    sys.exit(main())

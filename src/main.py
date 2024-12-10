import sys
from PyQt5.QtWidgets import QApplication
from ui import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Tworzenie głównego okna aplikacji
    window = MainWindow()
    window.show()

    # Uruchomienie pętli aplikacji
    sys.exit(app.exec_())

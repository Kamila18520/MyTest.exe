import sys
import socket
import platform
import psutil
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtGui import QIcon


# Funkcje pomocnicze

# Funkcja do pobierania informacji o adresie IPv4
def get_ipv4_info():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return f"Adres IPv4: {ip_address}\n"
    except Exception as e:
        return f"Błąd przy sprawdzaniu IPv4: {e}"

# Funkcja do pobierania informacji o proxy
def get_proxy_info():
    proxy = os.environ.get('http_proxy', 'Brak proxy')
    return f"Proxy: {proxy}"

# Funkcja do pobierania informacji o systemie
def get_system_info():
    system = platform.system()
    version = platform.version()
    processor = platform.processor()
    cores = psutil.cpu_count(logical=True)
    memory = psutil.virtual_memory().total // (1024 ** 2)  # Pamięć w MB
    return (f"System: {system}\n"
            f"Wersja: {version}\n"
            f"Procesor: {processor}\n"
            f"Rdzenie CPU: {cores}\n"
            f"Pamięć RAM: {memory} MB")


# Funkcja do pobierania nazwy hosta
def get_hostname():
    try:
        return f"Nazwa hosta: {socket.gethostname()}"
    except Exception as e:
        return f"Błąd przy sprawdzaniu nazwy hosta: {e}"


def get_bios_version():
    try:
        if platform.system() == "Windows":
            # Uruchamiamy komendę WMIC i odczytujemy wynik
            output = os.popen("wmic bios get smbiosbiosversion").read()
            # Usuwamy puste linie i dodatkowe białe znaki
            bios_version = [line.strip() for line in output.splitlines() if line.strip()]

            if len(bios_version) > 1:
                # Zwracamy wersję BIOSu, zwracamy tylko drugą linię, bo pierwsza to nagłówek
                return f"Wersja BIOS: {bios_version[1]}"
            else:
                return "Nie udało się odczytać wersji BIOSu"
        else:
            return "Funkcja niedostępna na tym systemie"
    except Exception as e:
        return f"Błąd przy sprawdzaniu wersji BIOS: {e}"


# Główne okno aplikacji
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyTestApp")  # Tytuł okna
        self.setGeometry(130, 130, 500, 300)  # Rozmiar i pozycja okna
        self.setFixedSize(500, 300)  # Ustawienie stałej wielkości okna

        self.setWindowIcon(QIcon("resources/icons/icon.png"))  # Ustawienie ikony okna

        # Główne okno aplikacji
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout i elementy UI
        layout = QVBoxLayout()
        self.text_view = QTextEdit()
        self.text_view.setReadOnly(True)  # Ustawienie pola tekstowego na tylko do odczytu
        layout.addWidget(self.text_view)

        # Przyciski
        self.btn_ipv4 = QPushButton("Sprawdź IPv4")
        self.btn_proxy = QPushButton("Sprawdź Proxy")
        self.btn_sysinfo = QPushButton("Informacje o systemie")
        self.btn_bios = QPushButton("Wersja BIOS")
        self.btn_hostname = QPushButton("Hostname")

        # Dodanie przycisków do layoutu
        layout.addWidget(self.btn_ipv4)
        layout.addWidget(self.btn_proxy)
        layout.addWidget(self.btn_sysinfo)
        layout.addWidget(self.btn_bios)
        layout.addWidget(self.btn_hostname)

        # Podpięcie sygnałów do funkcji
        self.btn_ipv4.clicked.connect(self.show_ipv4)
        self.btn_proxy.clicked.connect(self.show_proxy)
        self.btn_sysinfo.clicked.connect(self.show_sysinfo)
        self.btn_bios.clicked.connect(self.show_bios)
        self.btn_hostname.clicked.connect(self.show_hostname)

        self.central_widget.setLayout(layout)

    # Funkcje odpowiadające na przyciski
    def show_ipv4(self):
        result = get_ipv4_info()
        self.text_view.setText(result)

    def show_proxy(self):
        result = get_proxy_info()
        self.text_view.setText(result)

    def show_sysinfo(self):
        result = get_system_info()
        self.text_view.setText(result)

    def show_bios(self):
        result = get_bios_version()
        self.text_view.setText(result)

    def show_hostname(self):
        result = get_hostname()
        self.text_view.setText(result)


# Uruchomienie aplikacji
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Tworzenie głównego okna aplikacji
    window = MainWindow()
    window.show()

    # Uruchomienie głównej pętli aplikacji
    sys.exit(app.exec_())

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton

import helpers


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyTestApp")
        self.setGeometry(100, 100, 600, 400)

        self.setWindowIcon(QIcon("resources/icons/icon.png"))

        # Główne okno aplikacji
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout i elementy UI
        layout = QVBoxLayout()
        self.text_view = QTextEdit()
        self.text_view.setReadOnly(True)
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
        result = helpers.get_ipv4_info()
        self.text_view.setText(result)

    def show_proxy(self):
        result = helpers.get_proxy_info()
        self.text_view.setText(result)

    def show_sysinfo(self):
        result = helpers.get_system_info()
        self.text_view.setText(result)

    def show_bios(self):
        result = helpers.get_bios_version()
        self.text_view.setText(result)

    def show_hostname(self):
        result = helpers.get_hostname()
        self.text_view.setText(result)

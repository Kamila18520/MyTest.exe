import socket
import platform
import psutil
import os

def get_ipv4_info():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return f"Adres IPv4: {ip_address}\n"
    except Exception as e:
        return f"Błąd przy sprawdzaniu IPv4: {e}"

def get_proxy_info():
    proxy = os.environ.get('http_proxy', 'Brak proxy')
    return f"Proxy: {proxy}"

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

def get_bios_version():
    try:
        if platform.system() == "Windows":
            output = os.popen("wmic bios get smbiosbiosversion").read()
            return f"Wersja BIOS: {output.splitlines()[1]}"
        else:
            return "Funkcja niedostępna na tym systemie"
    except Exception as e:
        return f"Błąd przy sprawdzaniu wersji BIOS: {e}"

def get_hostname():
    try:
        return f"Nazwa hosta: {socket.gethostname()}"
    except Exception as e:
        return f"Błąd przy sprawdzaniu nazwy hosta: {e}"

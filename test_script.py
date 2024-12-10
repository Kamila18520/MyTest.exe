import unittest
import socket
import platform
import os
import psutil
from io import StringIO
from unittest.mock import patch
from main import get_ipv4_info, get_proxy_info, get_system_info, get_hostname, get_bios_version


class TestSystemInfo(unittest.TestCase):

    # Test dla funkcji get_ipv4_info
    @patch('socket.gethostbyname')
    @patch('socket.gethostname')
    def test_get_ipv4_info(self, mock_gethostname, mock_gethostbyname):
        mock_gethostname.return_value = 'localhost'
        mock_gethostbyname.return_value = '192.168.1.1'
        result = get_ipv4_info()
        self.assertIn("Adres IPv4: 192.168.1.1", result)

    # Test dla funkcji get_proxy_info
    @patch('os.environ.get')
    def test_get_proxy_info(self, mock_get):
        mock_get.return_value = 'http://proxy.example.com'
        result = get_proxy_info()
        self.assertIn("Proxy: http://proxy.example.com", result)

    # Test dla funkcji get_system_info
    @patch('platform.system')
    @patch('platform.version')
    @patch('platform.processor')
    @patch('psutil.cpu_count')
    @patch('psutil.virtual_memory')
    def test_get_system_info(self, mock_virtual_memory, mock_cpu_count, mock_processor, mock_version, mock_system):
        mock_system.return_value = 'Windows'
        mock_version.return_value = '10.0'
        mock_processor.return_value = 'Intel'
        mock_cpu_count.return_value = 4
        mock_virtual_memory.return_value.total = 8 * 1024 * 1024 * 1024  # 8 GB RAM

        result = get_system_info()
        self.assertIn("System: Windows", result)
        self.assertIn("Wersja: 10.0", result)
        self.assertIn("Procesor: Intel", result)
        self.assertIn("Rdzenie CPU: 4", result)
        self.assertIn("Pamięć RAM: 8192 MB", result)

    # Test dla funkcji get_hostname
    @patch('socket.gethostname')
    def test_get_hostname(self, mock_gethostname):
        mock_gethostname.return_value = 'test-host'
        result = get_hostname()
        self.assertIn("Nazwa hosta: test-host", result)

    # Test dla funkcji get_bios_version
    @patch('os.popen')
    def test_get_bios_version(self, mock_popen):
        # Jeśli jesteśmy na systemie Windows, sprawdzamy wynik
        if platform.system() == "Windows":
            mock_popen.return_value.read.return_value = 'SMBIOSBIOSVersion 2.0\n'
            result = get_bios_version()
            self.assertIn("Wersja BIOS: 2.0", result)
        else:
            # Dla innych systemów, oczekujemy komunikatu o braku wsparcia
            result = get_bios_version()
            self.assertIn("Funkcja niedostępna na tym systemie", result)

    # Test dla funkcji get_bios_version na systemie innym niż Windows
    @patch('platform.system')
    def test_get_bios_version_non_windows(self, mock_system):
        mock_system.return_value = 'Linux'
        result = get_bios_version()
        self.assertIn("Funkcja niedostępna na tym systemie", result)


if __name__ == '__main__':
    unittest.main()

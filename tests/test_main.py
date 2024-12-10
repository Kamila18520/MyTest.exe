import unittest
from unittest.mock import patch
import socket
import platform
import psutil
import os
from main import get_ipv4_info, get_proxy_info, get_system_info, get_bios_version, get_hostname


class TestHelpers(unittest.TestCase):

    # Test funkcji get_ipv4_info()
    @patch('socket.gethostname', return_value="mocked_hostname")
    @patch('socket.gethostbyname', return_value="192.168.1.1")
    def test_get_ipv4_info(self, mock_gethostbyname, mock_gethostname):
        result = get_ipv4_info()
        self.assertEqual(result, "Adres IPv4: 192.168.1.1\n")

    @patch('socket.gethostname', return_value="mocked_hostname")
    @patch('socket.gethostbyname', side_effect=Exception("Some error"))
    def test_get_ipv4_info_error(self, mock_gethostbyname, mock_gethostname):
        result = get_ipv4_info()
        self.assertTrue(result.startswith("Błąd przy sprawdzaniu IPv4"))

    # Test funkcji get_proxy_info()
    @patch('os.environ.get', return_value="http://proxy.example.com")
    def test_get_proxy_info(self, mock_getenv):
        result = get_proxy_info()
        self.assertEqual(result, "Proxy: http://proxy.example.com")

    @patch('os.environ.get', return_value=None)
    def test_get_proxy_info_no_proxy(self, mock_getenv):
        result = get_proxy_info()
        self.assertEqual(result, "Proxy: Brak proxy")

    # Test funkcji get_system_info()
    @patch('platform.system', return_value="Windows")
    @patch('platform.version', return_value="10.0.19043")
    @patch('platform.processor', return_value="Intel")
    @patch('psutil.cpu_count', return_value=8)
    @patch('psutil.virtual_memory', return_value=psutil._psvm.svmem(total=16*1024**3))
    def test_get_system_info(self, mock_virtual_memory, mock_cpu_count, mock_processor, mock_version, mock_system):
        result = get_system_info()
        self.assertIn("System: Windows", result)
        self.assertIn("Wersja: 10.0.19043", result)
        self.assertIn("Procesor: Intel", result)
        self.assertIn("Rdzenie CPU: 8", result)
        self.assertIn("Pamięć RAM: 16384 MB", result)

    # Test funkcji get_hostname()
    @patch('socket.gethostname', return_value="mocked_hostname")
    def test_get_hostname(self, mock_gethostname):
        result = get_hostname()
        self.assertEqual(result, "Nazwa hosta: mocked_hostname")

    @patch('socket.gethostname', side_effect=Exception("Some error"))
    def test_get_hostname_error(self, mock_gethostname):
        result = get_hostname()
        self.assertTrue(result.startswith("Błąd przy sprawdzaniu nazwy hosta"))

    # Test funkcji get_bios_version()
    @patch('platform.system', return_value="Windows")
    @patch('os.popen', return_value="SMBIOSBIOSVersion 1.2.3")
    def test_get_bios_version(self, mock_popen, mock_system):
        result = get_bios_version()
        self.assertEqual(result, "Wersja BIOS: 1.2.3")

    @patch('platform.system', return_value="Linux")
    def test_get_bios_version_linux(self, mock_system):
        result = get_bios_version()
        self.assertEqual(result, "Funkcja niedostępna na tym systemie")

    @patch('platform.system', return_value="Windows")
    @patch('os.popen', side_effect=Exception("WMIC command failed"))
    def test_get_bios_version_error(self, mock_popen, mock_system):
        result = get_bios_version()
        self.assertTrue(result.startswith("Błąd przy sprawdzaniu wersji BIOS"))


if __name__ == "__main__":
    unittest.main()

import unittest
from src.main import validate_package_name, validate_output_file, validate_test_mode

class TestConfigValidation(unittest.TestCase):

    def test_valid_package_name(self):
        validate_package_name("curl")

    def test_empty_package_name(self):
        with self.assertRaises(ValueError):
            validate_package_name("")

    def test_valid_output_file(self):
        validate_output_file("graph.png")

    def test_invalid_output_extension(self):
        with self.assertRaises(ValueError):
            validate_output_file("graph.txt")

    def test_valid_test_mode(self):
        validate_test_mode(True)
        validate_test_mode(False)

    def test_invalid_test_mode_type(self):
        with self.assertRaises(ValueError):
            validate_test_mode("yes")
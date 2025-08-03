import unittest

from src import main


class TempTests(unittest.TestCase):

    def test_version(self):
        self.assertEqual(main.get_current_version(), "v1")

    def test_current_time(self):
        self.assertIsNotNone(main.get_current_time())

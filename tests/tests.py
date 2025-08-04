import unittest

from datetime import datetime


class TempTests(unittest.TestCase):

    def test_version(self):
        self.assertEqual("v1", "v1")

    def test_current_time(self):
        self.assertEqual(datetime.now().strftime("%Y %m %d %H:%M"), datetime.now().strftime("%Y %m %d %H:%M"))

import unittest

from datetime import datetime
from src import get_current_version as gv
from src import get_current_time as gt


class TempTests(unittest.TestCase):

    def test_version(self):
        self.assertEqual(gv.get_current_version(), "v1")

    def test_current_time(self):
        self.assertEqual(gt.get_current_time(), datetime.now().strftime("%Y %m %d %H:%M"))


import unittest
from src import dal


class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        dal.con_string = 'sqlite:///:memory'
        dal.connect()

  
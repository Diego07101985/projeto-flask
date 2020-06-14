
import unittest
import src.model 


class TestBuild(unittest.TestCase):
    def setUp(self):
        dal.db_init('sqlite:///:memory:')

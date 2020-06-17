
try:
    import sys
    import os

    sys.path.append(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '../../desafio'
            )
        )
    )
except:
    raise


# from src import dal

from desafio import dal
from src.repositorys import RepositoryUsers
from src.models import User
from sqlalchemy.exc import IntegrityError
import unittest
from unittest.mock import patch
from desafio import session_scope
# from test_build import TestApp


class TestRepositoryUser(unittest.TestCase):

    def setUp(self):
        self.dal = dal
        self.dal.conn_string = 'sqlite:///:memory'
        self.dal.connect()
        self.users = RepositoryUsers()
        self.user = User(username="lans", email="j@j")

    @patch('desafio.session_scope')
    def test_1_deve_retornar_id_usuario_depois_add(self, mock_tmp):
        id_user = self.users.insert(self.user)
        self.assertIsInstance(id_user, int)
        self.assertEqual(id_user, 1)

    @patch('desafio.session_scope')
    def test_2_deve_retornar_integrity_error(self, mock_tmp):
        with self.assertRaises(IntegrityError):
            self.users.insert(self.user)

    @patch('desafio.session_scope')
    def test_3_obtem_um_usuario(self, mock_tmp):
        self.assertTrue(self.users.get_user(self.user) == self.user)

    @patch('desafio.session_scope')
    def test_4_deve_alterar_o_email_do_usuario(self, mock_tmp):
        self.user.email = "di@bob"
        update_usuario = self.users.update(self.user)
        self.assertEqual(update_usuario.email, self.user.email)

    @patch('desafio.session_scope')
    def test_5_deve_deletar_um_usuario(self, mock_tmp):
        self.assertIsNone(self.users.delete(self.user))


if __name__ == '__main__':
    unittest.main(verbosity=2)

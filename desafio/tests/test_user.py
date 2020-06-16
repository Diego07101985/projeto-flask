
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

        with session_scope() as session:
            self.users = RepositoryUsers(session)

        self.user = User(username="lans", email="lans@Julio")

    @patch('desafio.session_scope')
    def test_deve_retornar_id_usuario_depois_add(self, mock_tmp):
        self.users.insert(self.user)
        new_user = self.users.get_user(self.user)
        self.assertIsInstance(new_user.id, int)
        self.assertEqual(new_user.id, 1)

    @patch('desafio.session_scope')
    def test_deve_retornar_integrity_error(self, mock_tmp):
        print(mock_tmp)
        with self.assertRaises(IntegrityError):
            self.users.insert(self.user)

    @patch('desafio.session_scope')
    def test_obtem_um_usuario(self, mock_tmp):
        self.assertTrue(self.users.get_user(self.user) == self.user)

    @patch('desafio.session_scope')
    def test_deve_alterar_o_email_do_usuario(self, mock_tmp):
        new_email = "di@bob"
        self.user.email = new_email
        new_usuario = self.users.update(self.user)
        self.assertEqual(new_usuario.email, self.user.email)


if __name__ == '__main__':
    unittest.main(verbosity=2)

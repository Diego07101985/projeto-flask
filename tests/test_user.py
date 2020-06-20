# from src import dal


try:
    import sys
    import os

    sys.path.append(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '../desafio'
            )
        )
    )
except:
    raise


from desafio.repositorys import RepositoryUsers
from desafio.models import User
from sqlalchemy.exc import IntegrityError
import unittest
from unittest.mock import patch
import pytest

# from test_build import TestApp


@pytest.mark.usefixtures("app", "client", "runner")
class TestRepositoryUser(unittest.TestCase):

    def setUp(self):
        self.users = RepositoryUsers()
        self.user = User(id=1, email="j@j")
        self.user.username("lans")

    @patch('desafio.session_scope')
    def test_2_deve_retornar_integrity_error(self, mock_tmp):
        with self.assertRaises(IntegrityError):
            self.users.insert(self.user)

    @patch('desafio.session_scope')
    def test_1_deve_retornar_id_usuario_depois_add(self, mock_tmp):
        id_user = self.users.insert(self.user)
        self.assertIsInstance(id_user, int)
        self.assertEqual(id_user, 1)

    @patch('desafio.session_scope')
    def test_3_deve_obter_um_usuario_by_id(self, mock_tmp):
        user = self.users.get_user_by_id(self.user)
        self.assertIsInstance(user.id, int)
        self.assertTrue(user == self.user)

    @patch('desafio.session_scope')
    def test_3_deve_obter_um_usuario_by_name(self, mock_tmp):
        user = self.users.get_user_by_name(self.user)
        self.assertIsInstance(user.username(), str)
        self.assertTrue(user == self.user)

    @patch('desafio.session_scope')
    def test_4_deve_alterar_o_email_do_usuario(self, mock_tmp):
        self.user.email = "di@bob"
        update_usuario = self.users.update(self.user)
        self.assertEqual(update_usuario.email, self.user.email)

    @patch('desafio.session_scope')
    def test_5_deve_deletar_um_usuario(self, mock_tmp):
        self.assertIsNone(self.users.delete(self.user))

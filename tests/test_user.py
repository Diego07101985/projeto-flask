
import unittest
from tests import dal
from unittest import MagicMock, mock
from src.models import User
from src.repositorys import RepositoryUsers
from src import Session
from test_build import TestApp


class TestRepositoryUser(TestApp):

    def setUp(self):
        self.session = dal.Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    @mock.patch('src.dal.Session')
    def test_deve_inserir_usuario_return_id(self):
        with mock.patch('module.conn.execute', new=self.patched_conn_execute):
            user = User(username="Paulo", email="paulo@alyson")
            users = RepositoryUsers()
            self.assertEquals(users.insert(user), 1)

            # def test_pessoa_attr_nome_tem_o_valor_correto(self):
            #     self.assertEqual(self.p1.nome, 'Luiz')

            # def test_pessoa_attr_nome_eh_str(self):
            #     self.assertIsInstance(self.p1.nome, str)

            # def test_pessoa_attr_sobrenome_eh_str(self):
            #     self.assertIsInstance(self.p1.sobrenome, str)

            # def test_pessoa_attr_sobrenome_tem_o_valor_correto(self):
            #     self.assertEqual(self.p1.sobrenome, 'Otavio')

            # def test_dados_obtidos_false(self):
            #     self.assertFalse(self.p1.dados_obtidos)

            # def test_obter_todos_os_dados_sucesso_ok(self):
            #     with patch('requests.get') as fake_request:
            #         fake_request.return_value.ok = True
            #         self.assertEqual(self.p1.obter_todos_os_dados(), 'Conectado')
            #         self.assertTrue(self.p1.dados_obtidos)

            # def test_obter_todos_os_dados_falha_404(self):
            #     with patch('requests.get') as fake_request:
            #         fake_request.return_value.ok = False
            #         self.assertEqual(self.p1.obter_todos_os_dados(), '404')
            #         self.assertFalse(self.p1.dados_obtidos)


if __name__ == '__main__':
    unittest.main(verbosity=2)

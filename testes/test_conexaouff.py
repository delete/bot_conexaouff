# coding: utf-8
import unittest

from classes.ConexaoUff import ConexaoUff
from models.Disciplina import Disciplina
from models.Arquivo import Arquivo


class ConexaoUffTest(unittest.TestCase):
	
	def setUp(self):
		self.con = ConexaoUff()

	def test_object(self):
		self.assertIsInstance(self.con, ConexaoUff)

	def test_get_disciplinas(self):
		disciplinas = self.con.getDisciplinas()		
		self.assertEqual(len(disciplinas), 4)
		self.assertIsInstance(disciplinas[0], Disciplina)

	def test_get_arquivos(self):
		arquivos = self.con.getArquivosDeCadaGrupo()		
		self.assertEqual(len(arquivos), 14)
		self.assertIsInstance(arquivos[0], Arquivo)
	
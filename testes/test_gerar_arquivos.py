import unittest
from classes.GerarArquivos import GerarArquivos
from models.Disciplina import Disciplina


class GerarArquivosSuccessTest(unittest.TestCase):

	def setUp(self):
		self.testFile = 'testes/groupTest.html'
		nome = 'Interface Humano-Computador - C1'
		url = 'https://sistemas.uff.br/conexaouff/grupos/77482'
		codigo = '77482'
		self.disciplina = Disciplina(nome=nome, codigo=codigo, url=url)

	def test_disciplinas_amount(self):
		fileContent = open(self.testFile).read()
		files = GerarArquivos.gerar(self.disciplina, fileContent)
		self.assertEqual(len(files), 23)


class GerarArquivosErrorTest(unittest.TestCase):

	def setUp(self):
		self.testFile = 'testes/indexTest.html'
		nome = 'Calculo III - R1'
		url = 'https://sistemas.uff.br/conexaouff/grupos/68207'
		codigo = '68207'
		self.disciplina = Disciplina(nome=nome, codigo=codigo, url=url)

	def test_disciplinas_amount(self):
		fileContent = open(self.testFile).read()
		files = GerarArquivos.gerar(self.disciplina, fileContent)
		self.assertNotEqual(len(files), 23)

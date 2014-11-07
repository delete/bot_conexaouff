import unittest
from classes.GerarDisciplinas import GerarDisciplinas


class GerarDisciplinasSuccessTest(unittest.TestCase):

	def setUp(self):
		self.testFile = 'testes/indexTest.html'

	def test_disciplinas_amount(self):
		disciplinas = GerarDisciplinas.gerar(open(self.testFile).read())
		self.assertEqual(len(disciplinas), 4)


class GerarDisciplinasErrorTest(unittest.TestCase):

	def setUp(self):
		self.testFile = 'testes/groupTest.html'

	def test_disciplinas_amount(self):
		disciplinas = GerarDisciplinas.gerar(open(self.testFile).read())
		self.assertEqual(len(disciplinas), 0)
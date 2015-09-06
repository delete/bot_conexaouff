# coding: utf-8
from bs4 import BeautifulSoup
from models.Disciplina import Disciplina


class GerarDisciplinas(object):

	@staticmethod
	def gerar(pageContent):
		table = GerarDisciplinas.__getTable(pageContent)
		td_tags = GerarDisciplinas.__getTdTags(table)

		disciplinas = []
		if td_tags:
			for td in td_tags:
				disciplina = GerarDisciplinas.__criaObjtDisciplina(td)

				disciplinas.append(disciplina)

		return disciplinas

	@staticmethod
	def __getTable(pageContent):
		soup = BeautifulSoup(pageContent, 'html.parser')
		return soup.find('table', class_='table table-hover')

	@staticmethod
	def __getTdTags(table):
		try:
			tags = table.find_all('td')
			return tags
		except AttributeError:
			print 'Class: GerarDisciplinas - Metodo: __getTdTags'
			print 'Erro de conexão com o site.\n'

	@staticmethod
	def __criaObjtDisciplina(li):
		try:
			url = li.find('a').get('href')
			codigo = url[url.find('s/')+2:]
			nome = li.find('a').get('title')
			return Disciplina(nome=nome, codigo=codigo, url=url)
			
		except AttributeError:
			'Wrong page'
			raise


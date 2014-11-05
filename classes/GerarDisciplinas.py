# coding: utf-8
from bs4 import BeautifulSoup
from models.Disciplina import Disciplina


class GerarDisciplinas(object):

	@staticmethod
	def gerar(pageContent):
		ul_tag = GerarDisciplinas.__getUlTag(pageContent)		
		li_tags = GerarDisciplinas.__getLiTags(ul_tag)

		disciplinas = []
		if li_tags:
			for li in li_tags:
				disciplina = GerarDisciplinas.__criaObjtDisciplina(li)

				disciplinas.append(disciplina)

		return disciplinas

	@staticmethod
	def __getUlTag(pageContent):
		soup = BeautifulSoup(pageContent)
		return soup.find('ul', id='grupos')

	@staticmethod
	def __getLiTags(ul_tag):
		try:
			tags = ul_tag.find_all('li')
			return tags
		except AttributeError:
			print 'Erro de conexão com o site, por favor, tente novamente.'

	@staticmethod
	def __criaObjtDisciplina(li):
		url = li.find('a').get('href')
		codigo = url[url.find('s/')+2:]
		nome = li.find('a').get('title')
		return Disciplina(nome=nome, codigo=codigo, url=url)


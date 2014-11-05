# coding: utf-8
from bs4 import BeautifulSoup
from models.Arquivo import Arquivo


class GerarArquivos(object):

	@staticmethod
	def gerar(disciplina, pageContent):
		ul_tag = GerarArquivos.__getUlTag(pageContent)

		li_tags = GerarArquivos.__getLiTags(ul_tag)

		files = []
		if li_tags:
			for li in li_tags:
				file = GerarArquivos.__createFileObj(li, disciplina)
				files.append(file)

		return files

	@staticmethod
	def __getUlTag(pageContent):
		soup = BeautifulSoup(pageContent)
		return soup.find('ul', id='enviados_por_moderador')
	
	@staticmethod
	def __getLiTags(ul_tag):
		try:
			return ul_tag.find_all('a')
		except AttributeError:
			print 'Erro de conexão com o site, por favor, tente novamente.'

	@staticmethod
	def __createFileObj(link, disciplina):
		title =  link['title']
		url =  link['href']
		d = disciplina
		return Arquivo(titulo=title, url=url, disciplina=d)
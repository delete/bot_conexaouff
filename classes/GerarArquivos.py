# coding: utf-8
from bs4 import BeautifulSoup
from models.Arquivo import Arquivo

from logger import log

class GerarArquivos(object):

	@staticmethod
	def gerar(disciplina, pageContent):
		log(disciplina.nome)
		
		table = GerarArquivos.__getTable(pageContent)

		a_tags = GerarArquivos.__getATags(table)

		files = []
		if a_tags:
			for a in a_tags:
				file = GerarArquivos.__createFileObj(a, disciplina)
				files.append(file)

		return files

	@staticmethod
	def __getTable(pageContent):
		soup = BeautifulSoup(pageContent, 'html.parser')
		return soup.find('table', class_='table table-hover')
	
	@staticmethod
	def __getATags(table):
		try:
			return table.find_all('a')
		except AttributeError:
			log('Class: GerarArquivos - Metodo: __getATags')
			log('Erro de conexão com o site.\n')

	@staticmethod
	def __createFileObj(link, disciplina):
		title =  link['title']
		url =  link['href']
		d = disciplina
		return Arquivo(titulo=title, url=url, disciplina=d)
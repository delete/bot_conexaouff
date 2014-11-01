
class Disciplina():

	def __init__(self, nome, codigo, url):

		self.nome = nome
		self.codigo = codigo
		self.url = url

	def __str__(self):
		return '%s - %s' %(nome, codigo)
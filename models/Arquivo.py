
class Arquivo():

	def __init__(self, titulo, url, disciplina):

		self.titulo = titulo
		self.url = url
		self.disciplina = disciplina

	def __str__(self):
		return '%s' %(self.titulo)

	def __repr__(self):
		return '%s' %(self.titulo)
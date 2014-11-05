import os


class BaixarArquivos(object):

	NAVEGADOR = None

	@staticmethod
	def baixar(files, navegador):		
		
		BaixarArquivos.NAVEGADOR = navegador
		
		if files:
			for file in files:
				BaixarArquivos.NAVEGADOR.setUrl(file.url + '/download')

				BaixarArquivos.__baixa_e_salva_se_nao_existe(file)

	@staticmethod
	def __baixa_e_salva_se_nao_existe(file):
		if not os.path.exists(file.disciplina.nome):
			os.makedirs(file.disciplina.nome)

		file_path = file.disciplina.nome + '/' + file.titulo
		if not os.path.exists(file_path):
			BaixarArquivos.__baixa_e_salva_arquivo(file_path)

			print '[+] %s -> %s' % (file.titulo, file.disciplina.nome)

	@staticmethod
	def __baixa_e_salva_arquivo(file_path):
		with open(file_path, 'w') as file:
			conteudo = BaixarArquivos.NAVEGADOR.getContent()
			file.write(conteudo)		
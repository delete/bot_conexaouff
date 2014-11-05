# coding: utf-8
from Navegador import Navegador
from GerarArquivos import GerarArquivos
from GerarDisciplinas import GerarDisciplinas
from BaixarArquivos import BaixarArquivos


class ConexaoUff(object):
    
    def __init__(self):        

        self.DEFAULT_URL = 'https://sistemas.uff.br/conexaouff'

        self.__navegador = Navegador()
        self.__navegador.setUrl(self.DEFAULT_URL)
        self.__navegador.login()

        self.disciplinas = list()
        self.arquivos = list()

    def baixarArquivos(self):
        quantidade = 0
        self.getArquivosDeCadaGrupo()

        BaixarArquivos.baixar(self.arquivos, self.__navegador)

    def getArquivosDeCadaGrupo(self):
        self.getDisciplinas()
        
        for disciplina in self.disciplinas:
            self.__navegador.setUrl(self.DEFAULT_URL + '/grupos/%s/arquivos' % (disciplina.codigo))
            
            conteudo = self.__navegador.getContent()
            arquivos = GerarArquivos.gerar(disciplina, conteudo)
            self.arquivos.extend(arquivos)

        return self.arquivos

    def getDisciplinas(self):
        self.__navegador.setUrl(self.DEFAULT_URL)
        
        conteudo = self.__navegador.getContent()
                
        self.disciplinas = GerarDisciplinas.gerar(conteudo)

        return self.disciplinas

    def close(self):
        self.__navegador.exit()

# coding: utf-8
import os
from bs4 import BeautifulSoup
from Navegador import Navegador
from GerarArquivos import GerarArquivos
from GerarDisciplinas import GerarDisciplinas
from models.Disciplina import Disciplina
from models.Arquivo import Arquivo


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

        for arquivo in self.arquivos:
            file_path = arquivo.disciplina.nome + '/' + arquivo.titulo            
            self.__navegador.setUrl(arquivo.url + '/download')
            
            if not os.path.exists(arquivo.disciplina.nome):
                os.makedirs(arquivo.disciplina.nome)

            if not os.path.exists(file_path):
                self.__baixa_e_salva_arquivo(file_path)
                
                print '[+] %s -> %s' % (arquivo.titulo, arquivo.disciplina.nome)
                quantidade += 1

        if self.arquivos:
            print '\n[!] Foram baixados %d arquivos!' %(quantidade)

    def __baixa_e_salva_arquivo(self,file_path):
        with open(file_path, 'w') as file:
            conteudo = self.__navegador.getContent()
            file.write(conteudo)

    def getArquivosDeCadaGrupo(self):      
        self.getDisciplinas()
        
        for disciplina in self.disciplinas:
            self.__navegador.setUrl(self.DEFAULT_URL + '/grupos/%s/arquivos' % (disciplina.codigo))
            
            conteudo = self.__navegador.getContent()
            
            self.arquivos = GerarArquivos.gerar(disciplina, conteudo)

        return self.arquivos

    def getDisciplinas(self):
        self.__navegador.setUrl(self.DEFAULT_URL)
        
        conteudo = self.__navegador.getContent()
                
        self.disciplinas = GerarDisciplinas.gerar(conteudo)        
                    
        return self.disciplinas

    def close(self):
        self.__navegador.exit()

# coding: utf-8
import os
from bs4 import BeautifulSoup
from Navegador import Navegador
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
            links = self.__getLinks(conteudo)

            for link in links:
                arquivo = self.__criaObjtArquivo(link, disciplina)
                self.arquivos.append(arquivo)

        return self.arquivos

    def __getLinks(self, conteudo):
        soup = BeautifulSoup(conteudo)
        html_ul = soup.find('ul', id='enviados_por_moderador')
        html_com_todos_os_links = html_ul.find_all('a')
        return html_com_todos_os_links


    def __criaObjtArquivo(self, link, disciplina):
        title =  link['title']
        url =  link['href']
        d = disciplina
        return Arquivo(titulo=title, url=url, disciplina=d)

    def getDisciplinas(self):
        self.__navegador.setUrl(self.DEFAULT_URL)
        
        conteudo = self.__navegador.getContent()        
        
        html_lis = self.__getDisciplinasAsLiHtml(conteudo)
        if html_lis:
            for li in html_lis:
                disciplina = self.__criaObjtDisciplina(li)
                
                self.disciplinas.append(disciplina)        
                    
        return self.disciplinas

    def __getDisciplinasAsLiHtml(self, conteudo):
        soup = BeautifulSoup(conteudo)
        try:
            html_ul = soup.find('ul', id='grupos')
            html_lis = html_ul.find_all('li')
            return html_lis
        
        except AttributeError:
            print 'Erro de conexão, por favor, tente novamente.'
    
    def __criaObjtDisciplina(self, li):
        url = li.find('a').get('href')
        codigo = url[url.find('s/')+2:]
        nome = li.find('a').get('title')
        return Disciplina(nome=nome, codigo=codigo, url=url)

    def close(self):
        self.__navegador.exit()

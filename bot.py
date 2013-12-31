#! /usr/bin/env python
# coding: utf-8

import os
import json
import cookielib
import mechanize
from bs4 import BeautifulSoup


class Navegador(object):
    def __init__(self):        
        'Configura um browser e o cookie para manter logado na pagina.'
        
        #cria um navegador.
        self.__br = mechanize.Browser()

        # Prepara para tratar cookies...
        cj = cookielib.LWPCookieJar()
        self.__br.set_cookiejar(cj)

        # Ajusta algumas opcoes do navegador...
        self.__br.set_handle_equiv(True)
        self.__br.set_handle_gzip(False)
        self.__br.set_handle_redirect(True)
        self.__br.set_handle_referer(True)
        self.__br.set_handle_robots(False)
        self.__br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # Configura o user-agent.
        # Do ponto de vista do servidor, o navegador agora e o Firefox.
        self.__br.addheaders = [('User-agent', 'Mozilla/5.0 (X11;\
                                U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615\
                                Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        
    def __auth(self):
        '''Pega CPF e senha do arquivo auth em formato JSON,
            retornando um tupla com os dados.
        '''
        arq = open("auth")
        data = arq.read()
        data_json = json.loads(data)
        login = data_json['cpf']
        senha = data_json['senha']

        return (login, senha)

    def url(self, _url):
        'Insere uma URL no browser'
        self.__url = _url
        self.__br.open(self.__url)

    def login(self):
        'Faz um POST na pagina com o dados de login.'
        login, senha = self.__auth()
        # Se existirem formulários, você pode selecionar o primeiro (#0), por exemplo..
        self.__br.select_form(nr=0)
        # Preenche o formulário com os dados de login...
        self.__br.form['iduff'] = login
        self.__br.form['senha'] = senha
        # Envia o formulário usando o método HTTP POST
        self.__br.submit()

    def get_page(self):
        'Retorna o HTML'
        return self.__br.response().read()


class ConexaoUff(object):

    def __init__(self):
        'Instancia um site e seta um url padrao para manter o login em cookie.'

        self.__site = Navegador()
        self.__site.url('https://sistemas.uff.br/conexaouff')
        self.__site.login()

    def get_grupos(self):
        '''Retorna um dicionario com codigo e nome da disciplina
            Exemplo: {
                      'codigo1': nome_disciplina1, 
                      'codigo2': none_disciplina2
                     }
        '''
        self.__site.url('https://sistemas.uff.br/conexaouff')
        
        # Seleciona uma 'lista nao ordenada'(<ul>) da pagina, pelo id=grupos.        
        try:
            soup = BeautifulSoup(self.__site.get_page())
            lista = soup.find('ul', id='grupos')

            self.grupos = {}

            for item in lista.find_all('li'):
                codigo = item.find('a').get('href')            
                self.grupos[codigo[codigo.find('s/')+2:]] = item.find('a').get('title')                
        except AttributeError:
            print '\n\n[-]Entre com um login válido, no arquivo "auth"! \n\n'
            
        return self.grupos
            
    def __get_page_arquivos(self):
        '''Retorna uma lista de dicionarios, com link do arquivo e titulo do arquivo.
        Exemplo: 
        [
            {'/conexaouff/grupos/CODIGO_GRUPO_1/arquivos/CODIGO_ARQUIVO_1': 'TITULO_DO_ARQUIVO_1',
            '/conexaouff/grupos/CODIGO_GRUPO_1/arquivos/CODIGO_ARQUIVO_2': 'TITULO_DO_ARQUIVO_2' },
            
            {'/conexaouff/grupos/CODIGO_GRUPO_2/arquivos/CODIGO_ARQUIVO_1': 'TITULO_DO_ARQUIVO_1',
            '/conexaouff/grupos/CODIGO_GRUPO_2/arquivos/CODIGO_ARQUIVO_2': 'TITULO_DO_ARQUIVO_2' },
        ]
        '''
      
        grupos = self.get_grupos()
        self.__listaArq = []
        for key in grupos.keys():
            dicio = {}
            self.__site.url('https://sistemas.uff.br/conexaouff/grupos/%s/arquivos' % (key))
            try:
                soup = BeautifulSoup(self.__site.get_page())
                lista = soup.find_all('ul')
                arquivos = list(lista[1])
                dicio = {}
                for arquivo in arquivos:
                    try:
                        dicio[arquivo.a['href'][arquivo.a['href'].find('grupos/')+7:]] = arquivo.a['title']
                    except:
                        pass
            except:
                pass
            self.__listaArq.append(dicio)

    def get_arquivos(self):
        'Baixa cada arquivo, de cada grupo.'
        self.__get_page_arquivos()        
        for item in self.__listaArq:
            for key in item.keys():
                self.__site.url('https://sistemas.uff.br/conexaouff/grupos/%s/download' % (key))
                try:
                    #Testa se o arquivo ja existe, se nao existir, baixa!
                    open(self.grupos.get(key[:key.find('/')]) + '/' + item[key])
                except:
                    try:
                        #Tenta criar o diretorio, se existir, apenas baixa o arquivo.
                        os.mkdir(self.grupos.get(key[:key.find('/')]))
                    except OSError:
                        pass
                    arq = open(self.grupos.get(key[:key.find('/')]) + '/' + item[key], 'w')
                    texto = self.__site.get_page()
                    arq.write(texto)
                    arq.close()
                    print '[+] %s - Baixado!' % (item[key])

def header():
    try:
        os.system('clear')    
    except:
        os.system('cls')
    
    print '''
    _____        _   
    | __ )  ___ | |_ 
    |  _ \ / _ \| __|
    | |_) | (_) | |_ 
    |____/ \___/ \__| ConexaoUff
    por Fellipe Pinheiro

[!] Verificando arquivos a serem baixados... \n'''

if __name__ == '__main__':
    header()
    p = ConexaoUff()        
    p.get_arquivos()


                 

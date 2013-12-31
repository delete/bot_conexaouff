# coding: utf-8

import json
import cookielib
import mechanize

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
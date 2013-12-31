# coding: utf-8
import os
from bs4 import BeautifulSoup
from Navegador import Navegador


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

    def get_matriculados(self):
        '''
            https://sistemas.uff.br/conexaouff/grupos/49758/usuarios
            Retorna uma lista de lista de dicionarios de alunos.
            grupos = [
                        grupo1 = [
                                    aluno1: {'codigo': 'CODIGO',
                                           'nome': 'NOME',
                                           'foto': 'LINK_FOTO',
                                           'grupo': 'CODIGO_GRUPO',
                                           },

                                    aluno2: {'codigo': 'CODIGO',
                                             'nome': 'NOME',
                                             'foto': 'LINK_FOTO',
                                             'grupo': 'CODIGO_GRUPO',
                                            },

                                ], 

                        grupo2 = [
                                    aluno1: {'codigo': 'CODIGO',
                                           'nome': 'NOME',
                                           'foto': 'LINK_FOTO',
                                           'grupo': 'CODIGO_GRUPO',
                                           },

                                    aluno2: {'codigo': 'CODIGO',
                                             'nome': 'NOME',
                                             'foto': 'LINK_FOTO',
                                             'grupo': 'CODIGO_GRUPO',
                                            },

                                ],
                     ]

        '''
        grupos = self.get_grupos()

        lista_grupos = []

        for key in grupos.keys():
            lista = []
            self.__site.url('https://sistemas.uff.br/conexaouff/grupos/%s/usuarios' % (key))

            #Seleciona todas as div's com class=profile
            soup = BeautifulSoup(self.__site.get_page())
            conteudo = soup.find_all('div', {'class':'profile'})
                                
            for item in conteudo:
                #Cria um 'dicionario de aluno' com os dados do aluno
                dicio = {}    
                codigo = item.find('a').get('href')
                codigo = codigo[codigo.find('s/')+2:]
                dicio['grupo'] = key
                dicio['codigo'] = codigo
                dicio['nome'] = item.find('a').get('title').lower().title()
                dicio['foto'] = item.find('img').get('src')
                
                #Adiciona o 'd'icionario aluno' em uma 'l'ista de alunos'
                lista.append(dicio)

            #Adiciona a 'lista de alunos' dentro da 'lista de grupos'
            lista_grupos.append(lista)

        return lista_grupos
    
    def get_usuario(self):
        '''Retorna um diciona com os dados do usuario logado.
            {
                'nome': 'NOME',
                'foto': 'LINK_FOTO',
            }

        '''
        self.__site.url('https://sistemas.uff.br/conexaouff/')

        soup = BeautifulSoup(self.__site.get_page())
        lista = soup.find_all('img')
        dicio = {}
        dicio['nome'] = lista[2].get('alt').lower().title()
        dicio['foto'] = lista[2].get('src')
        
        return dicio
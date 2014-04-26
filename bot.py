# coding: utf-8
from classes import ConexaoUff
import os
import mechanize

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
    try:  
	p.get_arquivos()
    except mechanize.HTTPError, e:
        if e.code == 500:
            print u'[-]Parece que o site está fora do ar, tente mais tarde.'
        else:
            raise e
        

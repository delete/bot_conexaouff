from classes import ConexaoUff
import os

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
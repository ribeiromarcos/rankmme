# -*- coding: utf-8 -*-

'''
Arquivos
'''

import json
from datetime import datetime, timedelta
from os.path import isdir, isfile, getmtime
from os import mkdir, sep
from pathlib import Path

DIR_CACHE = '.cache'

def dir_cache():
    '''Diretório de dados'''
    _dir_dados = str(Path.home()) + sep + DIR_CACHE
    if not isdir(_dir_dados):
        mkdir(_dir_dados)
    return _dir_dados

def arquivo_atualizado(arquivo):
    '''Verifica se arquivo está atualizado'''
    # Verifica se arquivo existe
    if isfile(arquivo):
        # Data do arquivo
        data_arquivo = datetime.fromtimestamp(getmtime(arquivo))
        # Data atual
        data_atual = datetime.now()
        data_arquivo = data_arquivo + timedelta(days=1)
        if data_arquivo.date() >= data_atual.date():
            return True
    return False

def caminho_arquivo(nome_arquivo, subdir=None):
    '''Arquivo de símbolos''' 
    if subdir:
        dir_arq = dir_cache() + sep + subdir
        if not isdir(dir_arq):
            mkdir(dir_arq)
        nome_arquivo = dir_arq + sep + nome_arquivo
    return nome_arquivo

def abre_json(arquivo, subdir=None):
    '''Abre arquivo JSON'''
    nome_arq = caminho_arquivo(arquivo, subdir)
    if isfile(nome_arq):
        with open(nome_arq, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    return None

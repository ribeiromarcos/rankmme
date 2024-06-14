# -*- coding: utf-8 -*-

'''
Dados da Yahoo Finance
'''

from datetime import datetime, timedelta
import time
import yfinance as yf
import pandas as pd
from arquivos import caminho_arquivo, arquivo_atualizado, abre_json

DELAY = 1

SUB_DIR_YAHOO = 'yahoo'
ARQ_ATIVOS = 'ativos.json'

def _baixa_historico(simbolo, arquivo):
    '''Baixa histórico de cotações'''
    hist = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
    data_final = datetime.now() - timedelta(days=1)
    time.sleep(DELAY)
    try:
        hist = yf.download(simbolo + '.SA', end=data_final.strftime('%Y-%m-%d'),
                           progress=False, threads=False)
        hist.to_csv(arquivo)
    except Exception: # pylint: disable=broad-except
        pass
    return hist

def historico_yahoo(simbolo):
    '''Obtém histórico de cotações da Yahoo Finance'''
    arquivo = caminho_arquivo(simbolo + '.csv', SUB_DIR_YAHOO)
    if not arquivo_atualizado(arquivo):
        hist = _baixa_historico(simbolo, arquivo)
    else:
        try:
            hist = pd.read_csv(arquivo, parse_dates=True, index_col='Date')
        except Exception: # pylint: disable=broad-except
            hist = _baixa_historico(simbolo, arquivo)
    return hist

def lista_ativos():
    '''Lista de ativos'''
    ativos = abre_json(ARQ_ATIVOS)
    if not ativos:
        ativos = []
    return ativos

def principal():
    '''Função principal'''
    ativos = lista_ativos()
    for simbolo in ativos[:2]:
        print(simbolo)
        hist = historico_yahoo(simbolo)
        print(hist.head())
        print(hist.tail())
        print()

if __name__ == '__main__':
    principal()

# -*- coding: utf-8 -*-

'''
Rank MME
'''

import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from yahoo import historico_yahoo

PERIODO = 90
JANELA_MENOR = 9
JANELA_MAIOR = 30
JANELA_LONGA = 200

COL_ALTA = 'Alta'
COL_CRUZAMENTO = 'Cruzamento'
COL_COMPRA = 'Compra'
COL_VENDA = 'Venda'

def calcula_mme(ativo, lista_janelas):
    '''Calcula MME'''
    df_ativo = historico_yahoo(ativo)
    lista_janelas.sort()
    for janela in lista_janelas:
        col_mme = 'MME' + str(janela)
        df_ativo[col_mme] = df_ativo['Close'].ewm(span=janela).mean()
    mme_curta = 'MME' + str(lista_janelas[0])
    mme_media = 'MME' + str(lista_janelas[1])
    df_ativo[COL_ALTA] = np.where(df_ativo[mme_curta] >
                                  df_ativo[mme_media], 1, 0)
    df_ativo[COL_CRUZAMENTO] = df_ativo[COL_ALTA].diff()
    df_ativo = df_ativo.dropna()
    return df_ativo

def rank_mme(ativo, lista_janelas, periodo):
    '''Rank MME'''
    # df = _baixa_dados(ativo)
    df_ativo = calcula_mme(ativo, lista_janelas)
    if len(df_ativo) == 0:
        return float('-inf'), df_ativo
    lista_janelas.sort()
    df_ativo = df_ativo[-periodo:]
    df_ult_cru = df_ativo[df_ativo.Cruzamento != 0].tail(1)
    if len(df_ult_cru) == 0:
        return float('-inf'), df_ativo
    mme_longa = 'MME' + str(lista_janelas[1])
    rank = (df_ativo[mme_longa].values[-1] - df_ativo[mme_longa].values[0]) / \
        df_ativo[mme_longa].values[0]
    if df_ult_cru.Cruzamento.values[-1] == -1 and rank > 0:
        rank = -rank
    dias = datetime.now() - df_ult_cru.index[-1]
    rank = rank / (dias.days + 1)
    return rank, df_ativo

def plota_mme(df_ativo, lista_janelas):
    '''Calcula MME'''
    lista_janelas.sort()
    mme_curta = 'MME' + str(lista_janelas[0])
    mme_media = 'MME' + str(lista_janelas[1])
    mme_longa = 'MME' + str(lista_janelas[2])
    fig = plt.figure(figsize=(12, 8))
    ax1 = fig.add_subplot(111, ylabel='Preço')
    df_ativo['Close'].plot(ax=ax1, color='b', lw=2.)
    df_ativo[mme_curta].plot(ax=ax1, color='r', lw=2.)
    df_ativo[mme_media].plot(ax=ax1, color='g', lw=2.)
    df_ativo[mme_longa].plot(ax=ax1, color='y', lw=2.)
    ax1.plot(df_ativo.loc[df_ativo.Cruzamento == 1].index,
             df_ativo.Close[df_ativo.Cruzamento == 1],
            '^', markersize=10, color='g')
    ax1.plot(df_ativo.loc[df_ativo.Cruzamento == -1].index,
             df_ativo.Close[df_ativo.Cruzamento == -1],
            'v', markersize=10, color='r')
    plt.legend(['Preço', mme_curta, mme_media, mme_longa, 'Compra', 'Venda'])
    plt.grid()
    plt.show()
    return df_ativo

def teste():
    '''Função principal'''
    rank, df_ativo = rank_mme('KOPA11', [9, 30, 200], 30)
    print(rank)
    if len(df_ativo) > 0:
        plota_mme(df_ativo, [9, 30, 200])

if __name__ == '__main__':
    teste()

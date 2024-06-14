# -*- coding: utf-8 -*-

'''
Streamlit Rank MME App
'''

import matplotlib.pyplot as plt
import streamlit as st

from rank import rank_mme
from yahoo import lista_ativos


def plota(df_ativo, lista_janelas):
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
    ax1.legend(['Preço', mme_curta, mme_media, mme_longa, 'Compra', 'Venda'])
    st.pyplot(fig)

def lista_rank_mme(janelas, periodo, limite, num_ativos):
    '''Lista rank MME'''
    lista = lista_ativos()
    dicio_df = {}
    lista_rank = []
    for ativo in lista:
        print(ativo)
        rank, df_ativo = rank_mme(ativo, janelas, periodo, limite)
        if len(df_ativo) > 0 and rank > 0:
            dicio_df[ativo] = df_ativo
            atual = {'ativo': ativo, 'rank': rank}
            lista_rank.append(atual)
    lista_rank = [item for item in lista_rank
                  if item['rank'] != float('-inf')]
    lista_rank.sort(key=lambda x: x['rank'], reverse=True)
    num_ativos = min(num_ativos, len(lista_rank))
    for cont in range(num_ativos):
        ativo = lista_rank[cont]['ativo']
        df_ativo = dicio_df[ativo]
        st.write(ativo, lista_rank[cont]['rank'])
        plota(df_ativo, janelas)


def principal():
    '''Função principal'''
    st.title('Rank MME')
    # st.write('Rank MME')
    janela_curta = st.slider('Janela curta', 5, 80, step=1, value=9)
    janela_media = st.slider('Janela média', 10, 200, step=1, value=30)
    janela_longa = st.slider('Janela longa', 30, 300, step=1, value=200)
    periodo = st.slider('Período gráfico', 5, 120, step=1, value=60)
    limite = st.slider('Limite cruzamento', 1, 30, step=1, value=1)
    num_ativos = st.slider('Número de ativos', 5, 500, step=1, value=10)
    janelas = [janela_curta, janela_media, janela_longa]
    if st.button('Listar'):
        lista_rank_mme(janelas, periodo, limite, num_ativos)

if __name__ == '__main__':
    principal()

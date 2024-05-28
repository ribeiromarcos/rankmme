import json
import streamlit as st
from pathlib import Path
from os import mkdir, sep

cache_dir = str(Path.home()) + sep + '.cache'
mkdir(dir_cache)
cache_dir += sep + 'teste'
mkdir(dir_cache)
nome_arq = dir_cache + sep + 'teste.json'

conteudo = list(range(10))
with open(nome_arq, 'w', encoding='utf-8') as arq:
    json.dump(conteudo, arq, indent=2, ensure_ascii=False)

lista_salva = []
with open(nome_arq, 'r', encoding='utf-8') as arq:
    lista_salva = json.load(arq)
  
st.write('Olá Mundo!')
st.write('Lista Salva')


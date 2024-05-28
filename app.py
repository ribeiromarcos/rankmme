import json
import streamlit as st
from pathlib import Path
from os import mkdir, sep
from os.path import isdir

cache_dir = str(Path.home()) + sep + '.cache'
if not isdir(cache_dir):
    mkdir(cache_dir)
cache_dir += sep + 'teste'
if not isdir(cache_dir):
    mkdir(cache_dir)
nome_arq = cache_dir + sep + 'teste.json'

conteudo = list(range(10))
with open(nome_arq, 'w', encoding='utf-8') as arq:
    json.dump(conteudo, arq, indent=2, ensure_ascii=False)

lista_salva = []
with open(nome_arq, 'r', encoding='utf-8') as arq:
    lista_salva = json.load(arq)
  
st.write('Olá Mundo!')
st.write(lista_salva)


# ibprogramearj
import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def fazer_raspagem():
    url = "https://www.earj.com.br/ib-programme-at-earj/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    tabela = soup.find("table")  # Encontra a tabela no conteúdo HTML da página

    if tabela is None:
        st.write("Tabela não encontrada.")
        return None

    # Extrai os dados da tabela
    dados = []
    linhas = tabela.find_all("tr")
    for linha in linhas:
        celulas = linha.find_all("td")
        valores_celulas = [celula.text.strip() for celula in celulas]
        dados.append(valores_celulas)

    # Cria um DataFrame do pandas com os dados extraídos
    colunas = dados[0]
    dados = dados[1:]
    df = pd.DataFrame(dados, columns=colunas)
    return df

df = fazer_raspagem()

if df is not None:
    # Criando filtros para as divisões
    divisoes = df["Divisões"].unique()

    # Sidebar para selecionar a divisão
    divisao_selecionada = st.sidebar.selectbox("Selecione uma Divisão", divisoes)

    # Filtrando o DataFrame com base na divisão selecionada
    df_filtrado = df[df["Divisões"] == divisao_selecionada]

    # Organizando os dados com base nas categorias
    st.write("**Dados Organizados**")
    st.dataframe(df_filtrado[["Campus", "Theory of Knowledge", "Extended Essay", "Creativity, activity, and service (CAS)", "Learning Outcomes", "Certificates"]])

else:
    st.write("Não foi possível obter os dados.")

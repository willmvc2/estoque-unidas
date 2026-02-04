import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Estoque Unidas",
    page_icon="🚗",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background-color: #2b59b4;
    color: white;
}

p, span, div {
    font-size: 18px;
}

h1 {
    font-size: 40px;
    color: white;
}

h3 {
    font-size: 24px;
    color: white;
}

input {
    font-size: 20px !important;
}

.stButton > button {
    background-color: #f1d064;
    color: #1e3d7d;
    font-weight: bold;
    font-size: 18px;
    border-radius: 6px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.title("🚗 Estoque Unidas")

ARQUIVO = "data/estoque.xlsx"

if not os.path.exists(ARQUIVO):
    st.error("Base de dados indisponível. Contate o administrador.")
    st.stop()

df = pd.read_excel(ARQUIVO)

df.columns = df.columns.str.strip()

if "Placa" not in df.columns:
    st.error("A planilha precisa ter a coluna 'Placa'.")
    st.stop()

df["Placa"] = df["Placa"].astype(str).str.upper().str.strip()

st.subheader("Digite a placa do veículo")

placa = st.text_input(
    "Ex: ABC1D23",
    placeholder="Digite a placa aqui"
).upper().strip()

if st.button("PESQUISAR"):
    resultado = df[df["Placa"] == placa]

    if resultado.empty:
        st.error("Placa não encontrada.")
    else:
        row = resultado.iloc[0]
        st.markdown("---")

        for campo in df.columns:
            valor = row[campo]
            st.write(f"**{campo}:** {valor}")

import streamlit as st
import pandas as pd
import os

# =====================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================
st.set_page_config(
    page_title="Estoque Unidas",
    page_icon="🚗",
    layout="centered"
)

# =====================================
# ESTILO (FONTES E CORES)
# =====================================
st.markdown("""
<style>
.stApp {
    background-color: #2b59b4;
    color: white;
}

/* Texto padrão */
p, span, div {
    font-size: 18px;
}

/* Título */
h1 {
    font-size: 40px;
    color: white;
}

/* Subtítulo */
h3 {
    font-size: 24px;
    color: white;
}

/* Inputs */
input {
    font-size: 20px !important;
}

/* Botões */
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

# =====================================
# TÍTULO
# =====================================
st.title("🚗 Estoque Unidas")

# =====================================
# CAMINHO DA PLANILHA
# =====================================
ARQUIVO = "data/estoque.xlsx"

# =====================================
# VERIFICA SE EXISTE PLANILHA
# =====================================
if not os.path.exists(ARQUIVO):
    st.error("Base de dados indisponível. Contate o administrador.")
    st.stop()

# =====================================
# CARREGA PLANILHA
# =====================================
try:
    df = pd.read_excel(ARQUIVO)
except Exception:
    st.error("Erro ao carregar a planilha.")
    st.stop()

# =====================================
# AJUSTES DE COLUNAS
# =====================================
df.columns = df.columns.str.strip()

if "Placa" not in df.columns:
    st.error("A planilha precisa ter a coluna 'Placa'.")
    st.stop()

df["Placa"] = df["Placa"].astype(str).str.upper().str.strip()

# =====================================
# BUSCA
# =====================================
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

            if isinstance(valor, (int, float)) and campo.lower() != "km":
                st.write(f"**{campo}:** R$ {valor:,.2f}")
            else:
                st.write(f"**{campo}:** {valor}")

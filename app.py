import streamlit as st
import pandas as pd
import os

# ===============================
# CONFIGURAÇÃO DA PÁGINA
# ===============================
st.set_page_config(
    page_title="Estoque Unidas",
    page_icon="🚗",
    layout="centered"
)

# ===============================
# ESTILOS (FONTES, CORES, BOTÕES)
# 👉 AQUI VOCÊ MUDA O TAMANHO DA FONTE
# ===============================
st.markdown("""
<style>
/* Fundo geral */
.stApp {
    background-color: #2b59b4;
    color: white;
}

/* TEXTO PADRÃO */
.stMarkdown, .stText, p {
    font-size: 10px;   /* 👈 MUDE AQUI */
}

/* TÍTULO PRINCIPAL */
h1 {
    font-size: 20px;   /* 👈 MUDE AQUI */
    color: white;
}

/* SUBTÍTULOS */
h3 {
    font-size: 15px;   /* 👈 MUDE AQUI */
    color: white;
}

/* CAMPOS DE TEXTO (inputs) */
input {
    font-size: 20px !important;  /* 👈 MUDE AQUI */
}

/* BOTÕES */
.stButton>button {
    background-color: #f1d064;
    color: #1e3d7d;
    font-weight: bold;
    font-size: 18px;   /* 👈 MUDE AQUI */
    border-radius: 6px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# TÍTULO
# ===============================
st.title("🚗 Estoque Unidas")

# ===============================
# CARREGA PLANILHA SALVA NO GITHUB
# ===============================
CAMINHO_ARQUIVO = "data/estoque.xlsx"

if not os.path.exists(CAMINHO_ARQUIVO):
    st.error("Base de dados indisponível. Contate o administrador.")
    st.stop()

df = pd.read_excel(CAMINHO_ARQUIVO)

# Limpeza básica
df.columns = df.columns.str.strip()
df["Placa"] = df["Placa"].astype(str).str.strip().str.upper()

# ===============================
# BUSCA
# ===============================
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
        st.write(f"**Placa:** {row['Placa']}")
        st.write(f"**Modelo:** {row['Modelo']}")
        st.write(f"**Cor:** {row['Cor']}")
        st.write(f"**Ano:** {row['Ano']}")
        st.write(f"**KM:** {row['KM']}")

        fipe = row["Valor FIPE"]
        st.write(
            f"**Valor FIPE:** R$ {fipe:,.2f}"
            if isinstance(fipe, (int, float))
            else f"**Valor FIPE:** {fipe}"
        )

        valor = row["VALOR"]
        st.write(
            f"**Valor:** R$ {valor:,.2f}"
            if isinstance(valor, (int, float))
            else f"**Valor:** {valor}"
        )

        st.write(f"**Margem:** {row['MARGEM']}")

import streamlit as st
import pandas as pd
import os

# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================
st.set_page_config(
    page_title="Estoque Unidas",
    page_icon="🚗",
    layout="centered"
)

# ==============================
# ESTILO
# ==============================
st.markdown("""
<style>
.stApp { background-color: #2b59b4; color: white; }
p, span, div { font-size: 18px; }
h1 { font-size: 40px; color: white; }
h3 { font-size: 24px; color: white; }
input { font-size: 20px !important; }
.stButton > button {
    background-color: #f1d064;
    color: #1e3d7d;
    font-weight: bold;
    font-size: 18px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# DETECTA MODO ADMIN (CORRETO)
# ==============================
modo_admin = st.query_params.get("admin") == "1"

# ==============================
# ÁREA ADMIN (OCULTA)
# ==============================
if modo_admin:
    st.title("🔐 Área do Administrador")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if (
            usuario == st.secrets["admin"]["user"]
            and senha == st.secrets["admin"]["password"]
        ):
            st.session_state["admin_logado"] = True
        else:
            st.error("Credenciais inválidas")

    if st.session_state.get("admin_logado"):
        st.success("Login realizado com sucesso")

        arquivo = st.file_uploader(
            "Upload do estoque (estoque.xlsx)",
            type=["xlsx"]
        )

        if arquivo:
            os.makedirs("data", exist_ok=True)
            with open("data/estoque.xlsx", "wb") as f:
                f.write(arquivo.getbuffer())

            st.success("Estoque atualizado com sucesso")

    st.stop()

# ==============================
# USUÁRIO COMUM
# ==============================
st.title("🚗 Estoque Unidas")

ARQUIVO = "data/estoque.xlsx"

if not os.path.exists(ARQUIVO):
    st.error("Base de dados indisponível.")
    st.stop()

df = pd.read_excel(ARQUIVO)
df.columns = df.columns.str.strip()
df["Placa"] = df["Placa"].astype(str).str.upper().str.strip()

st.subheader("Digite a placa do veículo")

placa = st.text_input("Ex: ABC1D23").upper().strip()

if st.button("PESQUISAR"):
    resultado = df[df["Placa"] == placa]

    if resultado.empty:
        st.error("Placa não encontrada")
    else:
        row = resultado.iloc[0]
        st.markdown("---")
        for col in df.columns:
            st.write(f"**{col}:** {row[col]}")

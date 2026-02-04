import streamlit as st
import pandas as pd
import hashlib

# ======================
# CONFIGURAÇÃO DA PÁGINA
# ======================
st.set_page_config(
    page_title="Estoque Unidas",
    page_icon="🚗",
    layout="centered"
)

# ======================
# FUNÇÕES AUXILIARES
# ======================
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def admin_logado():
    return st.session_state.get("admin", False)

# ======================
# IDENTIFICA SE É ADMIN
# ======================
query_params = st.query_params
modo_admin = query_params.get("admin") == "1"

# ======================
# ESTILO
# ======================
st.markdown("""
<style>
.stApp {
    background-color: #1f3b78;
    color: white;
}
button {
    background-color: #f1d064 !important;
    color: #1f3b78 !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# ===================== MODO ADMIN =====================
# ======================================================
if modo_admin:

    st.title("🔐 Administração - Estoque Unidas")

    # LOGIN
    if not admin_logado():
        st.subheader("Login do Administrador")

        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            if (
                usuario == st.secrets["admin"]["user"]
                and hash_senha(senha) == st.secrets["admin"]["password"]
            ):
                st.session_state.admin = True
                st.success("Login realizado com sucesso")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos")

    # ÁREA ADMIN
    else:
        st.success("Você está logado como administrador")

        arquivo = st.file_uploader(
            "Enviar planilha de estoque (.xlsx)",
            type=["xlsx"]
        )

        if arquivo:
            df = pd.read_excel(arquivo)
            df.to_csv("estoque.csv", index=False)
            st.success("Planilha salva com sucesso")

        if st.button("Sair"):
            st.session_state.admin = False
            st.rerun()

# ======================================================
# =================== MODO USUÁRIO =====================
# ======================================================
else:
    st.title("🚗 Estoque Unidas")
    st.subheader("Consultar veículo por placa")

    placa = st.text_input("Digite a placa (ex: ABC1D23)").upper().strip()

    if st.button("Pesquisar"):
        try:
            df = pd.read_csv("estoque.csv")
            df["Placa"] = df["Placa"].astype(str).str.upper().str.strip()

            resultado = df[df["Placa"] == placa]

            if resultado.empty:
                st.error("Placa não encontrada")
            else:
                row = resultado.iloc[0]
                st.markdown("---")
                st.write(f"**Placa:** {row['Placa']}")
                st.write(f"**Modelo:** {row['Modelo']}")
                st.write(f"**Ano:** {row['Ano']}")
                st.write(f"**Cor:** {row['Cor']}")
                st.write(f"**Valor:** R$ {row['VALOR']:,.2f}")

        except Exception:
            st.warning("Base de dados ainda não carregada")

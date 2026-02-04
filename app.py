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
# ESTILO VISUAL
# ===============================
st.markdown("""
<style>
.stApp {
    background-color: #1e3d7d;
    color: white;
}
.stButton>button {
    background-color: #f1d064;
    color: #1e3d7d;
    font-weight: bold;
    border-radius: 6px;
    width: 100%;
}
h1, h3 {
    color: white;
}
label {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# TÍTULO
# ===============================
st.title("🚗 Estoque Unidas")

# ===============================
# CAMINHO DO ARQUIVO
# ===============================
CAMINHO_ARQUIVO = "data/estoque.xlsx"

# =====================================================
# 🔐 ÁREA DO ADMINISTRADOR
# =====================================================
with st.expander("🔐 Área do Administrador"):
    senha = st.text_input("Senha do administrador", type="password")

    if senha:
        if senha == st.secrets["ADMIN_PASSWORD"]:
            st.success("Acesso liberado")

            arquivo_admin = st.file_uploader(
                "Enviar nova planilha de estoque",
                type=["xlsx"]
            )

            if arquivo_admin is not None:
                os.makedirs("data", exist_ok=True)
                with open(CAMINHO_ARQUIVO, "wb") as f:
                    f.write(arquivo_admin.getbuffer())
                st.success("Planilha atualizada com sucesso!")
        else:
            st.error("Senha incorreta")

# =====================================================
# 📊 LEITURA DA PLANILHA
# =====================================================
if not os.path.exists(CAMINHO_ARQUIVO):
    st.warning("Nenhuma planilha carregada ainda.")
    st.stop()

try:
    df = pd.read_excel(CAMINHO_ARQUIVO)
except Exception:
    st.error("Erro ao ler a planilha.")
    st.stop()

# ===============================
# TRATAMENTO DOS DADOS
# ===============================
df.columns = df.columns.str.strip()
df['Placa'] = df['Placa'].astype(str).str.strip().str.upper()

# ===============================
# CONSULTA
# ===============================
st.subheader("CONSULTAR VEÍCULO POR PLACA")
placa_input = st.text_input("Digite a placa (ex: ABC1D23)").upper().strip()

if st.button("PESQUISAR"):
    if placa_input == "":
        st.warning("Digite uma placa.")
    else:
        resultado = df[df['Placa'] == placa_input]

        if not resultado.empty:
            row = resultado.iloc[0]

            st.markdown("---")
            st.write(f"**Placa:** {row['Placa']}")
            st.write(f"**Modelo:** {row['Modelo']}")
            st.write(f"**Cor:** {row['Cor']}")
            st.write(f"**Ano:** {row['Ano']}")
            st.write(f"**KM:** {row['KM']}")

            fipe = row['Valor FIPE']
            if isinstance(fipe, (int, float)):
                st.write(f"**Valor FIPE:** R$ {fipe:,.2f}")
            else:
                st.write(f"**Valor FIPE:** {fipe}")

            valor = row['VALOR']
            if isinstance(valor, (int, float)):
                st.write(f"**Valor:** R$ {valor:,.2f}")
            else:
                st.write(f"**Valor:** {valor}")

            st.write(f"**Margem:** {row['MARGEM']}")
        else:
            st.error("Placa não encontrada.")

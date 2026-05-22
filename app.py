import streamlit as st
import pandas as pd
import os
import streamlit.components.v1 as components

# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================
st.set_page_config(
    page_title="Estoque Unidas",
    page_icon="🚗",
    layout="centered"
)

# ==============================
# ESTILO (FONTES E CORES)
# ==============================
st.markdown("""
<style>
.stApp { background-color: #2b59b4; color: white; }

p, span { font-size: 20px; }

h3 { font-size: 24px; color: white; }

input { font-size: 20px !important; }

.stButton > button {
    background-color: #f1d064;
    color: #1e3d7d;
    font-weight: bold;
    font-size: 18px;
    width: 100%;
    border-radius: 6px;
}

.titulo-principal {
    font-size: 42px;
    font-weight: 800;
    color: white;
    margin-bottom: 20px;
}

.label-placa {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# DETECTA MODO ADMIN (?admin=1)
# ==============================
modo_admin = st.query_params.get("admin") == "1"

# ==============================
# ÁREA ADMIN
# ==============================
if modo_admin:
    st.markdown(
        "<div class='titulo-principal'>🔐 Área do Administrador</div>",
        unsafe_allow_html=True
    )

    if "admin" not in st.secrets:
        st.error("Secrets de administrador não configurado.")
        st.stop()

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if (
            usuario == st.secrets["admin"].get("user")
            and senha == st.secrets["admin"].get("password")
        ):
            st.session_state["admin_logado"] = True
        else:
            st.error("Usuário ou senha inválidos")

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
st.markdown(
    "<div class='titulo-principal'>🚗 Estoque Unidas</div>",
    unsafe_allow_html=True
)

ARQUIVO = "data/estoque.xlsx"

if not os.path.exists(ARQUIVO):
    st.error("Base de dados indisponível. Contate o administrador.")
    st.stop()

df = pd.read_excel(ARQUIVO)

# 🔧 PADRONIZA COLUNAS
df.columns = df.columns.str.strip()
df.columns = df.columns.str.upper()

# 🔧 Corrige nome FIPE automaticamente
if "FIPE" in df.columns:
    df.rename(columns={"FIPE": "VALOR FIPE"}, inplace=True)

if "PLACA" not in df.columns:
    st.error("A planilha precisa ter a coluna 'Placa'.")
    st.stop()

df["PLACA"] = df["PLACA"].astype(str).str.upper().str.strip()

st.markdown(
    "<div class='label-placa'>Digite a placa do veículo</div>",
    unsafe_allow_html=True
)

placa = st.text_input("Ex: ABC1D23").upper().strip()

if st.button("PESQUISAR"):
    resultado = df[df["PLACA"] == placa]

    if resultado.empty:
        st.error("Placa não encontrada")
    else:
        row = resultado.iloc[0]
        st.markdown("---")

        colunas_exibir = [
            "PLACA",
            "MODELO",
            "ANO",
            "COR",
            "KM",
            "VALOR FIPE",
            "VALOR",
            "MARGEM"
        ]

        for col in colunas_exibir:
            if col in df.columns:
                valor = row[col]

                if col in ["VALOR", "VALOR FIPE"] and isinstance(valor, (int, float)):
                    valor = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

                st.write(f"**{col.title()}:** {valor}")

        # ==============================
        # TEXTO PARA COPIAR
        # ==============================
        texto_copia = ""

        campos_copia = [
            "MODELO",
            "ANO",
            "COR",
            "KM",
            "VALOR FIPE",
            "VALOR",
            "MARGEM"
        ]

        for col in campos_copia:
            if col in df.columns:
                valor = row[col]

                if col in ["VALOR", "VALOR FIPE"] and isinstance(valor, (int, float)):
                    valor = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

                texto_copia += f"{col.title()}: {valor}\n"

        # ==============================
        # BOTÃO DE COPIAR
        # ==============================
        botao_copiar = f"""
        <textarea id="texto" style="position:absolute; left:-9999px;">
{texto_copia}
        </textarea>

        <button onclick="copiarTexto()" style="
            background-color:#f1d064;
            color:#1e3d7d;
            font-weight:bold;
            font-size:18px;
            width:100%;
            border:none;
            border-radius:6px;
            padding:10px;
        ">
        COPIAR
        </button>

        <script>
        function copiarTexto() {{
            var copyText = document.getElementById("texto");
            copyText.select();
            copyText.setSelectionRange(0, 99999);
            document.execCommand("copy");
            alert("Copiado com sucesso!");
        }}
        </script>
        """

        components.html(botao_copiar, height=100)

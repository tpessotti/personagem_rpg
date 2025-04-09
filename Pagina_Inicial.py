import streamlit as st
from estilo import aplicar_estilo_lsbc
import json
from dados_sistema import DadosSistema

st.set_page_config(page_title="Criador de Personagem LSBC", layout="wide")
aplicar_estilo_lsbc()
ds = DadosSistema()

st.title("🧭 Criador de Personagem LSBC")
st.subheader("Bem-vindo ao Criador de Personagens para a campanha *Lost Secrets of the Brazilian Coast*")

# 🛡️ Garante que o personagem e atributos estejam inicializados
if "personagem" not in st.session_state:
    st.session_state.personagem = {}

if "classes" not in st.session_state.personagem:
    st.session_state.personagem["classes"] = []

ds.inicializar_personagem()

st.text("""
Este criador foi feito para te ajudar a desenvolver personagens de forma modular e imersiva dentro do universo **LSBC**.

🧾 Ao longo do processo, você poderá definir:
- Informações básicas do seu personagem
- Classe, origem e etnia
- Atributos e habilidades
- Equipamentos iniciais
- E no final, exportar uma ficha pronta para jogar

Use o menu lateral esquerdo (ou superior em mobile) para navegar pelas etapas.
""")

with st.sidebar:
    st.markdown("## 📁 Importar")
    # Importar personagem
    arquivo_importado = st.file_uploader("📥 Importar Personagem (.json)", type=["json"])
    if arquivo_importado:
        try:
            personagem_importado = json.load(arquivo_importado)
            st.session_state.personagem = personagem_importado
            st.success("Personagem importado com sucesso!")
            st.rerun()
            st.stop()
        except Exception as e:
            st.error(f"Erro ao importar JSON: {e}")

st.info("👈 Comece selecionando a aba **Informações Gerais** no menu à esquerda.")

st.markdown("---")

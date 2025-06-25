import streamlit as st
from dados_sistema import DadosSistema
from estilo import aplicar_estilo_lsbc

# ====== Configuração Inicial ======
st.set_page_config(page_title="→ Informações Gerais", layout="wide")
aplicar_estilo_lsbc()
ds = DadosSistema()

# ====== Título da Página ======
st.markdown("# 🧭 Informações Gerais")

# ====== Inicialização do personagem ======
if "personagem" not in st.session_state:
    st.session_state.personagem = ds.inicializar_personagem()
    
personagem = st.session_state.personagem

# ====== Nome do Jogador e Personagem ======
st.markdown("### Identidade")
personagem["nome_jogador"] = st.text_input("Nome do Jogador", value=personagem.get("nome_jogador", ""))
personagem["nome"] = st.text_input("Nome do Personagem", value=personagem.get("nome", ""))

# ====== Idade e Altura ======
st.markdown("### Aparência Física")
col1, col2 = st.columns(2)
with col1:
    personagem["idade"] = st.number_input("Idade", min_value=0, max_value=120, step=1, value=personagem.get("idade", 18))
with col2:
    personagem["altura"] = st.number_input("Altura (cm)", min_value=100, max_value=250, value=personagem.get("altura", 170))

# ====== Gênero e Peso ======
col3, col4 = st.columns(2)
with col3:
    genero_opcoes = ["Masculino", "Feminino", "Outro", "Prefiro não dizer"]
    genero = st.selectbox("Gênero", genero_opcoes, placeholder = "Choose an option")
    personagem["genero"] = genero
    personagem["genero_idx"] = genero_opcoes.index(genero)
with col4:
    personagem["peso"] = st.number_input("Peso (kg)", min_value=30, max_value=300, value=personagem.get("peso", 70))

# ====== Etnia ======
st.markdown("### Contexto Cultural")
etnias = [
    "Africanos", "Árabes", "Asiáticos", "Caribenhos", "Europeus do Norte",
    "Latinos Europeus", "Indígenas da América", "Eslavos",
    "Latino-Americanos", "Norte-Americanos"
]
etnia = st.selectbox("Etnia", etnias, index=personagem.get("etnia_idx", 0))
personagem["etnia"] = etnia
personagem["etnia_idx"] = etnias.index(etnia)

# ====== Origem e História ======
personagem["origem"] = st.text_input("Local de nascimento ou origem", value=personagem.get("origem", ""))
personagem["historia"] = st.text_area("História resumida", value=personagem.get("historia", ""))

# ====== Imagem ======
st.markdown("### Imagem do Personagem")
# Inicializa a variável se necessário
if "abrir_modal_imagem" not in st.session_state:
    st.session_state.abrir_modal_imagem = False

# Botão para abrir o "modal"
if st.button("🖼️ Alterar imagem do personagem"):
    st.session_state.abrir_modal_imagem = True

# Simula o modal para alterar imagem
if st.session_state.abrir_modal_imagem:
    st.markdown("#### 🔗 Inserir link da imagem do personagem")
    nova_url = st.text_input("Cole o link da imagem abaixo", value=personagem.get("imagem", ""))

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Confirmar"):
            personagem["imagem"] = nova_url if nova_url.strip() else None
            st.session_state.abrir_modal_imagem = False
            st.success("Imagem atualizada com sucesso!")

    with col2:
        if st.button("❌ Cancelar"):
            st.session_state.abrir_modal_imagem = False

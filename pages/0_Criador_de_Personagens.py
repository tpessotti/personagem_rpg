import streamlit as st
from estilo import aplicar_estilo_lsbc
import json
from dados_sistema import DadosSistema
from datetime import datetime
from auth import carregar_personagens_usuario, excluir_personagem, salvar_personagem

# ========== Inicialização ==========
aplicar_estilo_lsbc()
ds = DadosSistema()

st.title("🧭 Criador de Personagem LSBC")
st.subheader("Bem-vindo ao Criador de Personagens para a campanha *Lost Secrets of the Brazilian Coast*")
with st.sidebar:
    st.text(" ")

# Garante que o personagem esteja inicializado
if "personagem" not in st.session_state:
    st.session_state.personagem = {}

if "classes" not in st.session_state.personagem:
    st.session_state.personagem["classes"] = []

if "adicionando_personagem" not in st.session_state:
    st.session_state.adicionando_personagem = False

# ========== Login necessário ==========
if "usuario" not in st.session_state:
    st.warning("⚠️ Faça login para acessar seus personagens salvos.")
    login = st.button("Login", use_container_width=True)
    if login:
        st.switch_page("pages/8_login.py")
    st.stop()

# ========== Carregamento de personagens ==========
st.markdown("# 📂 Meus Personages")
personagens = carregar_personagens_usuario(st.session_state.usuario)

# Formatação da apresentação
def formatar_personagem(nome, dados):
    classes = dados.get("classes", [])
    nivel_total = len(classes)

    distribuicao = {}
    for entrada in classes:
        cls = entrada.get("classe", "Indefinida")
        distribuicao[cls] = distribuicao.get(cls, 0) + 1

    partes = [f"{cls} {lvl}" for cls, lvl in distribuicao.items()]
    distrib_texto = " / ".join(partes)

    # Data de última edição
    data_raw = dados.get("ultima_edicao")
    if data_raw:
        try:
            data = datetime.fromisoformat(data_raw)
            data_formatada = data.strftime("%d/%m/%Y às %H:%M")
        except:
            data_formatada = "Data inválida"
    else:
        data_formatada = "Data desconhecida"

    return f"🏴‍☠️ {nome} | Nível Total: {nivel_total} | {distrib_texto} | Última edição: {data_formatada}"

if personagens:
    opcoes_formatadas = [
        formatar_personagem(nome, dados) for nome, dados in personagens.items()
    ]
    nome_para_dado = dict(zip(opcoes_formatadas, personagens.keys()))
    escolhido_formatado = st.selectbox("Escolha seu personagem:", opcoes_formatadas)
    escolhido = nome_para_dado.get(escolhido_formatado)

    # ===== Ações de personagem selecionado =====
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        with st.expander("➕ Adicionar Novo Personagem", expanded=False):
            st.markdown("Escolha como deseja criar seu personagem:")

            opcao = st.radio("Modo de Criação:", ["📦 Novo Personagem", "📥 Importar .json"], horizontal=True, key="modo_criacao")

            if opcao == "📦 Novo Personagem":
                if st.button("🧪 Iniciar Criação de Personagem", use_container_width=True):
                    st.session_state.personagem = ds.inicializar_personagem()
                    st.success("Novo personagem criado!")
                    st.switch_page("pages/1_Informações_Gerais.py")

            elif opcao == "📥 Importar .json":
                arquivo_importado = st.file_uploader("Selecione o arquivo JSON", type=["json"], key="import_json_novo")
                if arquivo_importado:
                    try:
                        personagem_importado = json.load(arquivo_importado)
                        personagem_importado["ultima_edicao"] = datetime.now().isoformat()
                        st.session_state.personagem = personagem_importado
                        st.success("Personagem importado com sucesso!")
                        salvar_personagem(st.session_state.usuario, escolhido, st.session_state.personagem)
                        st.switch_page("pages/7_Resumo.py")
                    except Exception as e:
                        st.error(f"Erro ao importar: {e}")

    with col2:
        if st.button("🔄 Carregar", use_container_width=True):
            st.session_state.personagem = personagens.get(escolhido, ds.inicializar_personagem())
            st.success(f"{escolhido} carregado com sucesso!")
            st.switch_page("pages/7_Resumo.py")

    with col3:
        if st.button("🗑️ Excluir Personagem", use_container_width=True):
            excluir_personagem(st.session_state.usuario, escolhido)
            st.success(f"{escolhido} foi excluído.")
            st.rerun()

    if st.session_state.adicionando_personagem:
        st.markdown("### ➕ Novo Personagem")

        opcao = st.radio("Como deseja criar?", ["📦 Novo Personagem", "📥 Importar .json"], horizontal=True)

        if opcao == "📦 Novo Personagem":
            if st.button("Criar Agora"):
                st.session_state.personagem = ds.inicializar_personagem()
                st.session_state.adicionando_personagem = False
                st.success("Novo personagem criado!")
                st.switch_page("pages/1_Informações_Gerais.py")

        elif opcao == "📥 Importar .json":
            arquivo_importado = st.file_uploader("Selecione o arquivo", type=["json"], key="import_json_novo")
            if arquivo_importado:
                try:
                    personagem_importado = json.load(arquivo_importado)
                    st.session_state.personagem = personagem_importado
                    st.session_state.adicionando_personagem = False
                    st.success("Personagem importado com sucesso!")
                    st.switch_page("pages/1_Informações_Gerais.py")
                except Exception as e:
                    st.error(f"Erro ao importar: {e}")

        if st.button("❌ Cancelar"):
            st.session_state.adicionando_personagem = False

else:
    st.markdown("Você ainda não tem personagens salvos.")

    st.markdown("### ➕ Primeiro Personagem")

    opcao = st.radio("Como deseja criar?", ["📦 Novo Personagem", "📥 Importar .json"], horizontal=True)

    if opcao == "📦 Novo Personagem":
        if st.button("🧪 Iniciar Criação de Personagem"):
            st.session_state.personagem = ds.inicializar_personagem()
            st.session_state.adicionando_personagem = False
            st.success("Novo personagem criado!")
            st.switch_page("pages/1_Informações_Gerais.py")

    elif opcao == "📥 Importar .json":
        arquivo_importado = st.file_uploader("Selecione o arquivo", type=["json"], key="import_json_novo")
        if arquivo_importado:
            try:
                personagem_importado = json.load(arquivo_importado)
                st.session_state.personagem = personagem_importado
                st.session_state.adicionando_personagem = False
                st.success("Personagem importado com sucesso!")
                st.switch_page("pages/1_Informações_Gerais.py")
            except Exception as e:
                st.error(f"Erro ao importar: {e}")

    if st.button("❌ Cancelar"):
        st.session_state.adicionando_personagem = False

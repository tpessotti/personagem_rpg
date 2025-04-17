import streamlit as st
from auth import carregar_usuarios, salvar_personagem, excluir_personagem
from estilo import aplicar_estilo_lsbc
import json
from datetime import datetime

ADMINS = ["tpessotti"]

def usuario_e_admin():
    return "usuario" in st.session_state and st.session_state.usuario in ADMINS

aplicar_estilo_lsbc()

if not usuario_e_admin():
    st.error("Acesso restrito. Somente administradores.")
    st.stop()

st.title("🛠️ Painel Administrativo LSBC")

# 🔎 Selecionar usuário
usuarios = carregar_usuarios()
usuario_alvo = st.selectbox("👤 Usuário alvo:", sorted(usuarios.keys()))
personagens = usuarios[usuario_alvo].get("personagens", {})

# 📁 Editar personagem existente
st.markdown("### 📂 Personagens existentes")

if personagens:
    personagem_nome = st.radio("Selecionar personagem:", sorted(personagens.keys()))
    personagem = personagens[personagem_nome]

    st.markdown(f"### ⚙️ Ações para o personagem: **{personagem_nome}**")

    col1, col2, col3 = st.columns(3)

    # 📝 COLUNA 1 — Editar personagem
    with col1:
        with st.expander("✏️ Editar personagem", expanded=False):
            novo_nome = st.text_input("Novo nome do personagem", value=personagem.get("nome", personagem_nome), key="editar_nome")

            # Editor de texto JSON manual
            import json
            personagem_json = json.dumps(personagem, indent=4, ensure_ascii=False)
            personagem_editado = st.text_area("Editar JSON do personagem (avançado)", value=personagem_json, height=300, key="json_editor")

            # Botão para salvar alterações manuais
            if st.button("Salvar Alterações", key="botao_salvar"):
                try:
                    personagem_atualizado = json.loads(personagem_editado)
                    personagem_atualizado["nome"] = novo_nome
                    salvar_personagem(usuario_alvo, novo_nome, personagem_atualizado)
                    st.success("Personagem salvo com sucesso!")
                except json.JSONDecodeError as e:
                    st.error(f"Erro no JSON: {e}")


    # 🗑️ COLUNA 3 — Excluir personagem
    with col3:
        with st.expander("🗑️ Excluir personagem", expanded=False):
            st.warning("⚠️ Esta ação não pode ser desfeita.")
            st.markdown(f"**Nome do personagem:** {personagem_nome}")
            st.markdown(f"**Última edição:** {personagem.get('ultima_edicao', 'N/A')}")

            if st.button("Confirmar Exclusão", key="botao_excluir"):
                excluir_personagem(usuario_alvo, personagem_nome)
                st.success("Personagem excluído com sucesso.")
                st.experimental_rerun()

    # 🔍 COLUNA 2 — Visualizar e exportar personagem
    with col2:
        with st.expander("📋 Exportar", expanded=False):
            st.markdown("#### 📄 Visualização da ficha:")
            import json
            personagem_bytes = json.dumps(personagem, indent=4).encode("utf-8")
            st.download_button(
                label="📥 Exportar como JSON",
                data=personagem_bytes,
                file_name=f"{personagem_nome}.json",
                mime="application/json"
            )



# 📥 Importar personagem por JSON
st.markdown("### 📥 Importar novo personagem (.json)")
col_nome, col_json = st.columns([2, 2])

with col_json:
    arquivo = st.file_uploader("Selecionar arquivo JSON", type=["json"], key="json_import")

with col_nome:
    nome_importado_manual = st.text_input("Nome do novo personagem", key="nome_importado")

if st.button("✅ Confirmar importação", use_container_width=True):
    if not arquivo:
        st.warning("⚠️ Por favor, selecione um arquivo JSON para importar.")
        st.stop()
    try:
        personagem_importado = json.load(arquivo)
        personagem_importado["nome"] = nome_importado_manual
        personagem_importado["ultima_edicao"] = datetime.now().isoformat()

        salvar_personagem(usuario_alvo, nome_importado_manual, personagem_importado)

        # ✅ Limpar campos após sucesso
        st.success(f"Personagem '{nome_importado_manual}' importado com sucesso!")

        # Limpar campos: força a reinicialização dos widgets
        st.session_state.pop("json_import", None)
        st.session_state.pop("nome_importado", None)
        st.rerun()

    except Exception as e:
        st.error(f"Erro ao importar personagem: {e}")

elif arquivo and not nome_importado_manual:
    st.warning("Por favor, defina um nome para o personagem antes de confirmar a importação.")


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

st.markdown("### 🧙 Visualizar personagens em cards")

# Junta todos os personagens de todos os usuários
todos_personagens = {}
for usuario, dados in usuarios.items():
    for nome, ficha in dados.get("personagens", {}).items():
        chave = f"{usuario} | {nome}"
        todos_personagens[chave] = ficha

# Seleção múltipla
nomes_disponiveis = sorted(todos_personagens.keys())
selecionados = st.multiselect("Selecione personagens para visualizar:", nomes_disponiveis)

# Layout em colunas
if selecionados:
    for i in range(0, len(selecionados), 4):
        cols = st.columns(4)
        for j, nome in enumerate(selecionados[i:i+4]):
            with cols[j]:
                p = todos_personagens[nome]
                ficha = p.get("atributos_finais", {})
                status = p.get("status_gerais", {})
                ca = status.get("ca", "❓")
                hp = status.get("hp", "❓")
                img = p.get("imagem", "https://imebehavioralhealth.com/wp-content/uploads/2021/10/user-icon-placeholder-1.png")  # imagem padrão

                # Classes e nível
                nivel_total = sum(1 for _ in p.get("classes", []))
                classes = {}
                for c in p.get("classes", []):
                    classe = c.get("classe", "???")
                    classes[classe] = classes.get(classe, 0) + 1
                classe_txt = " / ".join([f"{k} {v}" for k, v in classes.items()])
                
                # Exibe os atributos principais
                atributos_exibir = ["Força", "Destreza", "Constituição", "Inteligência", "Sabedoria", "Carisma"]
                # Cabeçalhos
                cabecalhos = "".join([
                    f"<th style='padding: 0.1rem 0.1rem; font-size: 0.75rem; text-align: center;'>{a[:3]}</th>"
                    for a in atributos_exibir
                ])

                # Valores com bônus
                valores = "".join([
                    f"<td style='padding: 0.1rem 0.1rem; font-size: 0.90rem; text-align: center;'>"
                    f"{ficha.get(a, {}).get('final', 0):02d} "
                    f"({(ficha.get(a, {}).get('final', 10) - 10) // 2:+d})</td>"
                    for a in atributos_exibir
                ])

                # Tabela completa
                bonus_txt = f"""
                <table style='margin: auto;'>
                    <tr>{cabecalhos}</tr>
                    <tr>{valores}</tr>
                </table>
                """

                # Card
                st.markdown(f"""
                    <div style='
                        position: relative;
                        border: 1px solid #ccc;
                        border-radius: 10px;
                        overflow: hidden;
                        background: #fefefe;
                        width: 100%;
                        height: 100%;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
                        font-family: Georgia, serif;
                        display: flex;
                        flex-direction: column;
                        justify-content: start;
                    '>
                        <div style='position: absolute; top: 5px; left: 10px; font-weight: bold; background-color: rgba(255, 255, 255, 0.8); border-radius: 6px; padding: 2px 8px;'>🛡️{ca}</div>
                        <div style='position: absolute; top: 5px; right: 10px; font-weight: bold; background-color: rgba(255, 255, 255, 0.8); border-radius: 6px; padding: 2px 8px;'>❤️{hp}</div>
                        <div style='
                            width: 100%;
                            aspect-ratio: 1 / 1;
                            overflow: hidden;
                            border-bottom: 1px solid #ccc;
                        '>
                            <img src="{img}" style='
                                width: 100%;
                                height: 100%;
                                object-fit: cover;
                                object-position: center top;
                                display: block;
                            ' />
                        </div>
                        <div style='padding: 0.0rem;text-align: center;'>
                            <h4 style='margin: 0;'>| {nivel_total} | {p.get("nome", nome)}</h4>
                            <p style='margin: 0.2rem 0;'>🏴‍☠️ {classe_txt}</p>
                            <h2 style='margin-top: 0.4rem;'>{bonus_txt}</h2>
                """, unsafe_allow_html=True)
                
                st.markdown(f"", unsafe_allow_html=True)
                st.markdown("</div></div>", unsafe_allow_html=True)

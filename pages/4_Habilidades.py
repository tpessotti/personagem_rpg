import streamlit as st
from estilo import aplicar_estilo_lsbc
from dados_sistema import DadosSistema

st.set_page_config(page_title="Habilidades", layout="wide")
aplicar_estilo_lsbc()
st.markdown("# 🧭 Escolha de Proficiências")
dados = DadosSistema()

# ===== Inicialização =====
if "personagem" not in st.session_state:
    st.session_state.personagem = dados.inicializar_personagem()

# Inicialização de habilidades (se necessário)
if "habilidades" not in st.session_state.personagem or not st.session_state.personagem["habilidades"]:
    st.session_state.personagem["habilidades"] = {hab: 0 for hab in dados.habilidades}

# Inicialização de atributos finais (se necessário)
if "atributos_finais" not in st.session_state.personagem:
    st.session_state.personagem["atributos_finais"] = {
        attr: {"final": 8} for attr in dados.atributos_base
    }

# ===== Resetar Proeficiências =====
if st.button("🔄 Resetar Proeficiências"):
    for k in st.session_state.personagem["habilidades"]:
        st.session_state.personagem["habilidades"][k] = 0
    st.rerun()

# ===== Proficiências Selecionadas =====
MAX_PROFICIENCIAS = 4
proficiencias_usadas = sum(st.session_state.personagem["habilidades"].values())
st.markdown(f"**Proficiências selecionadas:** {proficiencias_usadas} / {MAX_PROFICIENCIAS}")

# ===== Blocos de Habilidades em Grupos =====
for linha in [dados.habilidades_grupos[:2], dados.habilidades_grupos[2:]]:
    cols = st.columns(2)
    for col, (titulo, habilidades) in zip(cols, linha):
        with col:
            st.subheader(titulo)
            for habilidade in habilidades:
                atributo = dados.mapa_atributos[habilidade]
                valor_attr = st.session_state.personagem["atributos_finais"].get(atributo, {}).get("final", 8)
                modificador = (valor_attr - 10) // 2
                prof = st.session_state.personagem["habilidades"][habilidade]
                total = modificador + prof  # prof = 1 ou 2

                icone = "🔶" if prof == 2 else "🔸" if prof == 1 else ""

                c1, c2, c3 = st.columns([5, 1, 1])
                with c1:
                    st.markdown(
                        f"<span title='{dados.descricao_habilidades[habilidade]}'><b>{habilidade}</b> <i>({atributo})</i> {icone}</span>",
                        unsafe_allow_html=True
                    )
                with c2:
                    st.markdown(f"<div style='text-align: center; font-weight: bold;'> {total:+} </div>", unsafe_allow_html=True)
                with c3:
                    if st.button("🔸", key=f"mais_{habilidade}") and prof < 2 and proficiencias_usadas < MAX_PROFICIENCIAS:
                        st.session_state.personagem["habilidades"][habilidade] += 1
                        st.rerun()

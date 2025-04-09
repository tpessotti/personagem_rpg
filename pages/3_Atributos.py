import streamlit as st
from estilo import aplicar_estilo_lsbc
from dados_sistema import DadosSistema

# Configuração de página e estilo
st.set_page_config(page_title="Atributos", layout="wide")
aplicar_estilo_lsbc()
st.markdown("# 🧭 Atributos")
dados = DadosSistema()

# Inicialização
if "personagem" not in st.session_state:
    st.session_state.personagem = dados.inicializar_personagem()

if "bonus_manual" not in st.session_state:
    st.session_state.bonus_manual = {"+1": None, "+2": None}

personagem = st.session_state.personagem
classes = st.session_state.personagem.get("classes", [])

# Se ainda não houver atributos_finais (ex: personagem novo), inicializa com base = 8
if "atributos_finais" not in personagem:
    personagem["atributos_finais"] = {
        attr: {"base": 8, "bonus_classe": 0, "bonus_manual": 0, "final": 8}
        for attr in dados.atributos_base
    }

# Constantes
TOTAL_PONTOS = 75
VALOR_MINIMO = 8
VALOR_MAXIMO = 15
atributos_base = dados.atributos_base
bonus_classe = dados.calcular_bonus_classe(personagem, classes)
pontos_usados = sum(personagem["atributos_finais"][attr]["base"] for attr in atributos_base)
pontos_restantes = TOTAL_PONTOS - pontos_usados

# Interface
st.markdown(f"**Pontos usados:** {pontos_usados} / {TOTAL_PONTOS} &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp; **Restantes:** {pontos_restantes}")

for attr in atributos_base:
    base = personagem["atributos_finais"][attr]["base"]

    bonus_manual = (
        (1 if st.session_state.bonus_manual["+1"] == attr else 0)
        + (2 if st.session_state.bonus_manual["+2"] == attr else 0)
    )
    bonus_total = bonus_manual + bonus_classe.get(attr, 0)
    valor_final = base + bonus_total

    col1, col2, col3, col4, col5 = st.columns([1.5, 1, 1, 1, 1.5])
    with col1:
        st.markdown(f"**{attr}**")

    with col2:
        if st.button("🔽", key=f"menos_{attr}") and base > VALOR_MINIMO:
            personagem["atributos_finais"][attr]["base"] -= 1
            st.rerun()

    with col3:
        st.markdown(
            f"<div style='text-align:center; font-size:24px;'><strong>{valor_final}</strong></div>",
            unsafe_allow_html=True
        )

    with col4:
        if st.button("🔼", key=f"mais_{attr}") and base < VALOR_MAXIMO and pontos_restantes > 0:
            personagem["atributos_finais"][attr]["base"] += 1
            st.rerun()

    with col5:
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            ativar = st.session_state.bonus_manual["+1"] == attr
            novo_valor = st.checkbox("+1", value=ativar, key=f"b1_{attr}")
            if novo_valor != ativar:
                st.session_state.bonus_manual["+1"] = attr if novo_valor else None
                st.rerun()

        with col_b2:
            ativar2 = st.session_state.bonus_manual["+2"] == attr
            novo_valor2 = st.checkbox("+2", value=ativar2, key=f"b2_{attr}")
            if novo_valor2 != ativar2:
                st.session_state.bonus_manual["+2"] = attr if novo_valor2 else None
                st.rerun()

# Atualiza os atributos finais com base nos bônus atuais
st.session_state.personagem = dados.calcular_atributos_finais(
    st.session_state.personagem,
    bonus_classe,
    st.session_state.bonus_manual
)

st.divider()
st.markdown("**Nota:** O valor final inclui bônus de classe e bônus manuais. Cada bônus só pode ser atribuído uma vez e a atributos distintos.")
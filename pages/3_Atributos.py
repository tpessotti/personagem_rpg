import streamlit as st
from estilo import aplicar_estilo_lsbc
from dados_sistema import DadosSistema

# Configuração de página e estilo
aplicar_estilo_lsbc()
st.markdown("# 🧭 Atributos")
ds = DadosSistema()

# Inicialização
if "personagem" not in st.session_state:
    st.session_state.personagem = ds.inicializar_personagem()

personagem = st.session_state.personagem
classes = st.session_state.personagem.get("classes", [])

# Se ainda não houver atributos_finais (ex: personagem novo), inicializa com base = 8
if "atributos_finais" not in personagem:
    personagem["atributos_finais"] = {
        attr: {"base": 8, "bonus_classe": 0, "bonus_manual": 0, "final": 8}
        for attr in ds.atributos_base
    }

# Constantes
TOTAL_PONTOS = 75
VALOR_MINIMO = 8
VALOR_MAXIMO = 16
atributos_base = ds.atributos_base
bonus_classe = ds.calcular_bonus_classe(personagem, classes)
pontos_usados = sum(personagem["atributos_finais"][attr]["base"] for attr in atributos_base)
pontos_restantes = TOTAL_PONTOS - pontos_usados

# Interface
st.markdown(f"**Pontos usados:** {pontos_usados} / {TOTAL_PONTOS} &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp; **Restantes:** {pontos_restantes}")

for attr in atributos_base:
    base = personagem["atributos_finais"][attr]["base"]

    bonus_manual = personagem["atributos_finais"][attr]["bonus_manual"]
    bonus_total = bonus_manual + bonus_classe.get(attr, 0)
    valor_final = base + bonus_total

    col1, col2, col3, col4, col5 = st.columns([1, 0.1, 0.2, 0.1, 1])
    with col1:
        st.markdown(f"<div style='text-align: left;'><strong>{attr}</strong></div>", unsafe_allow_html=True)

    with col2:
        if st.button("▼", key=f"menos_{attr}", use_container_width=True) and base > VALOR_MINIMO:
            personagem["atributos_finais"][attr]["base"] -= 1
            st.rerun()
        
    with col3:
        st.markdown(
            f"<div style='text-align:center; font-size:24px;'><strong>{valor_final}</strong></div>",
            unsafe_allow_html=True
        )

    with col4:
        if st.button("▲", key=f"mais_{attr}", use_container_width=True) and base < VALOR_MAXIMO and pontos_restantes > 0:
            personagem["atributos_finais"][attr]["base"] += 1
            st.rerun()

    with col5:
        bonus_manual = personagem["atributos_finais"][attr].get("bonus_manual", 0)

        # Identificar quem já tem +1 e +2
        outro_com_mais1 = None
        outro_com_mais2 = None
        for nome_attr, dados in personagem["atributos_finais"].items():
            if nome_attr != attr:
                bm = dados.get("bonus_manual", 0)
                if bm == 1:
                    outro_com_mais1 = nome_attr
                elif bm == 2:
                    outro_com_mais2 = nome_attr

        col_b1, col_b2 = st.columns(2)

        with col_b1:
            novo_b1 = st.checkbox("+1", value=(bonus_manual == 1), key=f"b1_{attr}")
        with col_b2:
            novo_b2 = st.checkbox("+2", value=(bonus_manual == 2), key=f"b2_{attr}")

        # Determina novo bônus com base nos checkboxes
        novo_bonus = 0
        if novo_b2:
            novo_bonus = 2
        elif novo_b1:
            novo_bonus = 1

        if bonus_manual != novo_bonus:
            # Remove +1 de outro atributo, se necessário
            if novo_bonus == 1 and outro_com_mais1:
                personagem["atributos_finais"][outro_com_mais1]["bonus_manual"] = 0

            # Remove +2 de outro atributo, se necessário
            if novo_bonus == 2 and outro_com_mais2:
                personagem["atributos_finais"][outro_com_mais2]["bonus_manual"] = 0

            personagem["atributos_finais"][attr]["bonus_manual"] = novo_bonus
            st.rerun()


# Atualiza os atributos finais com base nos bônus atuais
st.session_state.personagem = ds.calcular_atributos_finais(st.session_state.personagem)
st.divider()
st.markdown("**Nota:** O valor final inclui bônus de classe e bônus manuais. Cada bônus só pode ser atribuído uma vez e a atributos distintos.")
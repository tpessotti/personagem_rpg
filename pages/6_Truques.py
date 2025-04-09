import streamlit as st
from dados_sistema import DadosSistema
from estilo import aplicar_estilo_lsbc

# ====== Configuração da Página ======
st.set_page_config(page_title="Truques e Misticismo", layout="wide")
aplicar_estilo_lsbc()
ds = DadosSistema()
st.markdown("# 🧭 Truques e Misticismo")

# ---------------------- INICIALIZAÇÃO ----------------------
ds = DadosSistema()
truques_disponiveis = ds.truques_disponiveis

# Garantir estrutura do personagem
if "personagem" not in st.session_state:
    st.session_state.personagem = {}

if "misticismo" not in st.session_state.personagem:
    st.session_state.personagem["misticismo"] = {
        "nivel_total": 0,
        "arsenal": [],
        "slots_usados": [0] * 6
    }

misticismo = st.session_state.personagem["misticismo"]

# Verificar nível total
classes = st.session_state.personagem.get("classes", [])
nivel_atual = sum(c.get("nivel", 0) for c in classes)

# Se o nível mudou, resetar arsenal e slots
if misticismo.get("nivel_total", -1) != nivel_atual:
    misticismo["nivel_total"] = nivel_atual
    misticismo["slots_usados"] = [0] * 6
    misticismo["arsenal"] = []

# Tabela de slots por nível
def calcular_slots(nivel):
    if nivel <= 2:
        return [1, 2, 0, 0, 0, 0]
    elif nivel <= 4:
        return [1, 3, 1, 0, 0, 0]
    elif nivel <= 6:
        return [1, 4, 2, 1, 0, 0]
    elif nivel <= 8:
        return [1, 4, 3, 2, 1, 0]
    else:
        return [1, 4, 3, 3, 2, 1]

slots_disponiveis = calcular_slots(nivel_atual)

# ---------------------- INTERFACE ----------------------
col_esq, col_dir = st.columns(2)

# COLUNA ESQUERDA: SLOTS
with col_esq:
    st.subheader("Slots Disponíveis")
    slot_cols = st.columns(2)
    for i in range(6):
        with slot_cols[i % 2]:
            icone = "🔮"
            usados = misticismo["slots_usados"][i]
            total = slots_disponiveis[i]
            texto = f"N{i}: {icone * usados}{'⚪' * (total - usados)}"
            st.markdown(texto)

    if st.button("🔁 Resetar Arsenal"):
        misticismo["arsenal"] = []
        misticismo["slots_usados"] = [0] * 6
        st.rerun()

# COLUNA DIREITA: ARSENAL
with col_dir:
    st.subheader("Arsenal do Personagem")
    if not misticismo["arsenal"]:
        st.info("Nenhum truque selecionado ainda.")
    else:
        for truque in misticismo["arsenal"]:
            st.markdown(f"- Nível {truque['nivel']} | {truque['tipo']} | **{truque['nome']}**")

# ---------------------- FILTROS ----------------------

st.markdown("---")
st.subheader("Buscar Truques")

filtro_nome = st.text_input("Filtrar por nome:")
filtro_tipo = st.selectbox("Filtrar por tipo", ["Todos"] + sorted(set(t["tipo"] for t in truques_disponiveis)))
filtro_nivel = st.selectbox("Filtrar por nível", ["Todos"] + list(range(6)))

# Aplicar filtros
truques_filtrados = []
for truque in truques_disponiveis:
    if filtro_nome and filtro_nome.lower() not in truque["nome"].lower():
        continue
    if filtro_tipo != "Todos" and truque["tipo"] != filtro_tipo:
        continue
    if filtro_nivel != "Todos" and truque["nivel"] != filtro_nivel:
        continue
    truques_filtrados.append(truque)

# ---------------------- TABELA DE TRUQUES ----------------------

st.markdown("---")
st.subheader("Todos os Truques")

if not truques_filtrados:
    st.warning("Nenhum truque encontrado com esses filtros.")
else:
    for t in truques_filtrados:
        with st.container():
            st.markdown(f"**{t['nome']}** (Nível {t['nivel']}) - *{t['tipo']}*")
            st.caption(f"🎯 *{t['efeito']}*")
            st.caption(f"📜 Requisitos: {t['requisitos']}")

            if t in misticismo["arsenal"]:
                st.success("✅ Já adicionado")
            elif misticismo["slots_usados"][t["nivel"]] >= slots_disponiveis[t["nivel"]]:
                st.error("❌ Sem slots disponíveis para este nível")
            else:
                if st.button(f"➕ Adicionar {t['nome']}", key=t["nome"]):
                    misticismo["arsenal"].append(t)
                    misticismo["slots_usados"][t["nivel"]] += 1
                    st.rerun()

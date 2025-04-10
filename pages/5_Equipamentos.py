import streamlit as st
from estilo import aplicar_estilo_lsbc
from dados_sistema import DadosSistema

# ===== Inicialização =====
aplicar_estilo_lsbc()
ds = DadosSistema()
st.markdown("# 🧭 Equipamentos Iniciais")

if "personagem" not in st.session_state:
    st.session_state.personagem = ds.inicializar_personagem()

ds.calcular_status_gerais(st.session_state.personagem)

personagem = st.session_state.personagem
equipamentos = personagem.setdefault("equipamentos", {})

# ===== Classe base =====
classes = personagem.get("classes", [])
if not classes:
    st.error("⚠️ Nenhuma classe foi selecionada.")
    st.stop()

classe_base = classes[0]["classe"]
equipos = ds.equipamento_inicial.get(classe_base, {})
armas_cc = equipos.get("Armas Corpo-a-Corpo", ["—"])
armas_dist = equipos.get("Armas à Distância", ["Nenhuma"])
extras_iniciais = equipos.get("Extras", [])
armaduras = ds.armadura_inicial.get(classe_base, ["Roupas Leves"])

# ===== Inicializar session_state com escolhas anteriores =====
if "equipamentos_confirmados" not in st.session_state:
    st.session_state.equipamentos_confirmados = personagem.get("equipamentos_confirmados", False)

if "arma_cc" not in st.session_state:
    st.session_state.arma_cc = equipamentos.get("arma_cc", armas_cc[0])
if "arma_dist" not in st.session_state:
    st.session_state.arma_dist = equipamentos.get("arma_dist", armas_dist[0])
if "armadura" not in st.session_state:
    st.session_state.armadura = equipamentos.get("armadura", armaduras[0])
if "extras" not in equipamentos:
    equipamentos["extras"] = extras_iniciais.copy()

# ===== Exibição =====
st.markdown(f"## Classe Base: *{classe_base}*")
st.markdown("### Escolhas Iniciais")

col1, col2 = st.columns(2)
with col1:
    arma_cc = st.radio(
        "Arma Corpo-a-Corpo",
        armas_cc,
        index=armas_cc.index(st.session_state.arma_cc),
        disabled=st.session_state.equipamentos_confirmados
    )
    st.session_state.arma_cc = arma_cc

with col2:
    arma_dist = st.radio(
        "Arma à Distância",
        armas_dist,
        index=armas_dist.index(st.session_state.arma_dist),
        disabled=st.session_state.equipamentos_confirmados
    )
    st.session_state.arma_dist = arma_dist

armadura = st.radio(
    "Armadura",
    armaduras,
    index=armaduras.index(st.session_state.armadura),
    disabled=st.session_state.equipamentos_confirmados
)
st.session_state.armadura = armadura

# ===== Confirmação =====
if not st.session_state.equipamentos_confirmados:
    if st.button("✅ Confirmar Equipamentos"):
        st.session_state.equipamentos_confirmados = True
        personagem["equipamentos_confirmados"] = True
        st.success("Equipamentos iniciais confirmados! Eles não poderão mais ser alterados.")
else:
    st.info("✅ Equipamentos já foram confirmados e estão bloqueados.")

# ===== Botão de Reset =====
if st.session_state.equipamentos_confirmados:
    if st.button("🔄 Resetar Equipamentos"):
        st.session_state.equipamentos_confirmados = False
        personagem["equipamentos_confirmados"] = False

        st.session_state.arma_cc = armas_cc[0]
        st.session_state.arma_dist = armas_dist[0]
        st.session_state.armadura = armaduras[0]

        equipamentos["arma_cc"] = armas_cc[0]
        equipamentos["arma_dist"] = armas_dist[0] if armas_dist[0] != "Nenhuma" else None
        equipamentos["armadura"] = armaduras[0]
        equipamentos["extras"] = extras_iniciais.copy()

        st.success("Equipamentos reiniciados. Você pode fazer novas escolhas.")
        st.rerun()

# ===== Salvar escolhas =====
equipamentos["arma_cc"] = st.session_state.arma_cc
equipamentos["arma_dist"] = st.session_state.arma_dist if st.session_state.arma_dist != "Nenhuma" else None
equipamentos["armadura"] = st.session_state.armadura

# ===== Visualização das Estatísticas =====
def mostrar_arma(nome):
    stats = ds.tabela_armas.get(nome)
    if not stats:
        return f"❔ {nome}"
    dano, distancia, propriedades, atributo = stats
    return f"**{nome}**: {dano} | Alcance: {distancia} | {propriedades} | Atributo: {atributo}"

def mostrar_armadura(nome):
    stats = ds.tabela_armaduras.get(nome)
    if not stats:
        return f"❔ {nome}"
    ca, tipo, penalidade, propriedades = stats
    return f"**{nome}**: CA {ca} | {tipo} | Penalidade: {penalidade} | {propriedades}"

st.markdown("### Itens Extras")
for item in equipamentos["extras"]:
    st.markdown(f"- {item}")

# ===== Adicionar Equipamento Extra =====
st.markdown("### ➕ Adicionar Equipamento Extra")

with st.expander("Criar novo equipamento"):
    tipo = st.selectbox("Tipo de Equipamento", ["Item", "Arma", "Armadura"], key="tipo_equip")
    nome = st.text_input("Nome do Equipamento")

    if tipo == "Arma":
        dano = st.text_input("Dano", placeholder="Ex: 1d6")
        alcance = st.text_input("Alcance", placeholder="Ex: 6m")
        propriedades = st.text_input("Propriedades", placeholder="Ex: Leve, Arremessável")
        atributo = st.selectbox("Atributo Usado", ["Força", "Destreza", "Força/Destreza", "—"])

        if st.button("Adicionar Arma"):
            descricao = f"🗡️ {nome} — {dano} | Alcance: {alcance} | {propriedades} | Atributo: {atributo}"
            equipamentos["extras"].append(descricao)
            st.success("Arma adicionada com sucesso!")
            st.rerun()

    elif tipo == "Armadura":
        ca = st.text_input("Classe de Armadura (CA)", placeholder="Ex: 14 + Destreza")
        tipo_arma = st.text_input("Tipo", placeholder="Leve / Média / Pesada")
        penalidade = st.text_input("Penalidade", placeholder="Ex: -1m")
        propriedades = st.text_input("Propriedades", placeholder="Ex: Discreta, Simbólica")

        if st.button("Adicionar Armadura"):
            descricao = f"🛡️ {nome} — CA: {ca} | Tipo: {tipo_arma} | Penalidade: {penalidade} | {propriedades}"
            equipamentos["extras"].append(descricao)
            st.success("Armadura adicionada com sucesso!")
            st.rerun()

    else:  # Item genérico
        descricao = st.text_area("Descrição do Item")
        if st.button("Adicionar Item"):
            item_formatado = f"📦 {nome}: {descricao}" if descricao else f"📦 {nome}"
            equipamentos["extras"].append(item_formatado)
            st.success("Item adicionado com sucesso!")
            st.rerun()

# ===== Estatísticas do Personagem =====
st.markdown("### Estatísticas dos Equipamentos")
st.markdown(f"- {mostrar_arma(st.session_state.arma_cc)}")
if st.session_state.arma_dist and st.session_state.arma_dist != "Nenhuma":
    st.markdown(f"- {mostrar_arma(st.session_state.arma_dist)}")
st.markdown(f"- {mostrar_armadura(st.session_state.armadura)}")

# Atualiza os status
st.session_state.personagem = ds.calcular_status_gerais(st.session_state.personagem)

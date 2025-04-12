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

tabela_armas = ds.tabela_armas.copy()
tabela_armaduras = ds.tabela_armaduras.copy()

# Adiciona personalizadas
tabela_armas.update(personagem.get("armas_personalizadas", {}))
tabela_armaduras.update(personagem.get("armaduras_personalizadas", {}))


# ===== Classe base =====
classes = personagem.get("classes", [])
if not classes:
    st.error("⚠️ Nenhuma classe foi selecionada.")
    st.stop()

classe_base = classes[0]["classe"]
equipos = ds.equipamento_inicial.get(classe_base, {})
armas_cc = equipos.get("Arma Primária", ["Nenhuma"])
armas_dist = equipos.get("Arma Secundária", ["Nenhuma"])
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
if not st.session_state.equipamentos_confirmados:
    st.markdown(f"## Classe Base: *{classe_base}*")
    st.markdown("---")
    st.markdown("### Escolhas Iniciais")

    col1, col2 = st.columns(2)
    with col1:
        arma_cc = st.radio(
            "Arma Primária",
            armas_cc,
            index=armas_cc.index(st.session_state.arma_cc),
            disabled=st.session_state.equipamentos_confirmados
        )
        st.session_state.arma_cc = arma_cc

    with col2:
        arma_dist = st.radio(
            "Arma Secundária",
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
        if st.button("✓ Confirmar Equipamentos"):
            st.session_state.equipamentos_confirmados = True
            personagem["equipamentos_confirmados"] = True
            st.success("Equipamentos iniciais confirmados! Eles não poderão mais ser alterados.")
            st.rerun()

# ===== Botão de Reset =====
if st.session_state.equipamentos_confirmados:
    if st.button("↺ Resetar Equipamentos"):
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
def mostrar_equipamento(titulo, atual, tipo, tabela, chave):
    st.markdown(f"### {titulo}")

    extras = equipamentos.get("extras", [])
    opcoes_disponiveis = [item for item in extras if item in tabela]
    opcoes = [atual] + [item for item in opcoes_disponiveis if item != atual]

    selecionado = st.selectbox("Equipado:", options=opcoes, index=0, key=f"troca_{chave}")

    # Se houver troca de equipamento
    if selecionado != atual:
        # Remove novo item dos extras, se estiver lá
        if selecionado in extras:
            equipamentos["extras"].remove(selecionado)

        # Adiciona o item anterior ao inventário se for diferente
        if atual and atual != "Nenhuma" and atual != selecionado:
            equipamentos["extras"].append(atual)

        # Atualiza o equipamento e o session_state
        equipamentos[chave] = selecionado
        st.session_state[chave] = selecionado

        st.success(f"{titulo} trocado para {selecionado}")
        st.rerun()

    # Exibe estatísticas do item selecionado
    stats = tabela.get(selecionado)
    if stats:
        if tipo == "arma":
            dano, distancia, propriedades, atributo = stats
            st.markdown(f"**{selecionado}**: {dano} | Alcance: {distancia} | {propriedades} | Atributo: {atributo}")
        elif tipo == "armadura":
            ca, tipo_arm, penalidade, propriedades = stats
            st.markdown(f"**{selecionado}**: CA {ca} | {tipo_arm} | Penalidade: {penalidade} | {propriedades}")
    else:
        st.markdown(f"**{selecionado}** _(sem dados cadastrados)_")


# ===== Adicionar Equipamento Extra =====
st.markdown("---")
st.markdown("### \+ Adicionar Equipamento Extra")

aba = st.radio("Tipo de Adição", ["📦 Item Personalizado", "🗡️ Arma da Base", "🛡️ Armadura da Base"], horizontal=True)

if aba == "📦 Item Personalizado":
    tipo = st.radio("Tipo do Item", ["Item", "Arma", "Armadura"], horizontal=True)
    with st.form("form_item_perso"):
        if tipo == "Arma":
            nome = st.text_input("Nome do Item")
            dano = st.text_input("Dano", placeholder="Ex: 1d6")
            alcance = st.text_input("Alcance", placeholder="Ex: 6m")
            propriedades = st.text_input("Propriedades", placeholder="Ex: Leve, Arremessável")
            atributo = st.selectbox("Atributo Usado", ["Força", "Destreza", "Força/Destreza", "—"])
        elif tipo == "Armadura":
            nome = st.text_input("Nome do Item")
            ca = st.text_input("Classe de Armadura (CA)", placeholder="Ex: 14 + Destreza")
            tipo_armadura = st.text_input("Tipo", placeholder="Leve / Média / Pesada")
            penalidade = st.text_input("Penalidade", placeholder="Ex: -1m")
            propriedades = st.text_input("Propriedades", placeholder="Ex: Discreta, Simbólica")
        elif tipo == "Item":
            nome = st.text_input("Nome do Item")
            descricao = st.text_area("Descrição")

        enviado = st.form_submit_button("Adicionar Item")
        if enviado and nome:
            # Simula registro na tabela (temporário)
            if tipo == "Arma":
                personagem.setdefault("armas_personalizadas", {})[nome] = (dano, alcance, propriedades, atributo)
            elif tipo == "Armadura":
                personagem.setdefault("armaduras_personalizadas", {})[nome] = (ca, tipo_armadura, penalidade, propriedades)
            elif tipo == "Item":
                nome_formatado = f"{nome}: {descricao}" if descricao else nome
                equipamentos["extras"][-1] = nome_formatado  # substitui o nome pelo formatado

            equipamentos["extras"].append(nome)
            st.success(f"{tipo} '{nome}' adicionado ao inventário.")
            st.rerun()

elif aba == "🗡️ Arma da Base":
    opcoes = [arma for arma in tabela_armas.keys() if arma not in equipamentos["extras"]]
    arma_escolhida = st.selectbox("Escolha uma arma:", options=opcoes, index=0 if opcoes else None)
    if arma_escolhida:
        if st.button("Adicionar Arma"):
            equipamentos["extras"].append(arma_escolhida)
            st.success(f"Arma '{arma_escolhida}' adicionada ao inventário.")
            st.rerun()

elif aba == "🛡️ Armadura da Base":
    opcoes = [armadura for armadura in tabela_armaduras.keys() if armadura not in equipamentos["extras"]]
    armadura_escolhida = st.selectbox("Escolha uma armadura:", options=opcoes, index=0 if opcoes else None)
    if armadura_escolhida:
        if st.button("Adicionar Armadura"):
            equipamentos["extras"].append(armadura_escolhida)
            st.success(f"Armadura '{armadura_escolhida}' adicionada ao inventário.")
            st.rerun()
            
# ===== Exibir Inventário =====
st.markdown("---")
st.markdown("### Inventário do Personagem")

mostrar_equipamento("Arma Primária", equipamentos.get("arma_cc"), "arma", tabela_armas, "arma_cc")
mostrar_equipamento("Arma Secundária", equipamentos.get("arma_dist"), "arma", tabela_armas, "arma_dist")
mostrar_equipamento("Armadura", equipamentos.get("armadura"), "armadura", tabela_armaduras, "armadura")

# Itens extras não equipáveis
st.markdown("### Saco de Carga")
extras = equipamentos.get("extras", [])
equipados = [equipamentos.get("arma_cc"), equipamentos.get("arma_dist"), equipamentos.get("armadura")]

for item in extras:
    col1, col2, col3 = st.columns([5, 1, 1])
    with col1:
        if item in tabela_armas and item not in equipados:
            dano, distancia, propriedades, atributo = tabela_armas[item]
            st.markdown(f"- {item} 🗡️ → {dano} | Alcance: {distancia} | {propriedades} | Atributo: {atributo}")
        elif item in tabela_armaduras and item not in equipados:
            ca, tipo_arm, penalidade, propriedades = tabela_armaduras[item]
            st.markdown(f"- {item} 🛡️ → CA {ca} | {tipo_arm} | Penalidade: {penalidade} | {propriedades}")
        elif item not in equipados:
            st.markdown(f"- {item}")

    with col2:
        if (
            item in personagem.get("armas_personalizadas", {}) or 
            item in personagem.get("armaduras_personalizadas", {})
        ):
            if st.button("✏️", key=f"edit_{item}"):
                st.session_state["item_para_editar"] = item
                st.rerun()

    with col3:
        if st.button("🗑️", key=f"del_{item}"):
            equipamentos["extras"].remove(item)
            personagem.get("armas_personalizadas", {}).pop(item, None)
            personagem.get("armaduras_personalizadas", {}).pop(item, None)
            st.success(f"{item} removido do inventário.")
            st.rerun()

if "item_para_editar" in st.session_state:
    item = st.session_state["item_para_editar"]

    if item in personagem.get("armas_personalizadas", {}):
        dano, alcance, propriedades, atributo = personagem["armas_personalizadas"][item]
        st.markdown(f"### ✏️ Editar Arma: *{item}*")

        with st.form("form_editar_arma"):
            novo_dano = st.text_input("Dano", value=dano)
            novo_alcance = st.text_input("Alcance", value=alcance)
            novas_props = st.text_input("Propriedades", value=propriedades)
            novo_atributo = st.selectbox("Atributo", ["Força", "Destreza", "Força/Destreza", "—"], index=0 if atributo not in ["Destreza", "Força/Destreza"] else ["Força", "Destreza", "Força/Destreza", "—"].index(atributo))

            enviar = st.form_submit_button("Salvar Alterações")
            if enviar:
                personagem["armas_personalizadas"][item] = (novo_dano, novo_alcance, novas_props, novo_atributo)
                st.success(f"{item} atualizado!")
                del st.session_state["item_para_editar"]
                st.rerun()
            if st.form_submit_button("Cancelar"):
                del st.session_state["item_para_editar"]
                st.rerun()

    elif item in personagem.get("armaduras_personalizadas", {}):
        ca, tipo_arm, penalidade, propriedades = personagem["armaduras_personalizadas"][item]
        st.markdown(f"### ✏️ Editar Armadura: *{item}*")

        with st.form("form_editar_armadura"):
            nova_ca = st.text_input("CA", value=ca)
            novo_tipo = st.text_input("Tipo", value=tipo_arm)
            nova_penalidade = st.text_input("Penalidade", value=penalidade)
            novas_props = st.text_input("Propriedades", value=propriedades)

            enviar = st.form_submit_button("Salvar Alterações")
            if enviar:
                personagem["armaduras_personalizadas"][item] = (nova_ca, novo_tipo, nova_penalidade, novas_props)
                st.success(f"{item} atualizado!")
                del st.session_state["item_para_editar"]
                st.rerun()
            if st.form_submit_button("Cancelar"):
                del st.session_state["item_para_editar"]
                st.rerun()



# Atualiza os status
st.session_state.personagem = ds.calcular_status_gerais(st.session_state.personagem)
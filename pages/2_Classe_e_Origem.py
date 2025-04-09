import streamlit as st
from estilo import aplicar_estilo_lsbc
from dados_sistema import DadosSistema

# ====== Configuração da Página ======
st.set_page_config(page_title="Classe e Origem", layout="wide")
aplicar_estilo_lsbc()
ds = DadosSistema()
st.markdown("# 🧭 Classe e Origem")

# ====== Inicialização ======
if "personagem" not in st.session_state:
    st.session_state.personagem = ds.inicializar_personagem()
personagem = st.session_state.personagem

# ====== Funções Auxiliares ======
def contar_niveis_totais():
    return len(personagem["classes"])

def contar_classes_distintas():
    return len(set(c["classe"] for c in personagem["classes"]))

def gerar_legenda_personagem():
    nome = personagem.get("nome", "Personagem")
    nivel_total = contar_niveis_totais()
    distribuicao = {}

    for entrada in personagem["classes"]:
        cls = entrada["classe"]
        distribuicao[cls] = distribuicao.get(cls, 0) + 1

    partes = [f"{cls} {lvl}" for cls, lvl in distribuicao.items()]
    distrib_texto = " / ".join(partes)

    return f"""
    <p style='margin-top: -0.5rem; margin-bottom: 1rem; color: #444; font-size: 0.95rem;'>
        🎖️ <strong>{nome}</strong> – Nível Total: {nivel_total}<br>
        🧩 <em>{distrib_texto}</em>
    </p>
    """


# ====== Adição de Nível ======

st.markdown(gerar_legenda_personagem(), unsafe_allow_html=True)

col1, col2 = st.columns([8, 2])
with col1:
    classe_selecionada = st.selectbox("Selecione a classe:", ds.classes_disponiveis)

with col2:
    if st.button("➕ Adicionar Nível"):
        niveis_totais = contar_niveis_totais()
        classes_usadas = {c["classe"] for c in personagem["classes"]}

        if niveis_totais >= 10:
            st.warning("O personagem já possui o nível máximo (10).")
        elif classe_selecionada not in classes_usadas and len(classes_usadas) >= 2:
            st.warning("Só é possível escolher até duas classes diferentes.")
        else:
            niveis_na_classe = sum(1 for c in personagem["classes"] if c["classe"] == classe_selecionada)
            nivel_na_classe = niveis_na_classe + 1
            proximo_nivel = niveis_totais + 1

            bonus = None
            if proximo_nivel in [2, 6, 9]:
                bonus = "atributo"
            elif proximo_nivel in [4, 8]:
                bonus = "proeza"

            personagem["classes"].append({
                "classe": classe_selecionada,
                "nivel": nivel_na_classe,
                "especializacao": None,
                "bonus": bonus
            })

            st.success(f"Nível {nivel_na_classe} de {classe_selecionada} adicionado.")

# ====== Exibição de Níveis ======
st.subheader("Progressão de Níveis")

for i, entrada in enumerate(personagem["classes"]):
    classe = entrada["classe"]
    nivel = entrada["nivel"]
    especializacao = entrada.get("especializacao")

    # Descrição
    if especializacao and nivel in [3, 5, 7, 10]:
        descricao = ds.descricao_especializacoes.get(classe, {}).get(especializacao, {}).get(nivel)
    else:
        descricao = ds.descricao_classes.get(classe, {}).get(nivel)

    if not descricao:
        descricao = "Descrição indisponível."

    col_main, col_del = st.columns([10, 1])
    with col_main:
        # Indicadores com conteúdos escolhidos
        indicadores = []
        if entrada.get("especializacao"):
            indicadores.append(f"🧩 <strong>Especialização:</strong> {entrada['especializacao']}")
        if entrada.get("atributo_escolhido"):
            indicadores.append(f"📈 <strong>Atributo:</strong> {entrada['atributo_escolhido']}")
        if entrada.get("proeza_escolhida"):
            indicadores.append(f"💥 <strong>Proeza:</strong> {entrada['proeza_escolhida']}")

        indicadores_html = "<p style='margin-bottom: 0.75rem;'></p>"
        if indicadores:
            indicadores_html = "<p style='margin-bottom: 0.75rem;'>" + "<br>".join(indicadores) + "</p>"

        st.markdown(
            f"""
            <div style='background-color:#f9f9f9; padding: 1.25rem; border-left: 4px solid #999; border-radius: 0.5rem; margin-bottom: 1rem;'>
                <h4 style='margin-top:0;'>{classe} – Nível {nivel}</h4>
                {indicadores_html}
                {descricao}
            </div>
            """, unsafe_allow_html=True
        )


    with col_del:
        if i == len(personagem["classes"]) - 1:
            if st.button("🗑️", key=f"del_{i}"):
                personagem["classes"].pop(i)
                st.rerun()

    # Escolha de Especialização
    if nivel in [3] and not entrada.get("especializacao"):
        espec_key = f"espec_{i}"
        especializacao = st.selectbox(
            f"Escolha uma especialização para {classe} (nível {nivel})",
            ds.especializacoes_por_classe.get(classe, []),
            key=espec_key
        )
        if st.button("✅ Confirmar Especialização", key=f"conf_espec_{i}"):
            entrada["especializacao"] = especializacao
            st.success(f"Especialização '{especializacao}' aplicada.")

    # Escolha de Atributo
    if entrada.get("bonus") == "atributo" and not entrada.get("atributo_escolhido"):
        attr_key = f"attr_{i}"
        atributo = st.selectbox(
            f"Aumentar atributo (nível {nivel})",
            ds.atributos_base,
            key=attr_key
        )
        if st.button("✅ Confirmar Atributo", key=f"conf_attr_{i}"):
            entrada["atributo_escolhido"] = atributo
            st.success(f"Atributo '{atributo}' aumentado.")

    # Escolha de Proeza
    if entrada.get("bonus") == "proeza" and not entrada.get("proeza_escolhida"):
        proezas_usadas = [c.get("proeza_escolhida") for c in personagem["classes"] if c.get("proeza_escolhida")]
        proezas_disponiveis = [p for p in ds.proezas_disponiveis if p not in proezas_usadas]

        proeza_key = f"proeza_{i}"
        proeza = st.selectbox(
            f"Escolha uma proeza (nível {nivel})",
            proezas_disponiveis,
            key=proeza_key
        )
        if st.button("✅ Confirmar Proeza", key=f"conf_proeza_{i}"):
            entrada["proeza_escolhida"] = proeza
            st.success(f"Proeza '{proeza}' aplicada.")

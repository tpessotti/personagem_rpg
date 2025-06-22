import streamlit as st
from collections import defaultdict
from estilo import aplicar_estilo_lsbc
from auth import salvar_personagem
from dados_sistema import DadosSistema
import json

# ===== Inicialização =====
aplicar_estilo_lsbc()
ds = DadosSistema()
st.markdown("# 🧭 Ficha Personagem LSBC")

# ===== Inicialização de Dados =====
if "personagem" not in st.session_state:
    st.error("Personagem não inicializado.")
    st.stop()

personagem = st.session_state.personagem
atributos_finais = personagem.get("atributos_finais", {})
status = personagem.get("status_gerais", {})
habilidades = personagem.get("habilidades", {})
equipamento = personagem.get("equipamentos", {})
truques = personagem.get("misticismo", {}).get("arsenal", [])
classes = st.session_state.personagem.get("classes", [])
bonus_classe = ds.calcular_bonus_classe(personagem, classes)
nivel_total, classes_texto = ds.calcular_nivel(personagem)
ds.calcular_status_gerais(personagem)
ds.calcular_atributos_finais(personagem, bonus_classe)
tabela_armas = ds.tabela_armas.copy()
tabela_armaduras = ds.tabela_armaduras.copy()

# Adiciona personalizadas
tabela_armas.update(personagem.get("armas_personalizadas", {}))
tabela_armaduras.update(personagem.get("armaduras_personalizadas", {}))

with st.sidebar:
    st.markdown("#### 💾 Salvar")

    # Exportar personagem
    personagem_export = {
        k: v for k, v in personagem.items() if not isinstance(v, st.runtime.uploaded_file_manager.UploadedFile)
    }
    json_personagem = json.dumps(personagem_export, indent=2, ensure_ascii=False)

    st.download_button(
        label="Exportar Personagem (.json)",
        data=json_personagem,
        file_name=f"{personagem.get('nome', 'personagem')}_{nivel_total}.json",
        mime="application/json",
        use_container_width=True,
    )

    if "usuario" in st.session_state:
        nome_pers = personagem.get("nome")
        if nome_pers:
            if st.button("Salvar Personagem na Conta", use_container_width=True):
                salvar_personagem(st.session_state.usuario, nome_pers, personagem)
                st.success(f"{nome_pers} salvo com sucesso!")
        else:
            st.warning("O personagem precisa ter um nome antes de ser salvo.")


    # Botão de impressão real com HTML
    st.markdown("""
        <style>
        @media print {
            .stSidebar {
                display: none !important;
            }
            .main {
                margin-left: 0 !important;
            }
        }
        </style>

        <div style="margin-top: 2rem;">
            <h4>🖨️ Imprimir Ficha</h4>
            <p>Para imprimir, clique no menu do Streamlit canto superior direito e selecione a opção <strong>Print</strong>.</p>
        </div>
    """, unsafe_allow_html=True)

# ===== Funções Auxiliares =====
def mostrar_valor(valor):
    mod = (valor - 10) // 2
    return f"{valor} ({mod:+})"

def mostrar_equipamento(nome, tabela, atributos_finais=None, bonus_proficiencia=0):
    stats = tabela.get(nome)
    if not stats:
        return f"❔ {nome}"

    def calcular_modificador(atributo_nome):
        try:
            valor = int(atributos_finais[atributo_nome]["final"])
            return (valor - 10) // 2
        except (KeyError, TypeError):
            return 0

    if tabela is tabela_armas:
        dano, alcance, propriedades, atributo_raw = stats
        atributo_uso = atributo_raw
        mod = 0

        if atributos_finais:
            if "/" in atributo_raw:  # Ex: "Força/Destreza"
                opcoes = [a.strip() for a in atributo_raw.split("/")]
                mods = {a: calcular_modificador(a) for a in opcoes}
                atributo_uso = max(mods, key=mods.get)
                mod = mods[atributo_uso]
            else:
                atributo_uso = atributo_raw.strip()
                mod = calcular_modificador(atributo_uso)

        bonus_ataque = mod + bonus_proficiencia
        bonus_dano = mod

        return (
            f"**{nome}** | Ataque: +{bonus_ataque} | Dano: {dano} {f'+{bonus_dano}' if bonus_dano >= 0 else bonus_dano} "
            f"| Alcance: {alcance} | {propriedades} | Atributo: {atributo_uso} "
        )

    else:  # tabela_armaduras
        ca, tipo, penalidade, props = stats
        return f"**{nome}** | CA: {ca} | Tipo: {tipo} | Penalidade: {penalidade} | {props}"

# ===== Cabeçalho =====
st.markdown("---")

col_img, col_info = st.columns([1, 4])

with col_img:
    if personagem.get("imagem"):
        st.image(personagem["imagem"], use_container_width=True)
    else:
        st.image("https://imebehavioralhealth.com/wp-content/uploads/2021/10/user-icon-placeholder-1.png", use_container_width=True)

with col_info:
    st.title(f"{personagem.get("nome", "🚫 Nome não informado")} | {nivel_total}")
    st.markdown(f"**Classe:** {classes_texto}")
    st.markdown(f"**Jogador:** {personagem.get('nome_jogador', '🚫')}")
    st.markdown(f"**Origem:** {personagem.get('origem', '🚫')} | **Etnia:** {personagem.get('etnia', '🚫')}")
    st.markdown(f"**Idade:** {personagem.get('idade')} | **Altura:** {personagem.get('altura')}cm | **Peso:** {personagem.get('peso')}kg | **Gênero:** {personagem.get('genero')}")



# ===== Atributos =====
st.markdown("---")
st.subheader("🧬 Atributos")
cols = st.columns(6)
for i, atributo in enumerate(["Força", "Destreza", "Constituição", "Inteligência", "Sabedoria", "Carisma"]):
    valor = atributos_finais.get(atributo, {}).get("final", 0)
    mod = (valor - 10) // 2
    cols[i].markdown(f"<h4 style='text-align:center'>{atributo}</h4>", unsafe_allow_html=True)
    cols[i].markdown(f"<h2 style='text-align:center'><span style='font-size:32px'>{valor} ({mod:+})</span></h2>", unsafe_allow_html=True)

# ===== Status =====
st.markdown("---")
st.subheader("⚙️ Status Gerais")

col1, col2, col3, col4, col5 = st.columns(5)

col1.markdown(f"""
<div style='text-align:center; font-size:20px;'>
    ❤️ <strong>HP</strong><br>
    <span style='font-size:28px;'>{status.get("hp", "—")}</span>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div style='text-align:center; font-size:20px;'>
    🛡️ <strong>CA</strong><br>
    <span style='font-size:28px;'>{status.get("ca", "—")}</span>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div style='text-align:center; font-size:20px;'>
    🏃‍♂️ <strong>Velocidade</strong><br>
    <span style='font-size:28px;'>{status.get("velocidade", "—")} m</span>
</div>
""", unsafe_allow_html=True)

col4.markdown(f"""
<div style='text-align:center; font-size:20px;'>
    ⚡ <strong>Iniciativa</strong><br>
    <span style='font-size:28px;'>+{status.get("iniciativa", "—")}</span>
</div>
""", unsafe_allow_html=True)

col5.markdown(f"""
<div style='text-align:center; font-size:20px;'>
    🎖️ <strong>Proficiência</strong><br>
    <span style='font-size:28px;'>+{status.get("bonus_proficiencia", "—")}</span>
</div>
""", unsafe_allow_html=True)


# ===== Equipamentos =====
st.markdown("---")
st.subheader("🎒 Equipamentos")

arma_cc = equipamento.get("arma_cc")
arma_dist = equipamento.get("arma_dist")
armadura = equipamento.get("armadura")
extras = equipamento.get("extras", [])

if arma_cc:
    st.markdown(mostrar_equipamento(
    arma_cc, tabela_armas,
    atributos_finais=atributos_finais,
    bonus_proficiencia=status.get("bonus_proficiencia", 0)
))

if arma_dist:
    st.markdown(mostrar_equipamento(
    arma_dist, tabela_armas,
    atributos_finais=atributos_finais,
    bonus_proficiencia=status.get("bonus_proficiencia", 0)
))

if armadura:
    st.markdown(mostrar_equipamento(
    armadura, tabela_armaduras,
    atributos_finais=atributos_finais,
    bonus_proficiencia=status.get("bonus_proficiencia", 0)
))

if extras:
    st.markdown("**Itens Extras:**")
    for item in extras:
        st.markdown(f"- {item}")

# ===== Truques =====
st.markdown("---")
st.subheader("✨ Truques (Misticismo)")
if truques:
    for truque in truques:
        st.markdown(f"- Nível {truque['Nível']} | {truque['Tipo']} | **{truque['Nome']}**")
else:
    st.info("Nenhum truque selecionado.")

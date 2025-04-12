import streamlit as st
from collections import defaultdict
from estilo import aplicar_estilo_lsbc
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
tabela_armas = ds.tabela_armas
tabela_armaduras = ds.tabela_armaduras

with st.sidebar:
    st.markdown("## 📁 Exportar")

    # Exportar personagem
    personagem_export = {
        k: v for k, v in personagem.items() if not isinstance(v, st.runtime.uploaded_file_manager.UploadedFile)
    }
    json_personagem = json.dumps(personagem_export, indent=2, ensure_ascii=False)

    st.download_button(
        label="Exportar Personagem (.json)",
        data=json_personagem,
        file_name=f"{personagem.get('nome', 'personagem')}_{nivel_total}.json",
        mime="application/json"
    )

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

def mostrar_equipamento(nome, tabela):
    stats = tabela.get(nome)
    if not stats:
        return f"❔ {nome}"
    if tabela is tabela_armas:
        dano, alcance, propriedades, atributo = stats
        return f"**{nome}** | Dano: {dano} | Alcance: {alcance} | {propriedades} | Atributo: {atributo}"
    else:
        ca, tipo, penalidade, props = stats
        return f"**{nome}** | CA: {ca} | Tipo: {tipo} | Penalidade: {penalidade} | {props}"

# ===== Cabeçalho =====
st.title(f"{personagem.get("nome", "🚫 Nome não informado")} | {nivel_total}")

col_img, col_info = st.columns([1, 2])

with col_img:
    if personagem.get("imagem"):
        st.image(personagem["imagem"], width=200)
    else:
        st.image("https://imebehavioralhealth.com/wp-content/uploads/2021/10/user-icon-placeholder-1.png", width=200)

with col_info:
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
    st.markdown(mostrar_equipamento(arma_cc, tabela_armas))
if arma_dist:
    st.markdown(mostrar_equipamento(arma_dist, tabela_armas))
if armadura:
    st.markdown(mostrar_equipamento(armadura, tabela_armaduras))

if extras:
    st.markdown("**Itens Extras:**")
    for item in extras:
        st.markdown(f"- {item}")

# ===== Truques =====
st.markdown("---")
st.subheader("✨ Truques (Misticismo)")
if truques:
    for truque in truques:
        st.markdown(f"- Nível {truque['nivel']} | {truque['tipo']} | **{truque['nome']}**")
else:
    st.info("Nenhum truque selecionado.")

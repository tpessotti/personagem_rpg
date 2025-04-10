import streamlit as st
from estilo import aplicar_estilo_lsbc, navbar_resumo

# Configuração inicial
st.set_page_config(page_title="LSBC | Segredos Perdidos da Costa Brasileira", layout="wide", initial_sidebar_state="collapsed")
aplicar_estilo_lsbc()
navbar_resumo()

# Prólogo
st.markdown("""

<!-- LOGO / TÍTULO -->
<div class="container">
    <strong style='font-size:3rem;'> 🧭 | LSBC | 🧭 </strong>
    <p style='font-size:3rem;'>|Segredos Perdidos da Costa Brasileira|</p>
    <p style='margin-top:1rem; font-size:0.9rem;'>Descubra mistérios esquecidos entre as marés do século XVIII.</p>
</div>
        
<div class="prologo">
<p>
No início do século XVIII, enquanto os impérios europeus disputavam cada palmo de terra no Novo Mundo, uma costa vasta e pouco explorada guardava segredos que jamais foram registrados nos mapas. Relíquias de um saber esquecido, artefatos de engenhosidade incompreendida e ruínas de civilizações apagadas pelo tempo permanecem escondidas entre as matas, recifes e fortalezas desmoronadas do litoral brasileiro.
</p>

<p>
Capitanias semiautônomas incentivam corsários e piratas, o comércio clandestino floresce, e organizações secretas moldam os destinos de nações em nome do controle do conhecimento perdido. Nesse cenário de intrigas e descobertas, heróis improváveis cruzam caminhos – guiados não por magia, mas pela razão, pela ciência e por uma sede de liberdade.
</p>

<p>
Este é o mundo de <strong>Lost Secrets of the Brazilian Coast</strong>. E sua história está prestes a começar...
</p>

<p style="text-align: center; margin-top: 10rem;">
    <a href="/Criador_de_Personagens" target="_self" style="
        background-color: #fcbf49;
        color: #2d2d2d;
        font-family: 'Alegreya SC', serif;
        padding: 0.6rem 1.4rem;
        border-radius: 8px;
        font-weight: bold;
        text-decoration: none;
        font-size: 1.2rem;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
    ">Começar Criação de Personagem</a>
</p>
</div>
""", unsafe_allow_html=True)

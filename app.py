import streamlit as st

# Importando o novo sistema de navegação com seções
paginas = {
    "🧭 ": [st.Page("pages/LSBC.py", title="LSBC", default=True),
            st.Page("pages/8_login.py", title="Minha Conta"),],
    "🧭": [
        st.Page("pages/0_Criador_de_Personagens.py", title="Criador de Personagens"),
        st.Page("pages/1_Informações_Gerais.py", title="→ Informações Gerais"),
        st.Page("pages/2_Classe_e_Origem.py", title="→ Classe e Origem"),
        st.Page("pages/3_Atributos.py", title="→ Atributos"),
        st.Page("pages/4_Habilidades.py", title="→ Habilidades"),
        st.Page("pages/5_Equipamentos.py", title="→ Equipamentos"),
        st.Page("pages/6_Truques.py", title="→ Truques"),
        st.Page("pages/7_Resumo.py", title="→ Resumo"),
        
    ]
}

# Ativando a navegação por seções
pagina = st.navigation(paginas)

# Executa a página selecionada
pagina.run()

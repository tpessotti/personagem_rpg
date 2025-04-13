import streamlit as st

def aplicar_estilo_lsbc():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Alegreya+SC:wght@400;700&display=swap');
            
            html, body, [class*="css"] {
                font-family: 'Alegreya SC', serif;
                background-color: #f8f5f0;
                color: #2d2d2d;
            }
            
            .stMarkdownContainer {
                font-family: 'Alegreya SC', serif;
                background-color: #f8f5f0;
            }
            
            .stTextArea {
                font-family: 'Alegreya SC', serif;
            }
            
            .stSelectbox{
                font-family: 'Alegreya SC', serif;
            }
            
            h2, h3, h4, h5, h6 {
                font-family: 'Alegreya SC', serif;
                color: #183152;
            }

            .stHeading h1,.stMarkdown h1{
                font-family: 'Alegreya SC', serif;
                color: #183152;
                font-size: 2.4rem;
                font-weight: 700;
            }

            .stMarkdown h2, .stHeading h2 {
                font-family: 'Alegreya SC', serif;
                color: #183152;
                font-size: 1.8rem;
                font-weight: 700;
            }

            .stMarkdown h3, .stHeading h3{
                font-family: 'Alegreya SC', serif;
                color: #183152;
                font-size: 1.5rem;
                font-weight: 700;
            }
            
            .stMarkdown h4, .stHeading h4{
                font-family: 'Alegreya SC', serif;
                color: #183152;
                font-size: 1.2rem;
                font-weight: 700;
            }
            
            .stMarkdown strong, p, span  {
                font-family: 'Alegreya SC', serif;
                font-size: 1.0rem;
                font-weight: 700;
                color: #183152;
            }
            
            .stMarkdown p, li, div {
                font-family: 'Alegreya SC', serif;
                font-size: 1.0rem;
                font-weight: 300;
            }
            
            .stText div {
                font-family: 'Alegreya SC', serif;
                font-size: 1.0rem;
                font-weight: 300;
            }
            
            .stMetric div {
                font-family: 'Alegreya SC', serif;
                font-size: 1.5rem;
                font-weight: 700;
                text-align: center;
                label-align: center;
            }
            
            .stButton>button {
                background-color: #325a7a;
                color: #f8f5f0;
                font-family: 'Alegreya SC', serif;
                border: none;
                padding: 0.0em 0.4em;
            }
            
            .stButton>button p {
                color: white;
                font-family: 'Alegreya SC', serif;
                border: none;
                padding: 0.0em 0.4em;
            }

            .stButton>button:hover {
                font-family: 'Alegreya SC', serif;
                background-color: #3f6f92;
                color: #f8f5f0;
            }
            
            .stButton>button:hover p {
                font-family: 'Alegreya SC', serif;
                color: #f8f5f0;
            }

            .st-bb {
                font-family: 'Alegreya SC', serif;
                background-color: #f8f5f0 !important;
                border-radius: 0.5rem;
            }

            .st-cf {
                font-family: 'Alegreya SC', serif;
            }
            
            .st.at {
                font-family: 'Alegreya SC', serif;
                background-color: #f8f5f0 !important;
            }

            .stTextInput>div>div>input {
                font-family: 'Alegreya SC', serif;
                background-color: #f8f5f0;
            }

            footer {
                visibility: hidden;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def navbar_homepage():
    col1, col2, col3 = st.columns([1, 7, 2])
    
    with col1:
        st.markdown(
            "<div style='font-size:1.4rem; font-family:serif;'>🧭 <strong>LSBC</strong></div>",
            unsafe_allow_html=True,
        )

    with col3:
        if "usuario" in st.session_state:
            st.markdown(f"""
                <p style="text-align: right;">
                    👤 <strong>{st.session_state.usuario}</strong>
                    <a href="/" target="_self" style="
                    color: #2d2d2d;
                    font-family: 'Alegreya SC', serif;
                    text-decoration: none;
                    font-size: 0.85rem;
                ">[Logout]</a>
                </p>
            """, unsafe_allow_html=True)
            
        else:
            st.markdown("""                        
                <p style="text-align: right;">
                    <a href="/login" target="_self" style="
                        color: #2d2d2d;
                        font-family: 'Alegreya SC', serif;
                        text-decoration: none;
                        font-size: 0.85rem;
                    ">[Login / Criar Conta]</a>
                </p>
            """, unsafe_allow_html=True)

def remover_sidebar():
    st.markdown(
        """
        <style>
            .stSidebar {
                display: none;
            }
            header[data-testid="stHeader"] {
            display: none;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def estilo_homepage():
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Alegreya+SC:wght@700&display=swap" rel="stylesheet">

    <style>
    /* Remove a sidebar e cabeçalho */
    header[data-testid="stHeader"] {
        display: none;
    }

    /* Background com imagem de mapa */
    .stApp {
        background: 
            linear-gradient(rgba(250, 245, 230, 0.75), rgba(250, 245, 230, 0.75)),
            url('https://kartinki.pics/pics/uploads/posts/2022-08/1660264608_64-kartinkin-net-p-fon-staraya-karta-krasivo-72.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: relative;
    }

    /* Conteúdo centralizado */
    .container {
        font-family: 'Alegreya SC', serif;
        text-align: center;
        margin: 3rem auto;
        line-height: 5rem;
        border-radius: 10px;
        width: 80%;
        color: #2d2d2d;
    }

    /* Prólogo */
    .prologo {
        padding: 2rem;
        border-radius: 8px;
        margin: 2rem auto;
        width: 80%;
        padding-top: 50px;
        padding-bottom: 50px;
        font-size: 1.2rem;
        line-height: 1.8rem;
        text-align: justify;
    }
    </style>

    """, unsafe_allow_html=True)
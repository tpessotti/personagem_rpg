import streamlit as st
from auth import autenticar, registrar_usuario
from estilo import aplicar_estilo_lsbc, remover_sidebar
from datetime import datetime
import streamlit as st

# Configuração inicial
st.set_page_config(page_title="Login | LSBC", layout="centered")
aplicar_estilo_lsbc()
#remover_sidebar()

def esqueci_a_senha():
    if "mostrar_expander_senha" not in st.session_state:
        st.session_state.mostrar_expander_senha = False
    with st.expander("🔐 Esqueci minha senha", expanded=st.session_state.mostrar_expander_senha):
        from auth import carregar_usuarios, validar_resposta_seguranca, redefinir_senha

        usuarios = carregar_usuarios()

        # Campo de entrada de usuário
        usuario_esqueci = st.text_input("Usuário", key="usuario_esqueci")

        # Controle de verificação
        if "usuario_verificado" not in st.session_state:
            st.session_state.usuario_verificado = None  # None = não verificado ainda

        # Botão para verificar se o usuário existe
        if st.button("Verificar Usuário"):
            st.session_state.mostrar_expander_senha = True
            if usuario_esqueci in usuarios:
                st.session_state.usuario_verificado = True
            else:
                st.session_state.usuario_verificado = False

        # Resultado da verificação
        if st.session_state.usuario_verificado is False:
            st.warning("Usuário não encontrado.")
            if st.button("Criar Conta"):
                st.switch_page("pages/login.py")  # ou o caminho correto da página de login
            return

        # Se o usuário foi verificado com sucesso
        if st.session_state.usuario_verificado and usuario_esqueci in usuarios:
            pergunta = usuarios[usuario_esqueci].get("pergunta_seguranca", "Pergunta não cadastrada.")
            st.markdown(f"**Pergunta de Segurança:** {pergunta}")

            resposta_usuario = st.text_input("Resposta", type="password", key="resposta_seguranca")
            nova_senha = st.text_input("Nova Senha", type="password", key="nova_senha")
            confirmar_nova_senha = st.text_input("Confirmar Nova Senha", type="password", key="confirmar_nova_senha")

            if st.button("Redefinir Senha"):
                if nova_senha != confirmar_nova_senha:
                    st.error("As senhas não coincidem.")
                elif not validar_resposta_seguranca(usuario_esqueci, resposta_usuario):
                    st.error("Resposta incorreta.")
                else:
                    redefinir_senha(usuario_esqueci, nova_senha)
                    st.success("Senha redefinida com sucesso! Faça login com a nova senha.")
                    st.session_state.usuario_verificado = None  # Reseta

if "usuario" not in st.session_state:
    st.markdown("## 🔐 Acesso ao Sistema LSBC")

    modo = st.radio("Você deseja:", ["🔑 Login", "📝 Criar Conta"], horizontal=True)
    usuario = st.text_input("Usuário")

    if modo == "🔑 Login":
        senha = st.text_input("Senha", type="password")
    else:
        senha = st.text_input("Senha", type="password")
        senha_confirm = st.text_input("Confirmar Senha", type="password")
        pergunta = st.selectbox("Pergunta de Segurança", [
        "Qual era o nome do seu primeiro animal de estimação?",
        "Em que cidade você nasceu?",
        "Qual foi o nome do seu primeiro personagem de RPG?",
        "Qual é o nome da sua taverna favorita no mundo fictício?",
        "Qual seria o nome da sua arma lendária?",
        "Qual foi a primeira classe que você jogou em um RPG?",
        "Qual era o nome do seu grupo de aventureiros?",
        "Qual o nome do vilão mais memorável da sua campanha?",
        "Qual o nome do mestre que mais te fez sofrer?",
        "Qual o nome da cidade onde você sempre começa campanhas?",
        "Seu nome é Gabriel?"
    ])
        resposta = st.text_input("Resposta à Pergunta de Segurança")


    col1, col2 = st.columns([1, 1])
    with col1:
        confirmar = st.button("Entrar" if modo == "🔑 Login" else "Criar Conta", use_container_width=True)
            
    with col2:
        voltar = st.button("Voltar para a página Principal", use_container_width=True)

    if voltar:
        st.switch_page("pages/LSBC.py")

    if confirmar:
        if modo == "🔑 Login":
            if autenticar(usuario, senha):
                st.session_state.usuario = usuario
                st.success(f"Bem-vindo de volta, {usuario}!")
                st.switch_page("pages/LSBC.py")
            else:
                st.error("Usuário ou senha incorretos.")
                esqueci_a_senha()
        else:
            if senha != senha_confirm:
                st.error("As senhas não coincidem.")
            elif not resposta.strip():
                st.error("Por favor, preencha a resposta de segurança.")
            else:
                if registrar_usuario(usuario, senha, pergunta, resposta):
                    st.session_state.usuario = usuario
                    st.success("Conta criada com sucesso! Bem-vindo, {usuario}!")
                    st.switch_page("pages/LSBC.py")
                else:
                    st.error("Este nome de usuário já existe.")
            

## ===============Exibir informações do usuário logado===============

from auth import carregar_personagens_usuario
from datetime import datetime
from collections import Counter
import random

comentarios_fixos = [
    "🦜 Um bom personagem começa com um bom nome… ou com um papagaio treinado.",
    "📜 Você já salvou o mundo hoje? Não? Hora de criar alguém que faça isso por você.",
    "🎲 Dados não mentem… só tiram 1 na hora errada. Ou na vez do Thorvak",
    "☠️ Os NPCs têm sentimentos também.",
    "🔮 Lembre-se: se tudo der errado, culpe os dados e role novamente.",
    "🐒 Seu macaco contador já está esperando um novo herói pra acompanhar!",
    "🧂 Cuidado com a classe Duelista… o estilo é afiado, mas a paciência do Mestre também.",
    "🏴‍☠️ Melhor levantar essa bandeira logo!",
]

comentarios_0 = [
    "Ainda não começou a criar seu personagem?",
    "A aventura está esperando por você! Ou não...",
    "Um novo personagem pode mudar tudo! LITERALMENTE! ",
    "Sério que você não tem nenhum personagem?",]

if "usuario" in st.session_state:
    personagens = carregar_personagens_usuario(st.session_state.usuario)
    total = len(personagens)
    
    st.markdown(f"## Bem-vindo(a) de volta, {st.session_state.usuario}!")
    st.markdown("---")  
    
    if total == 0:
        st.markdown(f"## ⚠️ {random.choice(comentarios_0)} ⚠️")
        st.markdown("---")
        criar = st.button("Criar Personagem", use_container_width=True, key="criar_personagem")
        if criar:
            st.switch_page("pages/0_Criador_de_Personagens.py")
    else:
        st.markdown(f"#### {random.choice(comentarios_fixos)}")
        st.markdown("---")   
        st.markdown("### 📈 Suas Estatísticas")
        st.markdown(f"**Total de Personagens:** {total}")
    

    if total > 0:
        # 🧙‍♂️ Último personagem editado
        personagem_mais_recente = max(
            personagens.items(),
            key=lambda item: item[1].get("ultima_edicao", "")
        )
        nome_recente, dados = personagem_mais_recente
        try:
            data_formatada = datetime.fromisoformat(dados["ultima_edicao"]).strftime("%d/%m/%Y às %H:%M")
        except:
            data_formatada = "Desconhecida"

        st.markdown(f"**Última edição:** {nome_recente} em {data_formatada}")

        # 📦 Contagem de classes e etnias
        todas_classes = []
        todas_etnias = []

        for p in personagens.values():
            todas_classes += [c.get("classe") for c in p.get("classes", [])]
            todas_etnias.append(p.get("etnia", "Desconhecida"))

        contagem_classes = Counter(todas_classes)
        contagem_etnias = Counter(todas_etnias)

        classe_mais = contagem_classes.most_common(1)[0] if contagem_classes else ("Nenhuma", 0)
        etnia_mais = contagem_etnias.most_common(1)[0] if contagem_etnias else ("Desconhecida", 0)

        st.markdown(f"**Classe mais usada:** {classe_mais[0]} ({classe_mais[1]}x)")
        st.markdown(f"**Etnia mais frequente:** {etnia_mais[0]} ({etnia_mais[1]}x)")

        # 🌎 Lista de etnias mais frequentes
        if len(contagem_etnias) > 1:
            st.markdown("**🌍 Outras etnias comuns:**")
            for etnia, qtd in contagem_etnias.most_common(5):
                if etnia != etnia_mais[0]:
                    st.markdown(f"- {etnia}: {qtd} personagem(ns)")

        from streamlit_autorefresh import st_autorefresh
        import random

        # Controla o índice do comentário e tempo de atualização
        st_autorefresh(interval=10000, key="comentario_refresh", limit=None)

        if "comentario_index" not in st.session_state:
            st.session_state.comentario_index = 0

        comentarios = []

        # Comentários baseados nas estatísticas
        if total == 1:
            comentarios.append("Parece que temos um favorito... 👀")
        elif 2 <= total <= 3:
            comentarios.append("Você tem um pequeno esquadrão… ou um grupo de personalidades alternativas?")
        elif 4 <= total <= 9:
            comentarios.append("Essa mesa tem mais integrantes do que sua última reunião de trabalho.")
        elif total >= 10:
            comentarios.append("Você desbloqueou o multiverso do LSBC. Prepare o crossover. 🌌")
            comentarios.append("Você é o próprio Conclave dos Avatares: um de cada reino. 🌈")

        if classe_mais in ["duelista", "marujo"]:
            comentarios.append("Você claramente resolve as coisas no grito e na lâmina. 🗡️")
        elif classe_mais in ["sacerdote", "erudito", "cientista"]:
            comentarios.append("Palavras e sabedoria… até o Mestre treme quando você abre a boca. 📚")

        if etnia_mais in ["indígenas", "indígena"]:
            comentarios.append("Conexão com a terra e a ancestralidade. O mestre de floresta te respeita. 🌿")
        elif etnia_mais in ["africanos", "africano"]:
            comentarios.append("Suas fichas são tão resistentes quanto a história dos seus povos. 🔥")
        elif etnia_mais in ["latino-americanos", "latino-americano"]:
            comentarios.append("Samba, suor e estratégia. O combo perfeito. 💃")
        elif len(contagem_etnias) >= 5:
            comentarios.append("Seu grupo é mais diverso que congresso interplanar. 🌍")

        # Comentários extras sempre disponíveis
        comentarios += [
            "🦜 Cuidado para não pisar na calopsita!!",
        ]

        # Avança o índice circularmente
        if comentarios:
            idx = st.session_state.comentario_index % len(comentarios)
            st.markdown("---")
            st.markdown(f"#### {comentarios[idx]}")
            st.session_state.comentario_index += 1

    st.markdown("---") 
    logout = st.button("Logout", use_container_width=True, key="logout")
    if logout:
        st.switch_page("pages/LSBC.py")
        
    voltar = st.button("Voltar para a página Principal", use_container_width=True)

    if voltar:
        st.switch_page("pages/LSBC.py")

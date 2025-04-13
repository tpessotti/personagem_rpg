import requests
import hashlib
from datetime import datetime
import streamlit as st

# --- CONFIGURAÇÃO JSONBIN ---
API_KEY = st.secrets["JSONBIN_API_KEY"]
BIN_ID = st.secrets["JSONBIN_BIN_ID"]

HEADERS = {
    "Content-Type": "application/json",
    "X-Master-Key": API_KEY
}

URL_BIN = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
URL_LATEST = f"{URL_BIN}/latest"

# --- UTILITÁRIOS JSONBIN ---

def carregar_todos_usuarios():
    """Carrega todos os dados do bin"""
    response = requests.get(URL_LATEST, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("record", {})
    else:
        print("Erro ao carregar usuários:", response.text)
        return {}

def salvar_todos_usuarios(data):
    """Substitui todos os dados no bin"""
    response = requests.put(URL_BIN, headers=HEADERS, json=data)
    if response.status_code not in [200, 201]:
        print("Erro ao salvar usuários:", response.text)

def hash_senha(senha):
    """Aplica hash SHA256"""
    return hashlib.sha256(senha.encode()).hexdigest()

# --- AUTENTICAÇÃO ---

def autenticar(usuario, senha):
    usuarios = carregar_todos_usuarios()
    user = usuarios.get(usuario)
    return user and user.get("senha") == hash_senha(senha)

def registrar_usuario(usuario, senha, pergunta=None, resposta=None):
    usuarios = carregar_todos_usuarios()
    if usuario in usuarios:
        return False

    usuarios[usuario] = {
        "senha": hash_senha(senha),
        "personagens": {},
        "pergunta_seguranca": pergunta,
        "resposta_seguranca": hash_senha(resposta) if resposta else None,
        "ultima_entrada": datetime.now().isoformat()
    }

    salvar_todos_usuarios(usuarios)
    return True

# --- PERSONAGENS ---

def carregar_personagens_usuario(usuario):
    usuarios = carregar_todos_usuarios()
    return usuarios.get(usuario, {}).get("personagens", {})

def salvar_personagem(usuario, nome_personagem, personagem):
    usuarios = carregar_todos_usuarios()
    if usuario in usuarios:
        personagem["ultima_edicao"] = datetime.now().isoformat()
        personagens = usuarios[usuario].get("personagens", {})
        personagens[nome_personagem] = personagem
        usuarios[usuario]["personagens"] = personagens
        salvar_todos_usuarios(usuarios)

def excluir_personagem(usuario, nome_personagem):
    usuarios = carregar_todos_usuarios()
    if usuario in usuarios:
        personagens = usuarios[usuario].get("personagens", {})
        personagens.pop(nome_personagem, None)
        usuarios[usuario]["personagens"] = personagens
        salvar_todos_usuarios(usuarios)

# --- SEGURANÇA DE SENHA ---

def validar_resposta_seguranca(usuario, resposta):
    usuarios = carregar_todos_usuarios()
    if usuario not in usuarios:
        return False
    return hash_senha(resposta) == usuarios[usuario].get("resposta_seguranca")

def redefinir_senha(usuario, nova_senha):
    usuarios = carregar_todos_usuarios()
    if usuario in usuarios:
        usuarios[usuario]["senha"] = hash_senha(nova_senha)
        salvar_todos_usuarios(usuarios)

# --- COMPATIBILIDADE ANTIGA ---

def carregar_usuarios():
    """Retorna todos os usuários como dicionário {usuario: {...}}"""
    return carregar_todos_usuarios()

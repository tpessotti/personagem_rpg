import os
import json
import hashlib
from datetime import datetime
import streamlit as st

CAMINHO_ARQUIVO = "data/usuarios.json"

def carregar_usuarios():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return {}
    with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_usuarios(usuarios):
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=2, ensure_ascii=False)

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def autenticar(usuario, senha):
    usuarios = carregar_usuarios()
    if usuario in usuarios and usuarios[usuario]["senha"] == hash_senha(senha):
        return True
    return False

def registrar_usuario(usuario, senha, pergunta=None, resposta=None):
    usuarios = carregar_usuarios()
    if usuario in usuarios:
        return False

    usuarios[usuario] = {
        "senha": hash_senha(senha),
        "personagens": {},
        "pergunta_seguranca": pergunta,
        "resposta_seguranca": hash_senha(resposta) if resposta else None
    }

    salvar_usuarios(usuarios)
    return True

def validar_resposta_seguranca(usuario, resposta):
    usuarios = carregar_usuarios()
    if usuario in usuarios:
        resposta_hash = hash_senha(resposta)
        return resposta_hash == usuarios[usuario].get("resposta_seguranca")
    return False

def redefinir_senha(usuario, nova_senha):
    usuarios = carregar_usuarios()
    if usuario in usuarios:
        usuarios[usuario]["senha"] = hash_senha(nova_senha)
        salvar_usuarios(usuarios)
        return True
    return False

def salvar_personagem(usuario, nome_personagem, personagem):
    usuarios = carregar_usuarios()
    if usuario in usuarios:
        personagem["ultima_edicao"] = datetime.now().isoformat()
        usuarios[usuario]["personagens"][nome_personagem] = personagem
        salvar_usuarios(usuarios)

def carregar_personagens_usuario(usuario):
    usuarios = carregar_usuarios()
    if usuario in usuarios:
        return usuarios[usuario].get("personagens", {})
    return {}

def excluir_personagem(usuario, nome_personagem):
    usuarios = carregar_usuarios()
    if usuario in usuarios:
        usuarios[usuario]["personagens"].pop(nome_personagem, None)
        salvar_usuarios(usuarios)

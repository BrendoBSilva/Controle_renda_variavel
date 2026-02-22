import json
import os

USUARIOS_FILE = "usuarios.json"

def carregar_usuarios():
    """Carrega a lista de usuários, corrige se arquivo estiver vazio ou corrompido"""
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, "r") as f:
            try:
                usuarios = json.load(f)
                if not isinstance(usuarios, list):
                    usuarios = []
            except json.JSONDecodeError:
                usuarios = []
    else:
        usuarios = []
    return usuarios

def salvar_usuarios(usuarios):
    with open(USUARIOS_FILE, "w") as f:
        json.dump(usuarios, f, indent=4)

def registrar_usuario(username, senha):
    usuarios = carregar_usuarios()
    for user in usuarios:
        if user.get("username") == username:
            return False
    usuarios.append({"username": username, "senha": senha})
    salvar_usuarios(usuarios)
    return True

def autenticar(username, senha):
    usuarios = carregar_usuarios()
    for user in usuarios:
        if user.get("username") == username and user.get("senha") == senha:
            return True
    return False
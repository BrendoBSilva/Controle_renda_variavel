import json
import os

DATA_FILE = "dados.json"

def carregar_dados(usuario):
    with open("dados.json", "r") as f:
        dados = json.load(f)

    if usuario not in dados:
        dados[usuario] = {"receitas": [], "gastos": []}

    return dados[usuario]

def salvar_dados(usuario, dados_usuario):
    """
    Salva os dados do usuário no arquivo JSON.
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                all_data = json.load(f)
                if not isinstance(all_data, dict):
                    all_data = {}
            except json.JSONDecodeError:
                all_data = {}
    else:
        all_data = {}

    all_data[usuario] = dados_usuario

    with open(DATA_FILE, "w") as f:
        json.dump(all_data, f, indent=4)

def adicionar_receita(usuario, receita):
    """
    Adiciona uma receita para o usuário.
    receita: {"data": "2026-02-21", "valor": 100.0, "origem": "Venda"}
    """
    dados = carregar_dados(usuario)
    dados["receitas"].append(receita)
    salvar_dados(usuario, dados)

def adicionar_gasto(usuario, gasto):
    """
    Adiciona um gasto para o usuário.
    gasto: {"data": "2026-02-21", "valor": 50.0, "categoria": "Casa", "tipo": "normal"}
    """
    dados = carregar_dados(usuario)
    dados["gastos"].append(gasto)
    salvar_dados(usuario, dados)
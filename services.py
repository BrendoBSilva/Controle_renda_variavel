from db import connectar
import pandas as pd
from datetime import date, datetime
from data_manager import carregar_dados

def registrar_receita(data, valor, origem):
    conn = connectar()
    cursor = conn.cursor()
    cursor.execute(
        "Insert into receitas (data, valor, origem) values (%s, %s, %s)",
        (data, valor, origem)
    )
    conn.commit()
    cursor.close()

def registrar_gasto(data, valor, categoria, tipo):
    conn = connectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO gastos (data, valor, categoria, tipo) VALUES (%s, %s, %s, %s)",
        (data, valor, categoria, tipo)
    )

    conn.commit()
    cursor.close()
    conn.close()


def resumo_mensal(usuario):

    dados = carregar_dados(usuario)

    hoje = date.today()
    mes_atual = hoje.month
    ano_atual = hoje.year

    receitas = 0
    gastos = 0
    gastos_inesperados = 0


    for r in dados["receitas"]:
        data_registro = datetime.strptime(r["data"], "%Y-%m-%d")
        if data_registro.month == mes_atual and data_registro.year == ano_atual:
            receitas += r["valor"]


    for g in dados["gastos"]:
        data_registro = datetime.strptime(g["data"], "%Y-%m-%d")
        if data_registro.month == mes_atual and data_registro.year == ano_atual:
            gastos += g["valor"]
            if g["tipo"] == "inesperado":
                gastos_inesperados += g["valor"]

    return receitas, gastos, gastos_inesperados

def comparar_meses():
    conn = connectar()

    query = """
    SELECT 
        YEAR(data) as ano,
        MONTH(data) as mes,
        SUM(valor) as total
    FROM receitas
    WHERE data >= DATE_SUB(CURRENT_DATE(), INTERVAL 2 MONTH)
    GROUP BY ano, mes
    ORDER BY ano, mes;
    """

    receitas = pd.read_sql(query, conn)

    query_gastos = """
    SELECT 
        YEAR(data) as ano,
        MONTH(data) as mes,
        SUM(valor) as total
    FROM gastos
    WHERE data >= DATE_SUB(CURRENT_DATE(), INTERVAL 2 MONTH)
    GROUP BY ano, mes
    ORDER BY ano, mes;
    """

    gastos = pd.read_sql(query_gastos, conn)

    conn.close()

    return receitas, gastos

def calcular_score(receitas, gastos, gastos_inesperados, meta):

    score = 100
    lucro = receitas - gastos


    if lucro < 0:
        score -= 40


    if receitas > 0:
        perc_inesperado = gastos_inesperados / receitas
        if perc_inesperado > 0.3:
            score -= 25


    if meta > 0 and lucro < meta * 0.5:
        score -= 20


    if gastos > receitas:
        score -= 15

    score = max(score, 0)

    
    if score >= 80:
        status = "🟢 Estável"
    elif score >= 50:
        status = "🟡 Atenção"
    else:
        status = "🔴 Crítico"

    return score, status

def projetar_fim_do_mes(receitas, gastos):
    hoje = date.today().day

    if hoje == 0:
        return 0

    lucro_atual = receitas - gastos
    media_diaria = lucro_atual / hoje
    projecao = media_diaria * 30

    return projecao

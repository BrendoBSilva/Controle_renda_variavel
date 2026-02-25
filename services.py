from db import conectar
from datetime import date
import calendar

def registrar_receita(usuario, data, valor, origem):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO receita (usuario, data, valor, origem) VALUES (?, ?, ?, ?)",
        (usuario, str(data), valor, origem)
    )

    conn.commit()
    conn.close()

def registrar_gasto(usuario, data, valor, categoria, tipo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO gasto (usuario, data, valor, categoria, tipo) VALUES (?, ?, ?, ?, ?)",
        (usuario, str(data), valor, categoria, tipo)
    )

    conn.commit()
    conn.close()

def resumo_mensal(usuario):
    hoje = date.today()
    mes = hoje.month
    ano = hoje.year

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(valor) FROM receita
        WHERE usuario = ? AND strftime('%m', data) = ? AND strftime('%Y', data) = ?
    """, (usuario, f"{mes:02d}", str(ano)))
    receitas = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT SUM(valor) FROM gasto
        WHERE usuario = ? AND strftime('%m', data) = ? AND strftime('%Y', data) = ?
    """, (usuario, f"{mes:02d}", str(ano)))
    gastos = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT SUM(valor) FROM gasto
        WHERE usuario = ? AND tipo = 'inesperado'
        AND strftime('%m', data) = ? AND strftime('%Y', data) = ?
    """, (usuario, f"{mes:02d}", str(ano)))
    gastos_inesperados = cursor.fetchone()[0] or 0

    conn.close()

    return receitas, gastos, gastos_inesperados

def calcular_score(receitas, gastos, inesperados, meta):
    lucro = receitas - gastos

    score = 50

    if lucro > 0:
        score += 20
    if meta > 0 and lucro >= meta:
        score += 20
    if inesperados == 0:
        score += 10

    score = max(0, min(100, score))

    if score >= 80:
        status = "Excelente 🔥"
    elif score >= 60:
        status = "Bom 👍"
    elif score >= 40:
        status = "Atenção ⚠️"
    else:
        status = "Crítico 🚨"

    return score, status

def projetar_fim_do_mes(receitas, gastos):
    hoje = date.today()
    dias_mes = calendar.monthrange(hoje.year, hoje.month)[1]
    dia_atual = hoje.day

    saldo_atual = receitas - gastos

    if dia_atual == 0:
        return saldo_atual

    media_diaria = saldo_atual / dia_atual
    projecao = media_diaria * dias_mes

    return projecao

def buscar_todos_registros(usuario):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, data, valor, origem FROM receita WHERE usuario = ?", (usuario,))
    receitas = cursor.fetchall()

    cursor.execute("SELECT id, data, valor, categoria, tipo FROM gasto WHERE usuario = ?", (usuario,))
    gastos = cursor.fetchall()

    conn.close()

    return receitas, gastos

def excluir_registro(tipo, registro_id):
    conn = conectar()
    cursor = conn.cursor()

    if tipo == "receita":
        cursor.execute("DELETE FROM receita WHERE id = ?", (registro_id,))
    else:
        cursor.execute("DELETE FROM gasto WHERE id = ?", (registro_id,))

    conn.commit()
    conn.close()
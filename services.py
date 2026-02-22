from db import connectar
import pandas as pd

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

def resumo_mensal():
    conn = connectar()
    query_receitas = """
        SELECT SUM(valor) as total FROM receitas
        WHERE MONTH(data) = MONTH(CURRENT_DATE())
        AND YEAR(data) = YEAR(CURRENT_DATE())
    """
    query_gastos = """
        SELECT SUM(valor) as total FROM gastos
        WHERE MONTH(data) = MONTH(CURRENT_DATE())
        AND YEAR(data) = YEAR(CURRENT_DATE())
"""

    total_receitas = pd.read_sql(query_receitas, conn).iloc[0, 0] or 0
    total_gastos = pd.read_sql(query_gastos, conn).iloc[0, 0] or 0

    conn.close()
    return total_receitas, total_gastos

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
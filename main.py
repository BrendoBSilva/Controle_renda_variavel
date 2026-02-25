import streamlit as st
import pandas as pd
from datetime import date
from db import criar_tabelas
from auth import registrar_usuario, autenticar
from services import (
    registrar_receita,
    registrar_gasto,
    resumo_mensal,
    calcular_score,
    projetar_fim_do_mes,
    buscar_todos_registros,
    excluir_registro
)

criar_tabelas()

st.set_page_config(
    page_title="Controle Financeiro",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --------- CSS PREMIUM MOBILE ---------

st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 3rem;
}

.card {
    background: #111827;
    padding: 18px;
    border-radius: 16px;
    margin-bottom: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
}

.card h3 {
    margin: 0;
    font-size: 14px;
    color: #9CA3AF;
}

.card h2 {
    margin: 5px 0 0 0;
    font-size: 22px;
}

.success { color: #10B981; }
.danger { color: #EF4444; }
.warning { color: #F59E0B; }

.stButton>button {
    border-radius: 12px;
    height: 45px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# --------- SESSÃO ---------
st.title("Controle Financeiro")
if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

# --------- LOGIN ---------
if st.session_state.usuario_logado is None:


    aba = st.radio("", ["Entrar", "Criar Conta"])

    username = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if aba == "Criar Conta":
        if st.button("Criar Conta", use_container_width=True):
            if registrar_usuario(username, senha):
                st.success("Conta criada com sucesso!")
            else:
                st.error("Usuário já existe.")
    else:
        if st.button("Entrar", use_container_width=True):
            if autenticar(username, senha):
                st.session_state.usuario_logado = username
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

    st.stop()

usuario = st.session_state.usuario_logado

# --------- MENU MOBILE ---------
menu = st.selectbox(
    "",
    [
        "🏠 Dashboard",
        "➕ Ganho",
        "➖ Gasto",
        "📅 Histórico",
        "🗑️ Corrigir",
        "⚙️ Conta"
    ]
)

# ================= DASHBOARD =================

if menu == "🏠 Dashboard":
    st.title("💰 Controle Geral")
    receitas, gastos, inesperados = resumo_mensal(usuario)
    lucro = receitas - gastos

    # CARDS
    st.markdown(f"""
    <div class="card">
        <h3>Entrou</h3>
        <h2 class="success">R$ {receitas:,.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <h3>Saiu</h3>
        <h2 class="danger">R$ {gastos:,.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

    cor = "success" if lucro >= 0 else "danger"

    st.markdown(f"""
    <div class="card">
        <h3>Resultado</h3>
        <h2 class="{cor}">R$ {lucro:,.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

    # META
    meta = st.number_input("Meta do mês", min_value=0.0)

    if meta > 0:
        progresso = max(min(lucro / meta, 1), 0)
        st.progress(progresso)
        st.caption(f"{progresso * 100:.0f}% da meta")

    # SCORE
    score, status = calcular_score(receitas, gastos, inesperados, meta)

    st.markdown(f"""
    <div class="card">
        <h3>Score do Mês</h3>
        <h2>{score}/100</h2>
        <p>{status}</p>
    </div>
    """, unsafe_allow_html=True)

    # PROJEÇÃO
    projecao = projetar_fim_do_mes(receitas, gastos)

    cor_proj = "success" if projecao >= 0 else "danger"

    st.markdown(f"""
    <div class="card">
        <h3>Projeção Final</h3>
        <h2 class="{cor_proj}">R$ {projecao:,.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

# ================= GANHO =================
elif menu == "➕ Ganho":
    st.subheader("Novo Ganho")

    valor = st.number_input("Valor", min_value=0.0)
    origem = st.text_input("Origem")
    data_input = st.date_input("Data", value=date.today())

    if st.button("Salvar", use_container_width=True):
        registrar_receita(usuario, data_input, valor, origem)
        st.success("Ganho registrado!")

# ================= GASTO =================
elif menu == "➖ Gasto":
    st.subheader("Novo Gasto")

    valor = st.number_input("Valor", min_value=0.0)
    categoria = st.selectbox("Categoria",
        ["Casa", "Transporte", "Alimentação", "Trabalho", "Emergência"]
    )
    tipo = st.radio("Tipo", ["normal", "inesperado"])
    data_input = st.date_input("Data", value=date.today())

    if st.button("Salvar", use_container_width=True):
        registrar_gasto(usuario, data_input, valor, categoria, tipo)
        st.success("Gasto registrado!")

# ================= HISTÓRICO =================
elif menu == "📅 Histórico":
    receitas_db, gastos_db = buscar_todos_registros(usuario)

    df_receitas = pd.DataFrame(receitas_db, columns=["id","data","valor","origem"])
    df_gastos = pd.DataFrame(gastos_db, columns=["id","data","valor","categoria","tipo"])

    if df_receitas.empty and df_gastos.empty:
        st.info("Sem registros.")
        st.stop()

    if not df_receitas.empty:
        df_receitas["data"] = pd.to_datetime(df_receitas["data"])
        df_receitas["tipo"] = "Receita"

    if not df_gastos.empty:
        df_gastos["data"] = pd.to_datetime(df_gastos["data"])
        df_gastos["tipo"] = "Gasto"

    df = pd.concat([df_receitas, df_gastos], ignore_index=True)

    st.bar_chart(df.groupby("tipo")["valor"].sum())
    st.dataframe(df.sort_values("data", ascending=False), use_container_width=True)

# ================= CORRIGIR =================
elif menu == "🗑️ Corrigir":
    receitas_db, gastos_db = buscar_todos_registros(usuario)

    for r in receitas_db:
        if st.button(f"Excluir Receita {r[1]} - R${r[2]}"):
            excluir_registro("receita", r[0])
            st.rerun()

    for g in gastos_db:
        if st.button(f"Excluir Gasto {g[1]} - R${g[2]}"):
            excluir_registro("gasto", g[0])
            st.rerun()

# ================= CONTA =================
elif menu == "⚙️ Conta":
    st.write(f"Usuário: {usuario}")
    if st.button("Sair", use_container_width=True):
        st.session_state.usuario_logado = None
        st.rerun()
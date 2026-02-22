import streamlit as st
from datetime import date
import pandas as pd
from auth import registrar_usuario, autenticar
from data_manager import carregar_dados, adicionar_receita, adicionar_gasto, salvar_dados

st.set_page_config(
    page_title="Controle Financeiro",
    layout="centered"
)

# ---------------- SESSÃO ----------------
if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

# ---------------- LOGIN ----------------
if st.session_state.usuario_logado is None:
    st.title("📱 Controle de Renda")

    aba = st.radio("Acessar", ["Entrar", "Criar Conta"])

    username = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if aba == "Criar Conta":
        if st.button("Criar Conta", use_container_width=True):
            if registrar_usuario(username, senha):
                st.success("Conta criada!")
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

# ---------------- MENU MOBILE ----------------
st.title("💰 Meu Controle Financeiro")

menu = st.selectbox(
    "Escolha uma opção",
    [
        "🏠 Resumo",
        "➕ Registrar Ganho",
        "➖ Registrar Gasto",
        "📅 Histórico do Mês",
        "🗑️ Corrigir Registros",
        "⚙️ Conta"
    ]
)

dados = carregar_dados(usuario)

# ---------------- RESUMO ----------------
if menu == "🏠 Resumo":
    total_receitas = sum(r["valor"] for r in dados["receitas"])
    total_gastos = sum(g["valor"] for g in dados["gastos"])
    saldo = total_receitas - total_gastos

    st.subheader("Resumo Geral")

    st.metric("💰 Total Recebido", f"R$ {total_receitas:,.2f}")
    st.metric("💸 Total Gasto", f"R$ {total_gastos:,.2f}")

    if saldo >= 0:
        st.metric("🟢 Saldo Atual", f"R$ {saldo:,.2f}")
    else:
        st.metric("🔴 Saldo Negativo", f"R$ {abs(saldo):,.2f}")

# ---------------- REGISTRAR GANHO ----------------
elif menu == "➕ Registrar Ganho":
    st.subheader("Novo Ganho")

    valor = st.number_input("Valor recebido", min_value=0.0)
    origem = st.text_input("Origem (opcional)")
    data_input = st.date_input("Data", value=date.today())

    if st.button("Salvar Ganho", use_container_width=True):
        adicionar_receita(usuario, {
            "data": str(data_input),
            "valor": valor,
            "origem": origem
        })
        st.success("Ganho registrado!")

# ---------------- REGISTRAR GASTO ----------------
elif menu == "➖ Registrar Gasto":
    st.subheader("Novo Gasto")

    valor = st.number_input("Valor gasto", min_value=0.0)
    categoria = st.selectbox(
        "Categoria",
        ["Casa", "Transporte", "Alimentação", "Trabalho", "Emergência"]
    )
    tipo = st.radio("Tipo", ["normal", "inesperado"])
    data_input = st.date_input("Data", value=date.today())

    if st.button("Salvar Gasto", use_container_width=True):
        adicionar_gasto(usuario, {
            "data": str(data_input),
            "valor": valor,
            "categoria": categoria,
            "tipo": tipo
        })
        st.success("Gasto registrado!")

# ---------------- HISTÓRICO DO MÊS ----------------
elif menu == "📅 Histórico do Mês":
    st.subheader("Resumo Mensal")

    df_receitas = pd.DataFrame(dados['receitas'])
    df_gastos = pd.DataFrame(dados['gastos'])

    if df_receitas.empty and df_gastos.empty:
        st.info("Nenhum dado registrado ainda.")
        st.stop()

    if not df_receitas.empty:
        df_receitas['data'] = pd.to_datetime(df_receitas['data'])
        df_receitas['tipo'] = 'Receita'

    if not df_gastos.empty:
        df_gastos['data'] = pd.to_datetime(df_gastos['data'])
        df_gastos['tipo'] = 'Gasto'

    df = pd.concat([df_receitas, df_gastos], ignore_index=True)

    meses = df['data'].dt.to_period('M').astype(str).unique()
    mes_selecionado = st.selectbox("Escolha o mês", sorted(meses, reverse=True))

    ano, mes = map(int, mes_selecionado.split('-'))
    df_mes = df[(df['data'].dt.month == mes) & (df['data'].dt.year == ano)]

    df_pivot = df_mes.pivot_table(
        index='data',
        columns='tipo',
        values='valor',
        aggfunc='sum'
    ).fillna(0)

    st.bar_chart(df_pivot)

    st.markdown("### 📜 Registros do mês")
    st.dataframe(df_mes.sort_values('data', ascending=False), use_container_width=True)

# ---------------- CORRIGIR REGISTROS ----------------
elif menu == "🗑️ Corrigir Registros":
    st.subheader("Apagar Registros")

    for tipo in ["receita", "gasto"]:
        lista = dados[tipo + "s"]
        if not lista:
            continue

        st.markdown(f"### {tipo.capitalize()}s")

        for i, item in enumerate(lista):
            descricao = f"{item['data']} - R$ {item['valor']:.2f}"
            if tipo == "gasto":
                descricao += f" - {item.get('categoria','')}"
            else:
                descricao += f" - {item.get('origem','')}"

            if st.checkbox(descricao, key=f"{tipo}_{i}"):
                lista[i]["apagar"] = True

        if st.button(f"Confirmar exclusão de {tipo}s", use_container_width=True):
            dados[tipo + "s"] = [r for r in lista if not r.get("apagar", False)]
            salvar_dados(usuario, dados)
            st.success("Registros atualizados!")
            st.rerun()

# ---------------- CONTA ----------------
elif menu == "⚙️ Conta":
    st.write(f"Usuário: {usuario}")
    if st.button("Sair", use_container_width=True):
        st.session_state.usuario_logado = None
        st.rerun()
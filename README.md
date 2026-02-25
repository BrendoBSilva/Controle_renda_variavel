# 📱 Controle de Renda Variável — Aplicação Mobile-First com Streamlit V3

Aplicação web desenvolvida em SQL e Python utilizando Streamlit para gerenciamento de renda variável e gastos imprevisíveis.

O projeto foi estruturado com separação de responsabilidades, arquitetura modular e foco em experiência mobile.

---

# 🎯 Objetivo

Desenvolver uma aplicação de interface simples, escalável e modular para auxiliar trabalhadores com renda variável no controle financeiro mensal, permitindo:

- Registro rápido de receitas
- Registro categorizado de gastos
- Visualização de saldo
- Histórico mensal com visualização gráfica
- Correção de registros incorretos
- Suporte multiusuário

---

# 🏗️ Arquitetura do Sistema

O sistema foi dividido em camadas com responsabilidades bem definidas:

## 1️⃣ Interface (main.py)

Responsável por:

- Renderização da interface com Streamlit
- Controle de sessão
- Navegação mobile-first
- Interação com o usuário
- Chamada das funções de negócio

## 2️⃣ Camada de Autenticação (auth.py)

Responsável por:

- Registro de novos usuários
- Validação de login
- Leitura e escrita segura em JSON
- Tratamento de arquivos corrompidos

## 3️⃣ Camada de Dados (data_manager.py)

Responsável por:

- Persistência em JSON
- Separação de dados por usuário
- Estruturação de receitas e gastos
- Atualização segura dos registros

---

# 📂 Estrutura do Projeto


Controlerendavariavel/
│
├── main.py
├── auth.py
├── data_manager.py
├── requirements.txt
├── usuarios.json
├── dados.json


---

# 🧠 Modelagem de Dados

## Estrutura de Usuários (usuarios.json)

```json
[
  {
    "username": "usuario1",
    "senha": "1234"
  }
]
Estrutura de Dados Financeiros (dados.json)
{
  "usuario1": {
    "receitas": [
      {
        "data": "2026-02-21",
        "valor": 100.0,
        "origem": "Venda"
      }
    ],
    "gastos": [
      {
        "data": "2026-02-21",
        "valor": 50.0,
        "categoria": "Casa",
        "tipo": "normal"
      }
    ]
  }
}

Cada usuário possui isolamento completo de dados.

📱 Design Mobile-First

O layout foi desenvolvido priorizando uso em celular:

Layout centralizado

Menu superior (sem sidebar)

Botões com largura total

Uso de use_container_width=True

Gráficos responsivos com st.bar_chart

Evita múltiplas colunas

📊 Funcionalidades Implementadas

Autenticação multiusuário

Registro de receitas

Registro de gastos (normal / inesperado)

Resumo financeiro automático

Histórico mensal filtrável

Visualização gráfica por mês

Exclusão seletiva de registros

Controle de sessão com st.session_state

⚙️ Tecnologias Utilizadas

Python 3.13

Streamlit

Pandas

JSON como mecanismo de persistência

Git

GitHub

🔐 Tratamento de Erros Implementado

Verificação de arquivos inexistentes

Tratamento de JSON corrompido

Garantia de estrutura correta (list/dict)

Proteção contra NoneType

Controle seguro de sessão

🚀 Como Executar Localmente

Clone o repositório:

git clone https://github.com/SEU_USUARIO/controlerenda.git

Instale as dependências:

pip install -r requirements.txt

🌍 Deploy realizado no Streamlit cloud

Atualização 1 - Inserção de meta do mês, score e projeção final
Atualização 2 - Migração para sqlite3, e exclusão do JSON para melhora de performance (cadastro persiste).



👨‍💻 Autor

Brendo Barbosa Silva
Graduando em Análise e Desenvolvimento de Sistemas e Ciência de dados
Interesse em Engenharia de Dados, Análise de Dados e Finanças

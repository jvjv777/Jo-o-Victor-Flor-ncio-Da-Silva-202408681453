import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Dashboard de Funcionários", layout="wide")
st.title("📊 Dashboard de Análise de Funcionários")

@st.cache_data
def carregar_dados():
    dados = {
        "nome": ["Ana", "Bruno", "Carlos", "Daniela", "Eduardo"],
        "idade": [23, 35, 29, np.nan, 40],
        "cidade": ["SP", "RJ", "SP", "MG", "RJ"],
        "salario": [3000, 5000, 4000, 3500, np.nan],
        "data_contratacao": pd.to_datetime(["2022-01-10", "2021-05-15", "2023-03-20", "2022-11-01", "2020-08-05"])
    }
    df = pd.DataFrame(dados)
    
    # Limpeza
    df["idade"] = df["idade"].fillna(df["idade"].mean())
    df["salario"] = df["salario"].fillna(df["salario"].median())
    
    # Novas colunas
    df["salario_anual"] = df["salario"] * 12
    df["ano_contratacao"] = df["data_contratacao"].dt.year
    df["categoria_salario"] = df["salario"].apply(
        lambda x: "Alto" if x > 4500 else "Médio" if x > 3000 else "Baixo"
    )
    return df

df = carregar_dados()

# Sidebar - Filtros
st.sidebar.header("🔎 Filtros")
cidades = st.sidebar.multiselect("Cidade", options=df["cidade"].unique(), default=df["cidade"].unique())
faixa_salario = st.sidebar.slider("Faixa Salarial", 
                                  float(df["salario"].min()), 
                                  float(df["salario"].max()), 
                                  (float(df["salario"].min()), float(df["salario"].max())))

df_filtrado = df[(df["cidade"].isin(cidades)) & 
                 (df["salario"] >= faixa_salario[0]) & 
                 (df["salario"] <= faixa_salario[1])]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("💰 Salário Médio", f"R$ {df_filtrado['salario'].mean():.2f}")
col2.metric("👥 Total Funcionários", df_filtrado.shape[0])
col3.metric("📈 Salário Máximo", f"R$ {df_filtrado['salario'].max():.2f}")

# Tabela
st.subheader("📋 Dados Filtrados")
st.dataframe(df_filtrado, use_container_width=True)

# Gráficos
st.subheader("📊 Análises")
col_g1, col_g2 = st.columns(2)
col_g1.bar_chart(df_filtrado.groupby("cidade")["salario"].mean())
col_g2.bar_chart(df_filtrado["categoria_salario"].value_counts())

# Pivot
st.subheader("📌 Tabela Dinâmica")
pivot = pd.pivot_table(df_filtrado, values="salario", index="cidade", columns="categoria_salario", aggfunc="mean")
st.dataframe(pivot)

# Download
csv = df_filtrado.to_csv(index=False).encode("utf-8")
st.download_button("Baixar CSV Filtrado", csv, "dados_filtrados.csv", "text/csv")

st.success("✅ Dashboard concluído!")

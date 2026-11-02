import streamlit as st

from src.data_loader import load_data

st.set_page_config(page_title="Análise de Falhas de Baterias de Veículos Elétricos", layout="wide")
st.title("Análise de Falhas de Baterias de Veículos Elétricos")
st.caption("EV Battery Failure Dataset — exploração das variáveis quantitativas")

df = load_data()

VARS_QUANT = ["manufacturing_year", "battery_capacity_kwh", "odometer_km"]

ROTULOS = {
    "manufacturing_year": "Ano de fabricação",
    "battery_capacity_kwh": "Capacidade da bateria (kWh)",
    "odometer_km": "Quilometragem (km)",
}

with st.sidebar:

    st.header("Filtros")

    variaveis = st.multiselect(
        "Variáveis quantitativas",
        options=VARS_QUANT,
        default=VARS_QUANT,
        format_func=lambda var: ROTULOS[var],
    )

    intervalos = {}

    for var in variaveis:

        if var == "manufacturing_year":
            minimo, maximo, passo = int(df[var].min()), int(df[var].max()), 1
        else:
            minimo, maximo, passo = float(df[var].min()), float(df[var].max()), 0.1

        if minimo == maximo:
            st.caption(f"{ROTULOS[var]}: todos os veículos têm o valor {minimo}.")
            continue

        intervalos[var] = st.slider(
            ROTULOS[var],
            min_value=minimo,
            max_value=maximo,
            value=(minimo, maximo),
            step=passo,
            key=f"intervalo_{var}",
        )

df_filtrado = df

for var, (inicio, fim) in intervalos.items():
    df_filtrado = df_filtrado[df_filtrado[var].between(inicio, fim)]

st.caption(f"{len(df_filtrado):,} de {len(df):,} veículos dentro dos intervalos escolhidos.")

col_correlacao, col_distribuicao = st.columns([1, 1.5])

with col_correlacao:
    st.subheader("Correlação")

    if len(variaveis) < 2:
        st.warning("Selecione pelo menos 2 variáveis para analisar a correlação.")
    elif df_filtrado.empty:
        st.warning("Nenhum veículo dentro dos intervalos escolhidos.")
    else:
        st.info("Espaço reservado para o mapa de correlação das variáveis selecionadas.")

with col_distribuicao:
    
    st.subheader("Distribuição")
    
    if not variaveis:
        st.warning("Selecione pelo menos 1 variável para analisar a distribuição.")
    elif df_filtrado.empty:
        st.warning("Nenhum veículo dentro dos intervalos escolhidos.")
    else:
        st.info("Espaço reservado para as distribuições das variáveis selecionadas.")
